from flask import Flask                     # è un microframework per Python che permette di creare applicazioni web

app = Flask(__name__)

# @app.route("<url>") è un decorator: quando viene passato l'url (parametro), viene eseguita la funzione indicata

# non necessario, è solo per il setup di flask
@app.route("/")
def default():
    return "Hello world.\n"


@app.route("/hello/<id>")
def hello(id=0): # ritorna il valore passato come <id>
    try:
        id = int(id)
        id += 1
    except ValueError:
        pass
    return f"{id}\n"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
