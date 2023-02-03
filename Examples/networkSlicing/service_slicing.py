from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import udp
from ryu.lib.packet import tcp
from ryu.lib.packet import icmp

# OBIETTIVO: definire le regole da implementare nel controller con ryu. Vogliamo creare due slices (una da 10bw e una da 1bw) che connettono entrambe h1, h2, h3 e h4
#            ma distinguiamo le slices sula base del traffico generato dagli utenti (es. il traffico create su una certa porta viene gestito da uno slice,
#            quello creato su altre porte andrà su altri slices)
# NOTA: è un file .py ma verrà lanciato come "script northbound" del controller ryu (infatti vengono importate le librerie di ryu)
# PER CHIAMARLO DA TERMINALE: ryu-manager topology_slicing.py


class TrafficSlicing(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TrafficSlicing, self).__init__(*args, **kwargs)

        # outport = self.mac_to_port[dpid][mac_address]
        self.mac_to_port = {
            1: {"00:00:00:00:00:01": 3, "00:00:00:00:00:02": 4},
            4: {"00:00:00:00:00:03": 3, "00:00:00:00:00:04": 4},
        }
        # creiamo una porta (9999). Assumiamo che si riceva traffico video su questa (ha bisogno di bw elevata, quindi utilizzeremo lo slice da 10bw).
        # Tutto il resto del traffico può essere allocato sullo slice da 1bw
        self.slice_TCport = 9999

        # outport = self.slice_ports[dpid][slicenumber]
        self.slice_ports = {1: {1: 1, 2: 2}, 4: {1: 1, 2: 2}}
        self.end_swtiches = [1, 4]

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)
        ]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath, priority=priority, match=match, instructions=inst
        )
        datapath.send_msg(mod)

    def _send_package(self, msg, datapath, in_port, actions):
        data = None
        ofproto = datapath.ofproto
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        datapath.send_msg(out)

    # _packet_in_handler (vedi "topology_slicing.py" per spiegazione)
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath                     # viene letto il datapath di ciò che è arrivato
        ofproto = datapath.ofproto                  # viene letto la versione del protocollo OpenFlow
        in_port = msg.match["in_port"]              # viene letta la porta in ingresso del pacchetto

        pkt = packet.Packet(msg.data)               # salviamo su "pkt" il payload del pacchetto ricevuto
        eth = pkt.get_protocol(ethernet.ethernet)   # salviamo su "eth" il protocollo di L2 in cui è incapsulato il pacchetto (utilizzando "pkt")

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:      # tramite "eth" acceddiamo all'intestazione ethernet, in particolare al tipo di protoccolo di L2
            # ignore lldp packet
            return
        dst = eth.dst       # leggiamo destinazione di L2
        src = eth.src       # leggiamo sorgente di L2

        dpid = datapath.id

        if dpid in self.mac_to_port:                
            if dst in self.mac_to_port[dpid]: # se la destinazione è nella tabella "mac_to_port" definita inizialmente
                out_port = self.mac_to_port[dpid][dst]
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(eth_dst=dst)
                self.add_flow(datapath, 1, match, actions)
                self._send_package(msg, datapath, in_port, actions)

            elif (pkt.get_protocol(udp.udp) and pkt.get_protocol(udp.udp).dst_port == self.slice_TCport): # se il protocollo è UDP e la porta di destinazione è 9999
                slice_number = 1 # mandiamo il flusso nello slice 1 ad alta capacità (da 10bw)
                #definiamo una nuova regola di matching:
                out_port = self.slice_ports[dpid][slice_number] # la porta in uscita dipenderà dalle porta associate allo slice 1
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    eth_dst=dst,
                    eth_type=ether_types.ETH_TYPE_IP,
                    ip_proto=0x11,  # udp
                    udp_dst=self.slice_TCport,
                )

                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)] # crea l'azione
                self.add_flow(datapath, 2, match, actions) # aggiunge l'azione alla tabella dello switch
                self._send_package(msg, datapath, in_port, actions)

            elif (pkt.get_protocol(udp.udp) and pkt.get_protocol(udp.udp).dst_port != self.slice_TCport): # se il protocollo è UDP ma la porta di destinazione NON è 9999
                slice_number = 2 # mandiamo il flusso nello slice 2 a bassa capacità (da 1bw)
                out_port = self.slice_ports[dpid][slice_number]
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    eth_dst=dst,
                    eth_src=src,
                    eth_type=ether_types.ETH_TYPE_IP,
                    ip_proto=0x11,  # udp
                    udp_dst=pkt.get_protocol(udp.udp).dst_port,
                )
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
                self._send_package(msg, datapath, in_port, actions)

            elif pkt.get_protocol(tcp.tcp): # se il protocollo è TCP lo trattiamo uguale al caso precedente
                slice_number = 2
                out_port = self.slice_ports[dpid][slice_number]
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    eth_dst=dst,
                    eth_src=src,
                    eth_type=ether_types.ETH_TYPE_IP,
                    ip_proto=0x06,  # tcp
                )
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
                self._send_package(msg, datapath, in_port, actions)

            elif pkt.get_protocol(icmp.icmp): # se il protocollo è ICMP lo trattiamo uguale al caso precedente
                slice_number = 2
                out_port = self.slice_ports[dpid][slice_number]
                match = datapath.ofproto_parser.OFPMatch(
                    in_port=in_port,
                    eth_dst=dst,
                    eth_src=src,
                    eth_type=ether_types.ETH_TYPE_IP,
                    ip_proto=0x01,  # icmp
                )
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, 1, match, actions)
                self._send_package(msg, datapath, in_port, actions)

        elif dpid not in self.end_swtiches: # altrimenti gli switch fanno un "FLOOD" (da una porta all'altra)
            out_port = ofproto.OFPP_FLOOD
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
            match = datapath.ofproto_parser.OFPMatch(in_port=in_port)
            self.add_flow(datapath, 1, match, actions)
            self._send_package(msg, datapath, in_port, actions)


# NOTA
#       Una volta costruita la topology ed eseguito questo programma, possiamo testare il network tramite i due seguenti comandi.
#       Utilizzando la porta 9999 e UDP ci aspettiamo di utilizzare lo slice1 da 10bw
#
#           $ h3 iperf -s -u -p 9999 -b 20M &
#               -s          ---> da lato server
#               -u          ---> utilizzando UDP
#               -p 9999     ---> indirizza alla porta 9999
#               -b 20M      ---> genera traffico fino a 20Mbit (in realtà sarà poi limitato a 10 dal link)
#               &           ---> esegue in backgorund
#
#           $ h1 iperf -c 10.0.0.3 -u -p 9999 -b 20M -t 10 -i 1
#               -c          ---> da lato client
#               10.0.0.3    ---> ip del server
#               -u          ---> UDP
#               -p 9999     ---> porta
#               -b 20M      ---> riceve un flusso di 20Mb (in realtà sarà 10 perché limitato dal link)
#               -t 10       ---> 10 secondi di misurazione 
#               -i 1        ---> misurazioni a intervallo di un secondo
#
#       Se gli stessi comandi venissero eseugiti utilizzando una porta diversa da 9999, allora il flusso verrà allocato nello slice2 da 1bw