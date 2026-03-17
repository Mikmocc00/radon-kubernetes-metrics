class LinesCode:

    def __init__(self, script):
        self.script = script

    def count(self):

        lines = self.script.splitlines()

        code_lines = [
            l for l in lines
            if l.strip() != "" and not l.strip().startswith("#") and not l.strip().startswith("//")
        ]

        return len(code_lines)