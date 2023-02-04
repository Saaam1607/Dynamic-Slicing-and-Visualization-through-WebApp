#!/usr/bin/python
"""
This is an example how to simulate a client server environment.
"""
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel

setLogLevel('info') # funzione di convenienza per impostare il LogLevel (è qualcosa del tipo l' "importanza")

# dichiarazione della rete
net = Containernet(controller=Controller) # Containernet è una classe di Mininet che permette l'esecuzione di alcuni metodi di Docker
net.addController('c0') # aggiunge il controller all'oggetto Containernet

# aggiunta dei container docker
info('*** Adding server and client container\n')
server = net.addDocker('server', ip='10.0.0.251', dcmd="python app.py", dimage="test_server:latest")    # aggiunge il container server che appena runna esegue comando 'python app.py'
                                                                                                        # come immagine runna l'immagine 'test_server:latest'
client = net.addDocker('client', ip='10.0.0.252', dimage="test_client:latest")                          # aggiunge il container client che runna l'immagine 'test_client:latest'

# setup della rete
info('*** Setup network\n')                                                                             
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
net.addLink(server, s1)
net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)
net.addLink(s2, client)
net.start()

# comandi da eseguire
info('*** Starting to execute commands\n')

info('Execute: client.cmd("time curl 10.0.0.251")\n')       # stampa indicazione su terminale
info(client.cmd("time curl 10.0.0.251") + "\n")             # il client accede al server.
                                                            # stampa su terminale il risultato di il risultato di curl (ovvero la pagina server)
                                                            # e il risutato di time (ovvero tempo di esecuzione). 

info('Execute: client.cmd("time curl 10.0.0.251/hello/42")\n')      # stampa indicazione su terminale
info(client.cmd("time curl 10.0.0.251/hello/42") + "\n")            # il client accede al server con il path (/hello/42)
                                                                    # triggera il decorator (vedi app.py, ovvero il programma eseguito sul lato server)
                                                                    # stampa id incrementato, ovvero 43 e capo
                                                                    # stampa il risultato di time

CLI(net)

net.stop()
