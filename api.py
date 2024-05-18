import flask
from flask import jsonify
from flask_limiter import Limiter, RateLimitExceeded
from flask_limiter.util import get_remote_address

from wordnet import getWordNet

app = flask.Flask(__name__)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,  # Use the client's IP address as the key
    default_limits=["200 per day", "50 per hour"],
)
app.config["JSON_AS_ASCII"] = False


@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Nepali WordNet API"


@app.route("/<word>", methods=["GET"])
@limiter.limit("10 per second")
def get_word(word):
    return jsonify(getWordNet(word))


@app.errorhandler(RateLimitExceeded)
def ratelimit_handler(e):
    return jsonify(error="ratelimit exceeded"), 429


if __name__ == "__main__":
    app.run(debug=True)
