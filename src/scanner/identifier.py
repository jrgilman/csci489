import string

class Identifier:

    alphabet = list(string.ascii_lowercase)
    numbers = range(0,9)

    def __init__(self, identifier_string):
        self.name = None
        self.value = None

        self.setName(identifier_string)

    def setName(self, identifier_string):
        for char in identifier_string:
            if (char in self.alphabet) and (self.name == None):
                self.name = char
            elif (char in self.alphabet):
                self.name += char
            elif (int(char) in self.numbers) and (self.name != None):
                self.name += char
            else:
                # this is a failure, should throw exception
                self.name = None
                break
