#
##   Parses and validates text
#

from Parser import *
import os

def main():
    running = True
    while(running):
        try:
            path = input("Howdy Mr. J, please enter filename: ")
            file = open(path, 'r')
        except:
            print("{} is an invalid filename!".format(path))
        else:
            running = False
    
    print("[i]Contents of {}, sintax validation on bottom.".format(path))

    CompParser = Parser(file)
    CompParser.run()
    input('Press Enter to exit')

    #free resources
    file.close()

if __name__ == '__main__':
    main()