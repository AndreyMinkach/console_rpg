from pyglet.graphics import OrderedGroup

from Gameplay.Dialogues.dialogue_manager import DialogManager, Dialog
from Gameplay.Quests.quest_manager import QuestManager
from Helpers.color_helper import ColorHelper
from UI.ui_base import UIBase
from Helpers.location_helper import Vector2
from UI.ui_scrollable_container import ScrollableContainer
from UI.ui_text import UIText
import gc


class UIDialog(UIBase):
    def __init__(self, position: Vector2, size: Vector2, name: str):
        super().__init__(position, size)
        self._child_group = OrderedGroup(self.group.order + 1)

        self.dialog_container = ScrollableContainer(position, size)
        self.dialog_container.children_margin = Vector2(5, 5)
        self.dialog_container.color = ColorHelper.LIGHT_BLUE[:3]
        self.dialog_container.group = self._child_group

        self.dialog = DialogManager.get_dialog_by_interlocutor(name)
        self.dialog.chose_phrase_by_id()
        self.show_next_phrases(self.dialog.dict_of_answers)

    def show_next_phrases(self, dict_ans: dict):
        self.dialog_container.delete_children()
        for answer_id, answer in dict_ans.items():
            ui_text = UIText(answer, Vector2(self.position.x + self.dialog_container.children_margin.x,
                                             self.position.y + self.size.x - self.dialog_container.children_margin.y),
                             Vector2(self.dialog_container.width - self.dialog_container.children_margin.x * 2, 22))
            ui_text.custom_data = answer_id
            ui_text.group = self._child_group
            self.dialog_container.add_child(ui_text)
            ui_text.on_click_down = lambda o, b: self.show_interlocutor_phrase(o.custom_data)

    def show_interlocutor_phrase(self, answer_id: str):
        if answer_id == 'goodbye':
            self.set_enabled(False)
            self.dialog_container.set_enabled(False)
            return
        self.dialog.chose_phrase_by_id(answer_id)
        self.dialog_container.delete_children()
        ui_text = UIText(self.dialog.interlocutor_answer, Vector2(self.position.x + self.dialog_container.children_margin.x,
                                                                  self.position.y + self.size.x - self.dialog_container.children_margin.y),
                         Vector2(self.dialog_container.width - self.dialog_container.children_margin.x * 2, 22),
                         document_style=dict(color=ColorHelper.GREEN))
        ui_text.group = self._child_group
        self.dialog_container.add_child(ui_text)
        ui_text.on_click_down = lambda o, b: self.show_next_phrases(self.dialog.dict_of_answers)
