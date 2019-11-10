from flask import render_template


class Block:
    "Base class for all question blocks. Custom questions are implemented here"

    def __init__(self, id_, question, type="base", content=None):
        self.id_ = id_
        self.type = type
        self.question = question

        if content == None:
            self.content = render_template(
                "Blocks/base.html", question=self.question)


class StringBlock(Block):
    "Question block that returns a string"

    def __init__(self, id_, question, default=""):
        super().__init__(id_, question, "string")

        self.content = render_template(
            "Blocks/string.html", question=question, default=default, name=id_)


class IntBlock(Block):
    "Question block that returns an integer, taken directly from user in a textbox"

    def __init__(self, id_,  question, default=0, min=0, max=9999):
        super().__init__(id_, question, "int")

        self.content = render_template("Blocks/int.html", question=question,
                                       default=default, min=min, max=max, name=id_)


class TallyIntBlock(Block):
    "Question block that returns an integer, taken from a tally with plus and minus signs."

    def __init__(self, id_, question, default=0, min=0, max=100):
        super().__init__(id_, question, "tallyInt")

        self.content = render_template(
            "Blocks/tallyInt.html", question=question, id=id_, default=default, name=id_)


class CheckBoxBlock(Block):
    "Question block that returns a boolean, taken from a checkbox"

    def __init__(self, id_, question):
        super().__init__(id, question, "checkBox")

        self.content = render_template(
            "Blocks/checkBox.html", question=question, name=id_)


class RadioButtonBlock(Block):
    "Radio button block that returns the property that was clicked"

    def __init__(self, id_, question, *choices):
        super().__init__(id_, question, "radioButton")

        self.content = render_template(
            "Blocks/radioButton.html", question=question, id=id_, args=choices, name=id_)


class HeaderBlock(Block):
    "Header block to act as a (section) title"

    def __init__(self, title):
        super().__init__(-1, None, "header")

        self.title = title

        self.content = render_template("Blocks/header.html", content=title)


class SpaceBlock(Block):
    "Space block to add space(measured in px) between sections"

    def __init__(self, size):
        super().__init__(-1, None, "space")

        self.size = size

        self.content = f'<div style="height:{size}px"></div>'
