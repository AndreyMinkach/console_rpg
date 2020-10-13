import warnings

from Helpers.json_loader import JsonLoader


def location_name_to_id(location_name: str) -> str:
    return location_name.strip().lower().replace(' ', '_')


class Location:
    def __init__(self):
        self.name: str = ''
        self.connections: list = []
        self.map_image_path = ''
        self.location_points: list = []

    def get_location_point(self, point_id: str) -> dict:
        for point in self.location_points:
            if point['id'] == point_id:
                return point
        warnings.warn(f"There is no location point '{point_id}' inside the '{self.name}' location!")
        return None


class LocationManager(JsonLoader):
    instance: 'LocationManager' = None
    json_verify_pattern: dict = {"name": str, "connections": list, "map_image_path": str, "location_points": list}

    def __init__(self):
        self.__class__.instance = self
        super().__init__("Static/Locations/", verify_pattern=self.__class__.json_verify_pattern)
        self._locations_dictionary = {}

        self._load_locations_from_json()

    def _load_locations_from_json(self):
        for location_dict in self.loaded_element_list:
            self._locations_dictionary[location_name_to_id(location_dict["name"])] = location_dict
        print(self._locations_dictionary)

    def get_location_by_name(self, location_name: str) -> Location:
        location_id: str = location_name_to_id(location_name)
        if location_id in self._locations_dictionary:
            location_dict = self._locations_dictionary[location_id]
            location_object = Location()
            location_object.__dict__.update(location_dict)
            return location_object
        else:
            warnings.warn(f"There is no location with id '{location_id}', source name is '{location_name}'")
