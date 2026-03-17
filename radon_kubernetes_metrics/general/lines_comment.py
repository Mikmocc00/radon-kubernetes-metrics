class LinesComment:

    def __init__(self, script):
        self.script = script

    def count(self):

        lines = self.script.splitlines()

        comments = [
            l for l in lines
            if l.strip().startswith("#")
               or l.strip().startswith("//")
        ]

        return len(comments)