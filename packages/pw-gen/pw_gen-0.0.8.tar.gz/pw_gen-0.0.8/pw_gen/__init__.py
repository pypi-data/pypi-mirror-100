import random
import secrets
import string

from random_word import RandomWords

class Simple():
    def __init__(self, length: int, *, characters = None):
        '''A simple password (less arguments compared to complex)'''
        self.length = length
        self.characters = characters
        self.output = ''

    def generate(self):
        '''
        Generates a password depending on the num_of_passwords and the arugments provided in the simple class
        '''
        characters = ''
        if self.characters is None:
            characters = string.ascii_letters + string.digits
        else:
            characters = self.characters

        del(self.output)
        self.output = ''
        password = ''
        for c in range(self.length):
            password += secrets.choice(characters)
        self.output += password
        return str(self.output)

    def result(self):
        return str(self.output.__str__())

class Complex(Simple):
    def __init__(self, length, string_method, *, include_numbers=True, include_special_chars=False):
        '''
        Creates a customisable password depending on length, string_method, numbers and special_chars
        '''
        characters = ''
        self.output = ''

        methods: dict = {
            "upper": string.ascii_uppercase,
            "lower": string.ascii_lowercase,
            "both": string.ascii_letters,
        }

        characters += methods[string_method]

        if include_numbers:
            characters += string.digits
        if include_special_chars:
            characters += string.punctuation

        super().__init__(length=length, characters=characters)

class Memorable(Simple):
    def __init__(self, include_numbers=True):
        '''A memorable password e.g HelloWorld123'''
        self.include_numbers = include_numbers
        self.output = ''

    def generate(self):
        '''Gets a list of random words'''
        r = RandomWords()
        words = r.get_random_words(minLength=5, maxLength=7)

        '''
        Generates the password containing 2 words and numbers if self.numbers == True
        '''

        del(self.output)
        self.output = ''
        password = ''
        two_words = ''
        for i in range(2):
            two_words += secrets.choice(words).title()
        password = two_words
        if self.include_numbers == True:
            for i in range(random.randint(3, 4)):
                password += secrets.choice(string.digits)
        self.output += password
        return self.output
