import enum

from Gameplay.Quests.quest_manager import QuestManager
from Helpers.json_loader import JsonLoader


def all_activators_true(list_of_activators: list):
    if len(list_of_activators) == 0:
        return True
    for activator in list_of_activators:
        if not activator:
            return False
    return True


class Dialog:
    def __init__(self):
        self.phrases = []
        self.available_dialogs = []
        self.available_phrases = []

    def chose_phrase_by_id(self, phrase_id: str):
        available_phrases = {}
        available_dialogs = []
        for dialog in self.available_dialogs:
            if dialog['id'] == phrase_id and all_activators_true(dialog['activator']):
                for phrase in dialog['phrases']:
                    if all_activators_true(phrase['activator']):
                        available_phrases[phrase['id']] = phrase['phrase_text']
                        available_dialogs = dialog['phrases']

        self.available_phrases = available_phrases
        self.available_dialogs = available_dialogs

    def start_dialog(self):
        available_phrases = {}
        available_dialogs = []
        for phrase in self.available_dialogs:
            for sub_phrase in phrase['phrases']:
                if all_activators_true(sub_phrase['activator']):
                    available_phrases[sub_phrase['id']] = sub_phrase['phrase_text']
                    available_dialogs = phrase['phrases']
        self.available_phrases = available_phrases
        self.available_dialogs = available_dialogs


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
        available_dialogs = []
        for dialog in self._dialogs_dictionary[interlocutor]:
            if all_activators_true(dialog['activator']):
                available_dialogs.append(dialog)
        dialog = Dialog()
        dialog.available_dialogs = available_dialogs
        self._active_dialog = dialog
        return dialog
