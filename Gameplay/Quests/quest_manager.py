import enum

from Helpers.json_loader import JsonLoader


class QuestStatus(enum.Enum):
    Inactive = 0
    Active = 1
    Completed = 2
    Failed = 3


class QuestStage:
    def __init__(self):
        self.activator = None

    def update(self):
        return QuestManager.instance.get_quest_variable(self.activator) is True


class Quest:
    def __init__(self):
        self.status = QuestStatus.Inactive
        self.activator = None
        self.stages = []
        self._current_stage = None
        self._current_stage_index = -1

    def select_next_stage(self):
        self._current_stage_index += 1
        if self._current_stage_index >= len(self.stages):
            self.status = QuestStatus.Completed
            return
        self._current_stage = self.stages[self._current_stage_index]

    def update(self):
        if self._current_stage.update() is True:
            self.select_next_stage()


class QuestManager(JsonLoader):
    instance: 'QuestManager' = None
    quest_json_verify_pattern: dict = {"id": str, "variables": list, "activator": str, "required_level": int,
                                       "stages": list}

    def __init__(self):
        super().__init__('Static/Quests/', verify_pattern=self.__class__.quest_json_verify_pattern)
        self.__class__.instance = self
        # this list contains active user quests, which the manager should update every frame
        self._active_quest_list = []
        # this list contains completed or failed quest ids
        self._completed_quest_list = []
        # contains global quests' variables (variable name is a key, value is some object(preferred boolean))
        self._quest_variables = {}
        # contains the information about by which variable some quest or quest stage should be activated
        # variable is a key, quest/quest stage is a value
        self._quest_variable_functions = {}
        self._quests_dictionary = {}
        # loads quests data from json files
        self._load_quests_from_json()

    def _load_quests_from_json(self):
        for quest_dict in self.loaded_element_list:
            quest_object = Quest()
            quest_object.__dict__.update(quest_dict)
            self._quests_dictionary[quest_dict['id']] = quest_object

            self.add_quest_variables_from_list(quest_dict['variables'])
            self._quest_variable_functions[quest_dict['activator']] = quest_dict['id']
            quest_object.stages = []
            for stage_dict in quest_dict['stages']:
                quest_stage = QuestStage()
                quest_stage.__dict__.update(stage_dict)
                quest_object.stages.append(quest_stage)
                self._quest_variables[quest_stage.activator] = False

    def get_quest_by_id(self, quest_id: str):
        return self._quests_dictionary[quest_id]

    def start_quest(self, quest_id: str):
        quest = self.get_quest_by_id(quest_id)
        quest.select_next_stage()
        quest.status = QuestStatus.Active
        self._active_quest_list.append(quest)

    def update(self):
        completed_quest_list = []
        for quest in self._active_quest_list:
            quest.update()
            if quest.status == QuestStatus.Completed:
                completed_quest_list.append(quest)

        for quest in completed_quest_list:
            self._active_quest_list.remove(quest)
            self._completed_quest_list.append(quest)

    def set_quest_variable(self, key: str, value):
        self._quest_variables[key] = value
        if key in self._quest_variable_functions.keys():
            self.start_quest(self._quest_variable_functions[key])

    def get_quest_variable(self, key: str):
        return self._quest_variables[key]

    def add_quest_variables_from_list(self, variable_list: list):
        for variable in variable_list:
            self._quest_variables[variable] = False
