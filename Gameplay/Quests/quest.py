from Gameplay.Quests.quest_manager import QuestStatus


class Quest:
    def __init__(self):
        self.status = QuestStatus.Inactive
        self._start_condition = None
        self._stages = []
        self._current_stage = None
        self._current_stage_index = -1

    def select_next_stage(self):
        self._current_stage_index += 1
        if self._current_stage_index >= len(self._stages):
            self.status = QuestStatus.Completed


