import random

import enum

from Gameplay.Quests.quest_manager import QuestManager
from Helpers.json_loader import JsonLoader


def check_activators(list_of_activators: list):
    if len(list_of_activators) == 0:
        return True
    for activator in list_of_activators:
        if not QuestManager.instance.get_quest_variable(activator):
            return False
    return True


class Dialog:
    def __init__(self):
        self.list_of_phrases = []
        self.dict_of_answers = {}
        self.interlocutor_answer = ''
        self.first_phrases = None
        self.first_dialogs = None

    def chose_phrase_by_id(self, phrase_id: str = ''):
        phrase_text = {}
        for phrase in self.list_of_phrases:
            if phrase['id'] == phrase_id and check_activators(phrase['activator']):
                self.interlocutor_answer = phrase['answer_text']
                self.list_of_phrases = phrase['phrases']
                self.activate_variables(phrase['variables_to_set'])
                for future_phrase in phrase['phrases']:
                    if check_activators(future_phrase['activator']):
                        phrase_text[future_phrase['id']] = future_phrase['phrase_text']

            elif phrase_id == '' and check_activators(phrase['activator']):
                phrase_text[phrase['id']] = phrase['phrase_text']
                self.first_dialogs = self.list_of_phrases

        if phrase_text == {}:
            phrase_text = self.first_phrases
            self.list_of_phrases = self.first_dialogs
            phrase_text['goodbye'] = self.get_random_bye_phrase()

        if phrase_id == '':
            phrase_text['goodbye'] = self.get_random_bye_phrase()
            self.first_phrases = phrase_text
        self.dict_of_answers = phrase_text

    def activate_variables(self, variables: dict):
        for variable, value in variables.items():
            QuestManager.instance.set_quest_variable(variable, value)

    def get_random_bye_phrase(self):
        list_of_bye_phrases = ['goodbye', 'прощавай', 'попутного вітру', 'давай до свіданія']
        return random.choice(list_of_bye_phrases)


class DialogManager(JsonLoader):
    _instance: 'DialogManager' = None

    def __init__(self):
        self.__class__._instance = self
        dialog_json_verify_pattern = {"id": str, "interlocutor": str, "activator": list, "phrases": list}
        super().__init__('Static/Dialogs/', dialog_json_verify_pattern)
        self._dialogs_dictionary = {}
        self._active_dialog = None
        self._load_dialogs_from_json()

    def _load_dialogs_from_json(self):
        for dialog_dict in self.loaded_element_list:
            if dialog_dict['interlocutor'] in self._dialogs_dictionary.keys():
                self._dialogs_dictionary[dialog_dict['interlocutor']].append(dialog_dict)
            else:
                self._dialogs_dictionary[dialog_dict['interlocutor']] = [dialog_dict]

    @classmethod
    def get_dialog_by_interlocutor(cls, interlocutor: str) -> Dialog:
        dialog_obj = Dialog()
        for dialog in cls._instance._dialogs_dictionary[interlocutor]:
            if check_activators(dialog['activator']):
                dialog_obj.list_of_phrases += dialog['phrases']
        dialog_obj.interlocutor = interlocutor
        dialog_obj.first_phrases = dialog_obj.list_of_phrases
        cls._instance._active_dialog = dialog_obj
        return dialog_obj
