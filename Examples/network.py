#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink

# OBBIETTIVO DEL PROGRAMMA: creazione dell'infrastruttura di rete



class NetworkSlicingTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        # sono dei template con capacità di bandwidth diversa. Vengono utilizzati successivamente per creare i vari link di collegamento tra switch e host
        # Attenzione! Non alzare troppo i valori di bw. Sopra i 50/60, siccome siamo in una macchina virtuale con container virtuali, potrebbero esserci dei limiti
        host_config = dict(inNamespace=True)
        http_link_config = dict(bw=1)
        video_link_config = dict(bw=10)
        host_link_config = dict()

        # Create switch nodes
        # crea 4 switch.
        for i in range(4):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), **sconfig)

        # Create host nodes
        # crea 4 host
        for i in range(4):
            self.addHost("h%d" % (i + 1), **host_config)

        # Add switch links
        # Costruisce i collegamenti tra gli switch utilizzando i template definidi in precedenza.
        # Le porte di ogni switch vengono nomicate seguondo l'ordine in cui vengono creati i collegamenti 
        self.addLink("s1", "s2", **video_link_config)   # bw = 10
        self.addLink("s2", "s4", **video_link_config)   # bw = 10
        self.addLink("s1", "s3", **http_link_config)    # bw = 1
        self.addLink("s3", "s4", **http_link_config)    # bw = 1

        # Add host links
        # costruisce i collegamenti tra gli switch e gli host. Viene utilizzato un template definito in precedenza (ma che bw avranno?)
        self.addLink("h1", "s1", **host_link_config)
        self.addLink("h2", "s1", **host_link_config)
        self.addLink("h3", "s4", **host_link_config)
        self.addLink("h4", "s4", **host_link_config)


topos = {"networkslicingtopo": (lambda: NetworkSlicingTopo())}

if __name__ == "__main__": # effetto: il codice verrà eseguito solo quando il programma verrà eseguito come uno script (ex. da terminale)
    
    # inizializziamo la tipologia appena definita (verrà utilizzata per costruire la rete nelle righe successive)
    topo = NetworkSlicingTopo() 
    
    # creazione della rete tramite un oggetto di tipo Mininet
    # E' possibile utilizzare la primitiva Containernet() nel caso si vogliano utilizzare i containers, altrimenti la primitiva Mininet() è sufficiente
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )

    # istanziamo un controller. In realtà non viene creato ma ci aspettiamo che sia disponibile all'ip locale 127.0.0.1
    controller = RemoteController("c1", ip="127.0.0.1", port=6633)
    # aggiungiamo il controller alla rete
    net.addController(controller)
    # costruiamo la rete (da fare quando viene utilizzata una topologia particolare)
    net.build()
    # facciamo partire la rete
    net.start()
    # restituiamo il controllo all'utente
    CLI(net)
    net.stop()
