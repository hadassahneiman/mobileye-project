class Results:
    def __init__(self):
        self.results = []

    def get_prev_tfls(self, index):
        return self.results[index]['part2']['candidates']

    def add_result(self, res):
        self.results.append(res)
