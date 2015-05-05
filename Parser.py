#
#   Parser, has Grammar
#

from Grammar import *


class Parser(object):
    def __init__(self, file):
        self.__m_file = file
        self.__m_Grammar = Grammar()

    def run(self):
        running = True
        while (running):
            print("haoles")
            running = False

    #tests
    def testGrammar(self):
        print(self.__m_Grammar.isIdentifier("variable"))
        print(self.__m_Grammar.isIntegerConstant("500"))
        print(self.__m_Grammar.isProgramKw("BEGIN"))
        print(self.__m_Grammar.isStringConstant("\"String bla bla\""))
        print(self.__m_Grammar.isSymbol("("))
        print(self.__m_Grammar.isOp("+"))
        print(self.__m_Grammar.isStatement(":="))
