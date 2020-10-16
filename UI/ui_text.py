from pyglet import font
from pyglet.font.ttf import TruetypeInfo
from pyglet.text.document import FormattedDocument
from pyglet.text.layout import TextLayout
from UI.ui_base import *


def load_font(path):
    p = TruetypeInfo(path)
    p.close()
    font.add_file(path)


load_font('Static/Fonts/DisposableDroidBB.ttf')


class UIText(UIBase):
    def __init__(self, caption: str, position: Vector2 = Vector2.zero, size: Vector2 = Vector2.one,
                 document_style=None, font_name: str = 'DisposableDroid BB', font_size: int = 20,
                 tint_color: (int, int, int, int) = ColorHelper.WHITE):
        super().__init__(position, size)
        document_style = {} if document_style is None else document_style
        document_style.update(dict(font_name=font_name, font_size=font_size))

        self._caption = caption
        self._document = FormattedDocument(caption)
        self.update_document_style(document_style)
        self._text_layout = TextLayout(self._document, width=size.x, height=size.y, batch=self.batch,
                                       group=OrderedGroup(self.group.order + 1.1), wrap_lines=True, multiline=True)
        self._text_layout.content_valign = 'center'
        self.position = position
        self.color = tint_color

    def set_text(self, text: str):
        self.my_label.text = text
        self.size.y = self.my_label.content_height
        self.my_label.height = self.my_label.content_height

    @property
    def caption(self) -> str:
        return self._caption

    @caption.setter
    def caption(self, value: str):
        self._caption = value
        self._document.text = value

    @UIBase.batch.setter
    def batch(self, value: Batch):
        UIBase.batch.fset(self, value)
        self._text_layout.batch = value

    @UIBase.group.setter
    def group(self, value: OrderedGroup):
        UIBase.group.fset(self, value)
        self._update_text_layout_groups(value)

    @UIBase.position.setter
    def position(self, value: Vector2):
        UIBase.position.fset(self, value)
        self._text_layout.x = value.x
        self._text_layout.y = value.y

    @UIBase.size.setter
    def size(self, value: Vector2):
        UIBase.size.fset(self, value)
        self._text_layout.width = value.x
        self._text_layout.height = value.y

    @UIBase.color.setter
    def color(self, value: (int, int, int, int)):
        UIBase.color.fset(self, value[:3])
        self.opacity = value[3] if len(value) == 4 else 255

    def update_document_style(self, style: dict):
        if style is not None:
            self._document.set_style(0, len(self._caption), style)

    def _update_text_layout_groups(self, group: OrderedGroup):
        self._text_layout.begin_update()
        self._text_layout._init_groups(OrderedGroup(group.order + 1))
        self._text_layout.end_update()
