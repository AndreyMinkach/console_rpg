from pyglet.graphics import OrderedGroup

from Gameplay.Dialogues.dialogue_manager import DialogManager, Dialog
from Helpers.color_helper import ColorHelper
from UI.ui_base import UIBase
from Helpers.location_helper import Vector2
from UI.ui_scrollable_container import ScrollableContainer
from UI.ui_text import UIText


class UIDialogue(UIBase):
    def __init__(self, position: Vector2, size: Vector2, name: str):
        super().__init__(position, size)

        dialogue_manager = DialogManager()
        self.dialog = dialogue_manager.start_dialog(name)
        self._child_group = OrderedGroup(self.group.order + 0.2)

        self.dialog_container = ScrollableContainer(position, size)
        self.dialog_container.children_margin = Vector2(5, 5)
        self.dialog_container.color = ColorHelper.LIGHT_BLUE[:3]
        self.dialog_container.group = self._child_group
        self.show_next_phrases(self.dialog.temp_dict_ans.items())
        # for answer_id, answer in self.dialog.temp_dict_ans.items():
        #     ui_text = UIText(answer, Vector2.zero, Vector2(400, 22))
        #     ui_text.custom_data = answer_id
        #     self.dialog_container.add_child(ui_text)
        #     ui_text.on_click_up = lambda o, b: self.choose_phrase(o)
        #     ui_text.group = self._child_group

    def choose_phrase(self, o: UIBase):
        self.dialog.choose_answer(o.custom_data)
        self.show_next_phrases(self.dialog.temp_dict_ans.items())

    def show_next_phrases(self, dict_ans):
        self.dialog_container.delete_children()
        for answer_id, answer in dict_ans:
            ui_text = UIText(answer, Vector2.zero, Vector2(400, 22))
            ui_text.custom_data = answer_id
            ui_text.group = self._child_group
            self.dialog_container.add_child(ui_text)
            ui_text.on_click_up = lambda o, b: self.choose_phrase(o)

