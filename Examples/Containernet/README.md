# ESEMPIO USO CONTAINER COME APPLICAZIONE CLIENT SERVER IN MININET
(Esempio preso pari pari da repo di containernet)
- `Dockerfile.server` Si basa su un immagine python, installa le dipendenze e copia l'intera directory (.) nella cartella `/app`
- `Dockerfile.client` Si basa su un immagine ubuntu 20 e installa le dipendenze
Per buildare le immagini dai dockerfiles:
```BASH
docker build -f Dockerfile.[client/server] -t test_[client/server]:latest
```
- `app.py` Setuppa il webserver con flask
- `demo.py` Setup della rete (crea topologia e assegna i container ecc.)