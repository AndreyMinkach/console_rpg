import glob
import json
import warnings


class JsonLoader:
    """
    This class is used for loading json files, whose content is the list of dictionaries with the same structure
    """

    def __init__(self, folder_path: str, verify_pattern=None, load_recursively: bool = True):
        if verify_pattern is None:
            verify_pattern = {}
        self._folder_path = folder_path
        self._verify_pattern = verify_pattern
        self._load_recursively = load_recursively
        self.loaded_element_list = []
        self._load_files()

    def _load_files(self):
        file_list = glob.glob(self._folder_path + '/**/*.json', recursive=self._load_recursively)
        for f in file_list:
            with open(f, 'r') as temp_file:
                temp_json = json.load(temp_file)
                for element_dict in temp_json:
                    match_result, failure_reason = self._verify_dictionary_with_pattern(element_dict)
                    if match_result is False:
                        warnings.warn(
                            f"The dictionary '{element_dict}' in file '{f}' is invalid, the reason is {failure_reason}")
                        continue
                    self.loaded_element_list.append(element_dict)

    def _verify_dictionary_with_pattern(self, json_to_verify: dict):
        json_items = list(json_to_verify.items())
        pattern_items = list(self._verify_pattern.items())
        for i in range(len(pattern_items)):
            json_pair = json_items[i]
            pattern_pair = pattern_items[i]
            if json_pair[0] != pattern_pair[0]:
                return False, f"bad name of key: is '{json_pair[0]}', must be '{pattern_pair[0]}'"
            if not isinstance(json_pair[1], pattern_pair[1]):
                return False, f"bad type of value in key '{json_pair[0]}': is '{type(json_pair[1])}', must be '{type(pattern_pair[1])}'"
        return True, None
