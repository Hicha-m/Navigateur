class File:
    def __init__(self):
        self.file = []

    def nouvelle_file(self):
        self.file = []

    def enfiler(self, x):
        self.file.append(x)
        return x

    def defiler(self):
        if not self.file_vide():
            return self.file.pop(0)

    def file_vide(self):
        return self.file == []

    def test_file(self, x):
        self.nouvelle_file(self)
        self.enfiler(self, x)
        self.defiler(self)
        self.file_vide(self)


if __name__ == "__main__":
    a = [1, 2, 3, 4, 5, 6]

    f = File()

    f.nouvelle_file()
    f.enfiler(1)
    print(f.file_vide())
    print(f.file)

 
