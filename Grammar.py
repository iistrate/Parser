#
## Grammar
#

class Grammar(object):
    """Tiny Language Grammar"""
    def __init__(self):
        self.__LexicalElements = \
        {
            'program' : ('BEGIN', 'END'),
            'keyword' : ('NULL'),
            'statement' : ('READ', 'WRITE', ':='),
            'symbol' : ('(', ')', '-', '+'),
        }

    def getLex(self):
        return self.__LexicalElements
    
    #see if token is a keyword
    def isProgramK(self, keyword):
        if keyword in self.__LexicalElements['program']:
            return True
        return False

    #see if token is a symbol
    def isSymbol(self, symbol):
        if symbol in self.__LexicalElements['symbol']:
            return True
        return False
        
    #see if token is an integerconstant
    def isIntegerConstant(self, integer):
        if (integer.isdigit()):
            if (int(integer) in range(0, 32767)):
                return True
        return False

    #see if token is a string constant
    def isStringConstant(self, string):
        #if first and last are quotes
        if string[0] == '"' and string[-1] == '"':
            #if there's no other quotes in middle of string
            if '"' not in string[1:-1]:
                return True
        return False

    #see if token is an identifier
    def isIdentifier(self, identifier):
        if  self.isIntegerConstant(identifier) or \
            self.isStringConstant(identifier) or \
            self.isProgramK(identifier) or \
            self.isSymbol(identifier):
            return False
        return True