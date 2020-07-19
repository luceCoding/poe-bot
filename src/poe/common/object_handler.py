from src.poe.screen.image_factory import ImageFactory


class ObjectHandler:

    def __init__(self, app):
        self._app = app
        self.obj_images = ImageFactory.get_object_images()
        self.obj_switch = {
            'waypoint': (self.obj_images['waypoint'],
                         self.obj_images['waypoint_post']),
            'stash': (self.obj_images['stash'],
                      self.obj_images['stash_post']),
            'seed_stockpile': (self.obj_images['seed_stockpile'],
                               self.obj_images['seed_stockpile_post']),
        }

    def open_object(self, object_name):
        # switch = {
        #     'waypoint': (self.obj_images['waypoint'],
        #                  self.obj_images['waypoint_post']),
        #     'stash': (self.obj_images['stash'],
        #               self.obj_images['stash_post']),
        #     'seed_stockpile': (self.obj_images['seed_stockpile'],
        #                        self.obj_images['seed_stockpile_post']),
        # }
        return self._app.click_on_image_and_wait_for(self.obj_switch[object_name][0],
                                                     self.obj_switch[object_name][1])
