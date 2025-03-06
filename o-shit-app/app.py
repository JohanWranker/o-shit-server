from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, world! This is a Flask app behind Caddy."


if __name__ == "__main__":
    # Flask listens on port 5000 so Caddy can reverse proxy to it.
    app.run(host="0.0.0.0", port=5000, debug=True)
