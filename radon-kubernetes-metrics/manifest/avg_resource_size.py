class AvgResourceSize:

    def __init__(self, script):
        self.script = script

    def count(self):
        resources = self.script.split('---')

        sizes = [
            len(r.strip().splitlines())
            for r in resources if r.strip()
        ]

        if not sizes:
            return 0

        return int(sum(sizes) / len(sizes))