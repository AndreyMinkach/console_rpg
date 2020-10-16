import random

import enum

from Gameplay.Quests.quest_manager import QuestManager
from Helpers.json_loader import JsonLoader


def all_activators_true(list_of_activators: list):
    if len(list_of_activators) == 0:
        return True
    for activator in list_of_activators:
        if not QuestManager.instance.get_quest_variable(activator):
            print(QuestManager.instance.get_quest_variable(activator), activator)
            return False
    return True


def activate_variables(variables: dict):
    for variable, value in variables.items():
        QuestManager.instance.set_quest_variable(variable, value)


def random_bye_phrase():
    list_of_bye_phrases = ['goodbye', 'прощавай', 'попутного вітру', 'давай до свіданія']
    return random.choice(list_of_bye_phrases)

class Dialog:
    def __init__(self):
        self.phrases = []
        self.available_phrases = []
        self.phrase_text = {}
        self.phrase_answer = ''
        self.first_phrases = None
        self.first_dialogs = None

    def chose_phrase_by_id(self, phrase_id: str = ''):
        phrase_text = {}

        for phrase in self.phrases:
            if phrase['id'] == phrase_id and all_activators_true(phrase['activator']):
                self.phrases = phrase['phrases']
                activate_variables(phrase['variables_to_set'])
                for future_phrase in phrase['phrases']:
                    if all_activators_true(future_phrase['activator']):
                        phrase_text[future_phrase['id']] = future_phrase['phrase_text']
                        self.phrase_answer = phrase['answer_text']

            elif phrase_id == '' and all_activators_true(phrase['activator']):
                phrase_text[phrase['id']] = phrase['phrase_text']
                self.first_dialogs = self.phrases

        if phrase_text == {}:
            phrase_text = self.first_phrases
            self.phrases = self.first_dialogs
            phrase_text['goodbye'] = random_bye_phrase()

        if phrase_id == '':
            phrase_text['goodbye'] = random_bye_phrase()
            self.first_phrases = phrase_text
        self.phrase_text = phrase_text


class DialogManager(JsonLoader):
    instance: 'DialogManager' = None

    def __init__(self):
        self.__class__.instance = self
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

    def get_dialog_by_interlocutor(self, interlocutor: str) -> Dialog:
        dialog_obj = Dialog()
        for dialog in self._dialogs_dictionary[interlocutor]:
            if all_activators_true(dialog['activator']):
                dialog_obj.phrases += dialog['phrases']
        dialog_obj.interlocutor = interlocutor
        dialog_obj.first_phrases = dialog_obj.phrases
        self._active_dialog = dialog_obj
        return dialog_obj
