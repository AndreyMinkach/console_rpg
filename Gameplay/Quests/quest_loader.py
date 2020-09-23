import os
import json
import warnings


class QuestLoader:
    instance = None
    quest_json_pattern = {}

    def __init__(self):
        self.__class__.instance = self
        self._load_quests_from_json()

    def _load_quests_from_json(self):
        folder_path = 'Static/Quests/'
        file_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.json')]
        for f in file_list:
            with open(f, 'r') as temp_file:
                temp_json = json.load(temp_file)
                for json_element in temp_json:
                    match_result = self.match_pattern(json_element)
                    if match_result is False:
                        warnings.warn(f"The dictionary '{json_element}' in  is invalid")

    def match_pattern(self, json_to_match: dict):
        for key, value in json_to_match.items():
            print(key, value)

    def get_quest_by_id(self, quest_id: str):
        pass
