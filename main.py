import logging
import os
import sentry_sdk
from flask import Flask, request, jsonify, send_file
from sentry_sdk.integrations.flask import FlaskIntegration
from generator import Generator
from other import Other
from middleware import Validator

sentry_sdk.init(
    dsn=os.getenv("SENTRY_KEY"),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

app = Flask(__name__)


@app.errorhandler(500)
def page_not_found(error) -> jsonify:
    logging.error("Error in %s: %s", request.url, error)
    return Other.get_img_error(500)


@app.errorhandler(400)
def page_not_found(error) -> jsonify:
    logging.error("Error in %s: %s", request.url, error)
    return Other.get_img_error(400)


@app.errorhandler(404)
def page_not_found(error) -> jsonify:
    logging.error("Error in %s: %s", request.url, error)
    return Other.get_img_error(404)


@app.errorhandler(405)
def page_not_found(error) -> jsonify:
    logging.error("Error in %s: %s", request.url, error)
    return Other.get_img_error(405)


@app.errorhandler(408)
def page_not_found(error) -> send_file:
    logging.error("Error in %s: %s", request.url, error)
    return Other.get_img_error(408)


@app.route("/generate_image", methods=['POST'])
def generate_image() -> send_file:
    data = request.get_json()
    data["profile"] = Validator.fix_desc(data["profile"])
    error_profile = Validator.validate_profile(data["profile"])
    if not error_profile and (1 < data["quality"] <= 75):
        return Generator(
            quality=data["quality"],
            image=Generator().get_image_from_url(data['url']),
            profile=data["profile"]
        ).get


if __name__ == "__main__":
    app.run()
