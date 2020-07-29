from gui.Quest import GUI as Quest

DESC = \
"""Ankandora, a land full of adventures awaits you. Many have traveld the wide fields and step mountains, setteled in one of the cities and
villages or fell, slain by the foes lurking in the darkest corners. Everyday new adventurers, scientists and tricksters come along and try their luck.

Now follow the paths and fight against the foes standing in your way to save the land or clame it as yours and become the new king."""
CONTROL = \
"""If it's your turn, click the dice button or hit 'D'
Select any field that you could reach with your points and select it.
Finally, if you're done. Hit the Button in the bottom center."""

class QuestHandler(Quest):
    def __init__(self):
        Quest.__init__(self)
        self.btnClose["command"] = self.hide

        self.lblQuestDesc["text_wordwrap"] = 23
        self.lblControlDesc["text_wordwrap"] = 25

        self.lblQuestDesc["text"] = DESC
        self.lblControlDesc["text"] = CONTROL

        self.hide()
