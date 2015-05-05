#
#   Parser, has Grammar
#

from Grammar import *
import re
from builtins import Exception

class Parser(object):
    def __init__(self, file):
        self.__m_file = file
        self.__m_Grammar = Grammar()
        self.__m_tokens = []
        self.__m_cursor = 0

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

    
    def __str__(self):
        rep = ""
        for token in self.__m_tokens:
            rep += " {} \n".format(token)
        return rep

    #check if we have more tokens in the raw token list
    @property
    def hasMoreTokens(self):
        if self.__m_cursor < len(self.__m_tokens):
            return True
        return False

    def run(self):
        #self.testGrammar() #Tests for grammar
        self.tokenize()
        print(self.__str__())
        while self.hasMoreTokens:
            try:
                self.isProgram()
            except Exception as custom:
                print(custom)
                break
            
            currentLine = self.__m_tokens[self.__m_cursor]
            #break current line in tokens
            for token in currentLine:
                print(token)
            
            self.__m_cursor += 1
        print("File is valid, congrats you can write good sintax! Yay?")

    #check if program
    def isProgram(self):
        if self.__m_tokens[-1] == "END" and self.__m_tokens[0] == "BEGIN":
            return
        elif self.__m_tokens[0][0] != "BEGIN":
            raise Exception(self.error(1, "BEGIN", self.__m_tokens[0][0]))
        elif self.__m_tokens[-1][0] != "END":
            raise Exception(self.error(len(self.__m_tokens), "END", self.__m_tokens[-1][0]))
    
    def error(self, lineNr, expected, got):
        return "Error at line #{}: expected {} not {}".format(lineNr, expected, got)
    #tests
    def testGrammar(self):
        print(self.__m_Grammar.isIdentifier("variable"))
        print(self.__m_Grammar.isIdentifier("1variable"))
        print(self.__m_Grammar.isIntegerConstant("500"))
        print(self.__m_Grammar.isIntegerConstant("b500"))
        print(self.__m_Grammar.isProgramKw("BEGIN"))
        print(self.__m_Grammar.isProgramKw("BLA"))
        print(self.__m_Grammar.isStringConstant("\"String bla bla\""))
        print(self.__m_Grammar.isStringConstant("String bla bla"))
        print(self.__m_Grammar.isSymbol("("))
        print(self.__m_Grammar.isSymbol("$"))
        print(self.__m_Grammar.isOp("+"))
        print(self.__m_Grammar.isOp("/"))
        print(self.__m_Grammar.isStatement(":="))
        print(self.__m_Grammar.isStatement("="))
