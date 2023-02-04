# ESEMPIO CREAZIONE DI UNA TOPOLOGIA DI NETWORK E DI SLICING IN MININET
Resources:
- Webinar del Granelli: https://www.youtube.com/watch?v=swJ8zEvwXcI
- Video dei bro di Comnetsemu: https://www.youtube.com/watch?v=kzw1gx2sWx4&t=2112s
- GitHub repo: https://git.comnets.net/public-repo/comnetsemu/-/tree/master/app/realizing_network_slicing

## topology.py
Il programma costruisce una network topology e startarla:
- crea 4 host, 4 switches e construisce un network attraverso dei link tra loro
- successivamente viene aggiunto un controller remoto.
- infine la network topology viene startata.

## topology_slicing.py
Il programma costruisce due slices utilizzando la topology creata in precedenza. L'obiettivo è dividere fisicamente i flussi di dati (in cui alcuni host possono raggiungere solo alcuni altri, simile ad un VLAN scenario)

- costruisce una matrice dove per ogni switch le porte di ingresso vengono mappate su porte di uscita (slice_ports)
- descrive la fase di "HANDSHAKE" tra il controller e gli switch
- descrive il gestore dei pacchetti in ingresso (_packet_in_handler). A seconda della porta in ingresso, viene utilizzata la matrice descritta in precedenza e viene scelta la porta di uscita. Infine l'azione viene inserita all'interno nella tabella delle azioni dello switch.

## service_slicing.py
Il programma crea un secondo tipo di slicing dove tutti gli host comunicano tra di loro. Il traffico viene gestito a seconda della TCport in cui viene ricevuto (il traffico proveniente da 9999, ovvero il presunto traffico vide viene rediretto su uno slice con bw=10, il resto su uno con bw=1)

- crea la tabella self.mac_to_port [...]
- costruisce una matrice dove per ogni switch le porte di ingresso vengono mappate su porte di uscita (slice_ports)
- descrive la fase di "HANDSHAKE" tra il controller e gli switch
- descrive il gestore dei pacchetti in ingresso (_packet_in_handler). In particolare verrà osservato il tipo di protocollo e la porta di ingresso del pacchetto per decidere con quale slice gestirlo