from Helpers.json_loader import JsonLoader


class Location:
    def __init__(self):
        pass


class LocationManager(JsonLoader):
    instance: 'LocationManager' = None
    json_verify_pattern: dict = {"id": str, "name": str, "relationship": list, "location_points": list}

    def __init__(self):
        super().__init__("Static/Locations/", verify_pattern=self.__class__.json_verify_pattern)
        self._locations_dictionary = {}

        self._load_locations_from_json()

    def _load_locations_from_json(self):
        for location_dict in self.loaded_element_list:
            self._locations_dictionary[location_dict["id"]] = location_dict
