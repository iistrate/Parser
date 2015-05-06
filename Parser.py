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
        comment = (re.compile('//[^\n]*|/*|\*[^\n]*', re.MULTILINE|re.DOTALL)).sub("", string)
        return comment

    def tokenize(self):
        #my reg exp
        symbols = '[' + re.escape(''.join(self.__m_Grammar.getLex()['symbol'])) + ']'
        keywords = '|'.join(self.__m_Grammar.getLex()['keyword'])
        statements = '|'.join(self.__m_Grammar.getLex()['statement'])
        program = '|'.join(self.__m_Grammar.getLex()['program'])
        nkeywords = '[\w\-]+'
        strings = r'"[^"]*"'
        numbers = '\d+'

        #get them all together
        match = re.compile(symbols + "|" + keywords + "|" + strings + "|" + nkeywords
                           + "|" + numbers + "|" + program + "|" + statements)

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
        count = 1
        for token in self.__m_tokens:
            rep += "{:3d}{} \n".format(count, token)
            count += 1
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
                self.checkUnknown(currentLine)
                #check if valid read
                if (currentLine[0].lower() == "read"):
                    self.isValidFunction(currentLine)
                #check if it starts with an identifier
                elif (self.__m_Grammar.isIdentifier(currentLine[0])):
                      #check if line is a statement
                      self.isValidStatement(currentLine)
                #check if valid write
                elif (currentLine[0].lower() == "write"):
                    self.isValidFunction(currentLine)
                #check if valid var
                elif self.__m_Grammar.isIntegerConstant(currentLine[0][0]):
                    raise Exception("Invalid var name at line {} got {}".format(self.__m_line, currentLine[0]))                        

            except Exception as customErr:
                print(customErr)
                valid = False
                break
                
            self.__m_cursor += 1
            self.updateLine()
         
        if (valid): print("File is valid, congrats you can write good sintax! Yay?")
    
    def checkUnknown(self, line):
        for token in line:
            if token in self.__m_Grammar.getLex()['unknown']:
                raise Exception("Unexpected token: {} on line {}, token not in language!".format(token, self.__m_line))

    def updateLine(self):
        self.__m_line = self.__m_cursor + 1

    def isValidStatement(self, line):
        self.isTerminated(line)
        #we know if started with an identifier
        count = 0
        for token in line:
            #is the next token :=
            if count == 1:
                if token != ":=":
                    raise Exception(self.errorExpectedToken(self.__m_line, ":=", token))
            #if + or -
            if token in self.__m_Grammar.getLex()['op']:
                #check before and after for identifiers or integer constants
                if (not self.__m_Grammar.isIdentifier(line[count-1])) and (not self.__m_Grammar.isIntegerConstant(line[count-1])):
                    raise Exception(self.errorExpectedToken(self.__m_line, "identifier or int on the left", line[count-1]))
                elif (not self.__m_Grammar.isIdentifier(line[count+1])) and (not self.__m_Grammar.isIntegerConstant(line[count+1])):
                    raise Exception(self.errorExpectedToken(self.__m_line, "identifier or int on the right", line[count+1]))
            count += 1

    def isValidFunction(self, line):
        #check if it is a valid statement
        self.isTerminated(line)
        count = 0
        for token in line:
            if (count == 1 and token != "("):
                raise Exception(self.errorExpectedToken(self.__m_line, "(", token))
            if (count == len(line)-2 and token != ")"):
                raise Exception(self.errorExpectedToken(self.__m_line, ")", token))
            if token == ',':
                #check before and after for identifiers or integer constants
                if (not self.__m_Grammar.isIdentifier(line[count-1])) and (not self.__m_Grammar.isIntegerConstant(line[count-1])):
                    raise Exception(self.errorExpectedToken(self.__m_line, "identifier or int on the left", line[count-1]))
                elif (not self.__m_Grammar.isIdentifier(line[count+1])) and (not self.__m_Grammar.isIntegerConstant(line[count+1])):
                    raise Exception(self.errorExpectedToken(self.__m_line, "identifier or int on the right", line[count+1]))
            if token == ';':
                if count != len(line) -1:
                    raise Exception("Invalid use of terminator ';' at line {} expected ','".format(self.__m_line))                     
            count += 1
    
    def isTerminated(self, line):
        if line[-1] != ";":
            raise Exception(self.errorExpectedToken(self.__m_line, "; as a terminator", line[-1]))

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
    
    #custom exception message
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
