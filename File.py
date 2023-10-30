class File:
    def __init__(self):
        self.file = []

    def nouvelle_file(self):
        self.file = []

    def enfiler(self, x):
        return self.file.append(x)

    def defiler(self):
        return self.file.pop()

    def file_vide(self):
        return self.file == []

    def test_file(self, x):
        self.nouvelle_file(self, f)
        self.enfiler(self, f, x)
        self.defiler(self, f)
        self.file_vide(self, f)


if __name__ == "__main__":
    a = [1, 2, 3, 4, 5, 6]

    f = File()

    f.nouvelle_file()

    for i in range(len(a)):
        a.enfiler(f, i)

    print(f)
