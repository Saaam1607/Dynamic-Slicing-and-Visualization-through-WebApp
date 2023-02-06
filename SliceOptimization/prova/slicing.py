from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3

# OBIETTIVO: definire le regole da implementare nel controller con ryu
# NOTA: è un file .py ma verrà lanciato come "script northbound" del controller ryu (infatti vengono importate le librerie di ryu)
# PER CHIAMARLO DA TERMINALE: ryu-manager topology_slicing.py

# NOTE INTERESSANTI:
#      -) Una volta eseguito il controller e creato lo scenario, i comandi "dump" e "links" sono utili per controllare come è stata creata la topologia
#      -) "pingall" è il metodo più semplice per verificare che il controller e la topology siano stati creati correttamente
#      -) per creare traffico artificale tra hosts (a seconda del bandwidth del collegamento tra gli hosts) è possibile utilizare "iperf h1 h2" (ovviamente solo tra host nello stesso slice)


class TrafficSlicing(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TrafficSlicing, self).__init__(*args, **kwargs)

        # out_port = slice_to_port[dpid][in_port]
        # dato uno switch, viene definito come collegare la porta d'ingresso con la porta d'uscita. Si tratta di una sorta di regola che utilizziamo
        # per definire ognli slice. In pratica possiamo isolare di flussi all'interno di uno swtich
        # Per capire come sono assegnate le porte, vedere in network.py e seguire l'ordina di creazizione dei links
        self.slice_to_port = {
            1: {1: 3, 3: 1, 2: 4, 4: 2},                
            4: {1: 3, 3: 1, 2: 4, 4: 2},
            2: {1: 2, 2: 1},
            3: {1: 2, 2: 1},
        }
        # Esempio (prima entry, ovvero switch1):
        #       tutto quello che entra nella porta 1, esce dalla porta 3
        #       tutto quello che entra nella porta 3, esce dalla porta 1
        #       tutto quello che entra nella porta 2, esce dalla porta 4
        #       tutto quello che entra nella porta 4, esce dalla porta 2

    # funzione per l'HANDSHAKE
    # all'inizio della session il controller invia un messaggio FEATURE REQUEST allo switch (viene gestito da Ryu)
    # lo switch risponde con un messaggio FEATURE REPLY
    # il messaggio 
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

    # il _packet_in_handler è il gestore dei pacchetti in ingresso al controller.
    # In pratica definisce il comportamento del controller quando vuole scrivere una nuova regola perché ha ricevuto un pacchetto che prima non era nelle flowTables
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath             # viene letto il datapath di ciò che è arrivato
        in_port = msg.match["in_port"]        # viene letta la porta in ingresso del pacchetto ricevuto
        dpid = datapath.id                    # viene letto il datapathID del pacchetto ricevuto (== numero dello switch in cui è stato ricevuto il pacchetto)

        # viene letta la tabella slice_to_port e sulla base di qual'è lo switch ricevente e la porta in cui ha ricevuto verrà scelta la porta di uscita
        # (vedi la tabella slice_to_port per capire quale sarà)
        out_port = self.slice_to_port[dpid][in_port]                        # viene scelta la porta di uscita come spiegato
        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]       # parametro2 che verrà inserito nella FlowTable successivamente
        match = datapath.ofproto_parser.OFPMatch(in_port=in_port)           # parametro1 che verrà inserito nella FlowTable successivamente

        self.add_flow(datapath, 1, match, actions)              # l'azione compiuta viene aggiunta nella tabella delle azioni dello switch (nuova flowEntry)
        self._send_package(msg, datapath, in_port, actions)     # inoltra/invia il pacchetto secondo i parametri stabiliti
