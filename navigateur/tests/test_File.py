""""ce programme contient les tests des méthodes contenus dans le fichier "File.py""" ""

from navigateur.classes.File import File


def test_nouvelle_file():
    f = File()
    f.nouvelle_file()
    assert f.file == []


def test_enfiler():
    f = File()
    f.nouvelle_file()
    f.enfiler(5)
    assert f.file == [5]
    f.enfiler(1)
    assert f.file == [5, 1]


def test_defiler():
    f = File()
    f.nouvelle_file()
    assert f.defiler() == None
    assert f.file == []
    f.enfiler(5)
    f.enfiler(1)
    assert f.defiler() == 5
    assert f.file == [1]
    assert f.defiler() == 1
    assert f.file == []


def test_file_vide():
    f = File()
    f.nouvelle_file()
    assert f.file_vide() == True
    f.enfiler(5)
    f.enfiler(1)
    f.defiler()
    assert f.file_vide() == False
    f.defiler()
    assert f.file_vide() == True
