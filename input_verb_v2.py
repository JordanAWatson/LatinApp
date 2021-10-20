from dataclasses import dataclass

@dataclass
class Verb:
    pass



def dictionary_test_cases():

    # test 1: class construction
    try:
        v = Verb()
        print("Test 1 pass")
    except:
        print("Test 1 fail")


    # test 2: connect to database
    try:
        v.connect()
        print("Test 2 pass")
    except:
        print("Test 2 fail")

    # test 3: find if verb exists in dictionary
    try:
        if Verb.dictionary_find("a", "1st"):
            raise Error
        else:
            print("Test 3 pass")

    except:
        print("Test 3 fail")


    # test 4: add verb to dictionary
    try:
        v.dictionary_add("a", "1st")
        v.dictionary_add("a", "2nd")
        print("Test 4 pass")
    except:
        print("Test 4 fail")

    # test 5: find added verb in dictionary
    try:
        if not Verb.dictionary_find("a", "1st"):
            raise Error
        else:
            print("Test 5 pass")
    except:
        print("Test 5 fail")


    # test 6: 



dictionary_test_cases()
