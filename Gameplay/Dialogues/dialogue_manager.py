import enum

from Gameplay.Quests.quest_manager import QuestManager
from Helpers.json_loader import JsonLoader


class Dialog:
    def __init__(self):
        self.temp_dict_ans = {}
        self._active_dialog = None
        self.phrases = []
        self.q = {}
        self.phrases = []
    # def get_next_phrases(self, answer_id: str):
    #     # QuestManager.instance.set_quest_variable('some_variable', True)
    #     for phrase in self.phrases:
    #         print(self.phrases)
    #         if phrase['id'] == answer_id:
    #             self._phrase_choice = phrase
    #     self._available_phrases = self.phrases
    #     self.temp_dict_ans = []
    #     for phrase in self._phrase_choice['phrases']:
    #         self.temp_dict_ans.append(phrase['phrase_text'])
    #     self.my_phrase = self._phrase_choice["phrase_text"]
    #     self.interlocutor_phrase = self._phrase_choice["answer_text"]
    #     print(r"\я кажу " + self.my_phrase + " " + self._phrase_choice['id'])
    #     print("|мені відповідають " + self.interlocutor_phrase)
    #     print("/варіанти відповіді ", self.temp_dict_ans)
    #     print()

    def get_next_phrases(self):
        # QuestManager.instance.set_quest_variable('some_variable', True)
        for next_phrases in self.phrases:
            self.temp_dict_ans[next_phrases['id']] = next_phrases['phrase_text']
            self.q[next_phrases['id']] = next_phrases['phrase_text']
        # print(self.q)
            # self.temp_dict_ans(next_phrases['phrase_text'])
        # print(self.temp_dict_ans)

    def choose_answer(self, choice_id: str):
        second_dialog = Dialog()
        q = {}
        for chosen_phrase in self._active_dialog.__dict__['phrases']:
            if chosen_phrase["id"] == choice_id:
                q = chosen_phrase
                break
        second_dialog.__dict__.update(q)
        self.phrases = second_dialog.phrases
        self.__dict__.update(self._active_dialog.__dict__)
        second_dialog.get_next_phrases()
        self._active_dialog = second_dialog
        self.temp_dict_ans = second_dialog.temp_dict_ans


class DialogManager(JsonLoader):
    instance = None

    def __init__(self):
        dialog_json_verify_pattern = {"id": str, "interlocutor": str, "activator": list, "phrases": list}
        super().__init__('Static/Dialogs/', dialog_json_verify_pattern)
        self._dialogs_dictionary = {}
        self._active_dialog = None
        self._load_dialogs_from_json()

    def _load_dialogs_from_json(self):
        for dialog_dict in self.loaded_element_list:
            dialog_object = Dialog()
            dialog_object.__dict__.update(dialog_dict)
            self._dialogs_dictionary[dialog_dict['interlocutor']] = dialog_object

    def start_dialog(self, interlocutor: str) -> Dialog:
        dialog = self.get_dialog_by_interlocutor(interlocutor)
        temp_list = []
        [temp_list.append(phrase) for phrase in dialog.phrases]
        dialog.phrases = temp_list
        dialog._active_dialog = dialog
        dialog.get_next_phrases()
        return dialog

    def get_dialog_by_interlocutor(self, interlocutor):
        return self._dialogs_dictionary[interlocutor]
