from QAPair import QAPair


class Topic:
    def __init__(self, name):
        self.name = name
        self.questions = []

    def add_questions(self, path_to_file):
        with open(path_to_file) as f:
            lines = f.readlines()
            for ind in range(0, len(lines), 2):
                question = lines[ind]
                answer = lines[ind + 1]
                tmp_qapair = QAPair(question=question, answer=answer)
                self.questions.append(tmp_qapair)
