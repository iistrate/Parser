#
#   Parser, has Grammar
#

from Grammar import *


class Parser(object):
    def __init__(self, file):
        self.__m_file = file
        self.__m_Grammar = Grammar()

        self.testGrammar()

    def validate(self):
        running = True
        while (running):
            print("haoles")
            running = False


    def testGrammar(self):
        print(self.__m_Grammar.isIdentifier("test"))