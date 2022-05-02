import logging
from flask import send_file, jsonify
from generator import Generator


class Other(object):
    @staticmethod
    def get_error(
            code: int, url: str = None, error: str = None, load_img: bool = False
    ) -> send_file or tuple:
        logging.error("Error in %s: %s", url, error)
        if load_img:
            return Generator().image_proc(Generator().get_image_from_url(
                "https://http.cat/%d" % code))
        return jsonify({"error": code}), code
