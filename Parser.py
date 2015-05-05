#
#   Parser, has Grammar
#

from Grammar import *
import re

class Parser(object):
    def __init__(self, file):
        self.__m_file = file
        self.__m_Grammar = Grammar()
        self.__m_tokens = []

    def removeComments(self, string):
        #tested on http://pythex.org/
        comment = (re.compile('//[^\n]*|/\*[^\n]*|\*[^\n]*', re.MULTILINE|re.DOTALL)).sub("", string)
        return comment

    def tokenize(self):
        #my reg exp
        symbols = '[' + re.escape(''.join(self.__m_Grammar.getLex()['symbol'])) + ']'
        keywords = '|'.join(self.__m_Grammar.getLex()['keyword'])
        statements = '|'.join(self.__m_Grammar.getLex()['statement'])
        program = '|'.join(self.__m_Grammar.getLex()['program'])
        op = '|'.join(self.__m_Grammar.getLex()['op'])
        nkeywords = '[\w\-]+'
        strings = r'"[^"]*"'
        numbers = '\d+'


        #get them all together
        match = re.compile(symbols + "|" + keywords + "|" + strings + "|" +
                           nkeywords + "|" + numbers + "|" + program + "|" + statements)

        for line in self.__m_file:
            #remove out comments
            line = self.removeComments(line)
            #remove newlines
            line = line.strip()
            #remove empty lines
            if (line):
                self.__m_tokens.append(match.findall(line))
        #2d array to 1d array
        self.__m_tokens = [x for sublist in self.__m_tokens for x in sublist]
    
    def __str__(self):
        rep = ""
        for token in self.__m_tokens:
            rep += " {} \n".format(token)
        return rep

    def run(self):
        self.tokenize()
        print(self.__str__())


    #tests
    def testGrammar(self):
        print(self.__m_Grammar.isIdentifier("variable"))
        print(self.__m_Grammar.isIntegerConstant("500"))
        print(self.__m_Grammar.isProgramKw("BEGIN"))
        print(self.__m_Grammar.isStringConstant("\"String bla bla\""))
        print(self.__m_Grammar.isSymbol("("))
        print(self.__m_Grammar.isOp("+"))
        print(self.__m_Grammar.isStatement(":="))
