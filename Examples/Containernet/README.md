# ESEMPIO USO CONTAINER COME APPLICAZIONE CLIENT SERVER IN MININET
(Esempio preso pari pari da repo di containernet)

Set up delle immagini che verranno utilizzato
- `Dockerfile.server` Si basa su un immagine python, installa le dipendenze e copia l'intera directory (.) nella cartella `/app`
- `Dockerfile.client` Si basa su un immagine ubuntu 20 e installa le dipendenze

Per buildare le immagini dai dockerfiles:
```BASH
docker build -f Dockerfile.[client/server] -t test_[client/server]:latest
```

Programma **_demo.py_**:
- Crea una rete con Containernet(). Aggiunge due host basati su due Docker containers.
- Il container server, appena viene istanziato, esegue il programma app.py
- Setuppa la rete (aggiunge due switch):	[Server] --- [s1] --- [s2] --- [Client]
- utilizza il client per fare un curl sul server

Programma **_app.py_**:
- Setuppa il webserver con Flask (per documentazione Flask: https://flask.palletsprojects.com/en/2.2.x/quickstart/)
