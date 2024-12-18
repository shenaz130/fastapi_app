from calculations import add


def test_add():
    print("test is success!!!")
    sum = add (5, 6)
    assert sum == 11
    #assert True