from io import BytesIO
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from requests import get as http_get
from flask import send_file


class Utils(object):
    @staticmethod
    def percentage_part(part, percent) -> float:
        return float(part) / 100 * percent


class Generator:
    def __init__(self, quality: int = 80, image: Image = None, profile: dict = {
        "name": "Пользователь", "age": 18, "city": "Киев", "description": ""
    }) -> None:
        self.quality = quality
        self.image = image
        self.color_mode = 'RGB'
        self.profile = profile

        self.fonts_dir = "fonts/"
        self.bold_font = self.fonts_dir + "NunitoSans-ExtraBold.ttf"
        self.font = self.fonts_dir + "Mulish-VariableFont_wght.ttf"

    def calculate_background_size(self, image: Image) -> tuple:
        width, height = image.size
        max_ = max([
            height + int(Utils.percentage_part(height, 12))
        ])
        return (max_, max_ + self.calculate_datablock(height))

    def calculate_center_pos(self, size_back: tuple, size_image: tuple) -> tuple:
        w_b, h_b = size_back; w_i, h_i = size_image
        if w_b > w_i: return (int((w_b - w_i) / 2), int(Utils.percentage_part(w_b, 8)))
        if h_b > h_i: return (int(Utils.percentage_part(h_b, 8)), int((h_b - h_i) / 2))

    def calculate_datablock(self, height: int) -> int:
        return int(Utils.percentage_part(height, 15))

    def _add_text_datablock(self, image: Image) -> Image:
        _, h = image.size
        draw = ImageDraw.Draw(image)
        calc_ = int(Utils.percentage_part(h, 3))
        # Draw user name
        font_name = ImageFont.truetype(self.bold_font, int(Utils.percentage_part(h, 4.5)))
        draw.text(
            (calc_, h - (self.calculate_datablock(h) - calc_)),
            "%s, %d" % (self.profile["name"], self.profile["age"]), (255, 255, 255), font=font_name
        )
        # Draw city
        font_city = ImageFont.truetype(self.bold_font, int(Utils.percentage_part(h, 2.8)))
        draw.text(
            (calc_, h - (self.calculate_datablock(h) - calc_ * 3)),
            self.profile["city"], (255, 255, 255), font=font_city
        )
        return image

    def create_background(self, image: Image) -> Image:
        calculated_size = self.calculate_background_size(image)
        image = image.resize(calculated_size, Image.ANTIALIAS)
        image = image.filter(ImageFilter.GaussianBlur(max(calculated_size) / 6))
        return image

    def image_paste(self, back: Image, front: Image) -> Image:
        back.paste(front, self.calculate_center_pos(back.size, front.size)); return back

    def image_proc(self, pil_img: Image) -> send_file:
        img_io = BytesIO()
        pil_img.save(img_io, 'JPEG', quality=self.quality)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')

    def get_image_from_url(self, url: str) -> Image:
        response = http_get(url)
        return Image.open(BytesIO(response.content))

    @property
    def builder(self) -> Image:
        return self._add_text_datablock(self.image_paste(
            self.create_background(self.image), self.image
        ))

    @property
    def get(self) -> send_file:
        return self.image_proc(self.builder)
