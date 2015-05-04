#
##   Parses and validates text
#

from Parser import *
import os

def main():
    running = True
    while(running):
        try:
            file = open(input("Howdy, please enter filename: "), 'r')
        except:
            print("Invalid filename!")
        else:
            running = False

    CompParser = Parser(file)
    CompParser.validate()

    #free resources
    file.close()

if __name__ == '__main__':
    main()