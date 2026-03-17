class LinesBlank:

    def __init__(self, script):
        self.script = script

    def count(self):

        lines = self.script.splitlines()

        blank = [l for l in lines if l.strip() == ""]

        return len(blank)