import json

import Helpers.helper as helper
from Helpers.atlas_helper import TextureAtlas
from Scene.scene_object import SceneObject


class MapLoader:
    def __init__(self, map_json_filename='map.json', tileset_filename='tileset.png', folder=r'Static/Tileset/'):
        self.tileset_image = TextureAtlas.load_image(image_path=tileset_filename, folder=folder)
        self.map_dict = self._load_json(map_json_filename)
        self.tile_size = self.map_dict['tilewidth']
        self.image_height = self.map_dict['tilesets'][0]['imageheight']
        self.image_width = self.map_dict['tilesets'][0]['imagewidth']
        self.tileset_row_number = self.image_height // self.tile_size
        self.tileset_column_number = self.image_width // self.tile_size
        self.map_tiles = dict()
        self.images_dict = dict()
        self.animated_tiles = dict()
        self.map_rows = self.map_dict['height']
        self.map_columns = self.map_dict['width']
        self.tile_indices = self.map_dict['layers'][0]['data']
        self._map_initialization()
        self.load_map()

    def load_map(self):
        """
        This method creates SceneObjects place them on map
        """

        _x, _y = x, y = (-self.map_columns // 2), (self.map_rows // 2)

        for index in range(len(self.tile_indices)):

            image_data = self.images_dict[self.tile_indices[index] - 1]

            sc = SceneObject(
                helper.get_animation(
                    images=image_data[0],
                    durations=image_data[1])
            )

            if self.tile_indices[index] - 1 in list(self.animated_tiles.keys()):
                sc.play_animation()

            if index % self.map_columns == 0:
                y -= 1
                x = _x
                sc.position = (x, y)
            else:
                x += 1
                sc.position = (x, y)

    def _map_initialization(self):
        """
        This method loads all necessary map data from json
        """

        image_id = 0

        # fill animated_tiles dictionary with duration and tile id lists
        for i in self.map_dict['tilesets'][0]['tiles']:
            self.animated_tiles[i['id']] = (
                [tile_id['duration'] for tile_id in i['animation']],
                [tile_id['tileid'] for tile_id in i['animation']]
            )

        # fill image_dict dictionary with loaded images from tileset image
        for i in range(self.tileset_row_number):
            for j in range(self.tileset_column_number):
                image_part = self.tileset_image.get_region(
                    x=j * self.tile_size,
                    y=self.image_height - (i * self.tile_size) - self.tile_size,
                    width=self.tile_size,
                    height=self.tile_size
                )

                self.images_dict[image_id] = ([image_part], [0])
                image_id += 1

        # fill animated_tiles dictionary with animated tiles and durations lists
        for key, value in self.animated_tiles.items():
            self.images_dict[key] = (
                [self.images_dict[animated_tile_id][0][0] for animated_tile_id in value[1]],
                [duration / 1000 for duration in value[0]]
            )

    @staticmethod
    def _load_json(file_name: str, folder=r'Static/Maps/') -> dict:
        """
        This method loads map.json file with all map data

        :return dict(): dict with map data
        """

        f = open(folder + file_name)
        return json.load(f)
