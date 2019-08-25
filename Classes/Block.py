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
            "Blocks/string.html", question=question, default=default)


class IntBlock(Block):
    "Question block that returns an integer, taken directly from user in a textbox"

    def __init__(self, id_,  question, default=0, min=0, max=9999):
        super().__init__(id_, question, "int")

        self.content = render_template("Blocks/int.html", question=question,
                                       default=default, min=min, max=max)


class TallyIntBlock(Block):
    "Question block that returns an integer, taken from a tally with plus and minus signs."

    def __init__(self, id_, question, default=0, min=0, max=100):
        super().__init__(id_, question, "tallyInt")

        self.content = render_template(
            "Blocks/tallyInt.html", question=question, id=id_, default=default)

class CheckBoxBlock(Block):
    "Question block that returns a boolean, taken from a checkbox"

    def __init__(self, id_, question):
        super().__init__(id, question, "checkBox")

        self.content = render_template("Blocks/checkBox.html", question=question)

class RadioButtonBlock(Block):
    "Radio button that returns the property that was clicked"

    def __init__(self, id_, question, *choices):
        super().__init__(id_, question, "radioButton")

        self.content = render_template("Blocks/radioButton.html", question=question, id=id_, args=choices)
