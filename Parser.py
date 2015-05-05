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
        #cursor starts at 0, line at 1
        self.__m_line = self.__m_cursor + 1

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
        valid = True
        while self.hasMoreTokens:
            currentLine = self.__m_tokens[self.__m_cursor]
            try:
                #check for BEGIN; then END
                self.isProgram()
                #check if valid read
                if (currentLine[0].lower() == "read"):
                    self.isValidRead(currentLine)
                #check if it starts with an identifier
                elif (self.__m_Grammar.isIdentifier(currentLine[0])):
                      #check if line is a statement
                      self.isValidStatement(currentLine)

            except Exception as custom:
                print(custom)
                valid = False
                break
                
            self.__m_cursor += 1
         
        if (valid): print("File is valid, congrats you can write good sintax! Yay?")

   
    def isValidStatement(self, line):
        #we know if started with an identifier
        count = 0
        for token in line:
            #is the next token :=
            if count == 1:
                if token != ":=":
                    raise Exception(self.errorExpectedToken(self.__m_line, ":=", token))
            count += 1

    def isValidRead(self, line):
        #check if it is a valid statement
        self.isTerminated(line)
        count = 0
        for token in line:
            if (count == 1 and token != "("):
                raise Exception(self.errorExpectedToken(self.__m_line, "(", token))
            if (count == len(line)-2 and token != ")"):
                raise Exception(self.errorExpectedToken(self.__m_line, ")", token))
            count += 1
    
    def isTerminated(self, line):
        if line[-1] != ";":
            raise Exception(self.errorExpectedToken(self.__m_line, ";", line[-1]))

    #count left P and right P; at the end raise exception if !=
    def checkParentheses(self, line):
        leftP = 0
        rightP = 0
        for token in line:
            if token == '(':
                leftP += 1
            elif token == ')':
                rightP += 1
        if leftP == rightP:
            return
        #if here we have an error
        missing = "right"
        if leftP < rightP:
            missing = "left"

        raise Exception("Missing a {} parentheses on line {}".format(missing, self.__m_line))

    #check if program
    def isProgram(self):
        if self.__m_tokens[-1][0].lower() == "end" and self.__m_tokens[0][0].lower() == "begin":
            return
        elif self.__m_tokens[0][0].lower() != "BEGIN":
            raise Exception(self.errorExpectedToken(1, "BEGIN", self.__m_tokens[0][0]))
        elif self.__m_tokens[-1][0].lower() != "end":
            raise Exception(self.errorExpectedToken(len(self.__m_tokens)+1, "END", self.__m_tokens[-1][0]))
    
    def errorExpectedToken(self, lineNr, expected, got):
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
