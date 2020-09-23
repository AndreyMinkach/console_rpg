import enum
from Gameplay.Quests.quest_loader import QuestLoader


class QuestStatus(enum.Enum):
    Inactive = 0
    Active = 1
    Completed = 2
    Failed = 3


class QuestManager:
    instance = None

    def __int__(self):
        self.__class__.instance = self
        self._quest_list = []
        # contains global quests' variables (variable name is a key, value is some object(preferred boolean))
        self._quest_variables = {}
        # contains the information about by which variable some quest or quest stage should be activated
        # variable is a key, quest/quest stage is a value
        self._quest_variables_function = {}

    def start_quest(self, quest_id: str):
        quest = QuestLoader.instance.get_quest_by_id(quest_id)
        quest.select_next_stage()
        quest.status = QuestStatus.Active

    def set_quest_variable(self, key: str,  value):
        self._quest_variables[key] = value
