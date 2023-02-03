from flask import Flask                     # è un microframework per Python che permette di creare applicazioni web

app = Flask(__name__)

# non necessario, è solo per il setup di flask
@app.route("/")
def default():
    return "Hello world.\n"


@app.route("/hello/<id>")
def hello(id=0):
    try:
        id = int(id)
        id += 1
    except ValueError:
        pass
    return f"{id}\n"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
