from PIL import Image


class ScreenToMinimap:

    def __init__(self, screen_width, screen_height):
        self.screen_width, self.screen_height = screen_width, screen_height
        self.minimap_width = self.minimap_height = 275

        self.x1, self.y1 = 1650, 45
        self.x2 = self.x1 + self.minimap_width
        self.y2 = self.y1 + self.minimap_height
        self.mid_x, self.mid_y = self.minimap_width // 2, self.minimap_height // 2

    def crop_minimap(self, img):
        if isinstance(img, Image.Image):
            return img.crop(box=(self.x1, self.y1, self.x2, self.y2))  # rgb
        return img[self.y1:self.y2, self.x1:self.x2]  # bgr numpy
