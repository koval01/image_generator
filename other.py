import logging
from flask import send_file
from generator import Generator


class Other(object):
    @staticmethod
    def get_img_error(code: int, url: str, error: str) -> send_file:
        logging.error("Error in %s: %s", url, error)
        return Generator().image_proc(Generator().get_image_from_url(
            "https://http.cat/%d" % code))
