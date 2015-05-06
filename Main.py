#
##   Parses and validates text
#

from Parser import *
import os

def main():
    running = True
    while(running):
        try:
            path = "count.txt"#input("Howdy, please enter filename: ")
            file = open(path, 'r')
        except:
            print("{} is an invalid filename!".format(path))
        else:
            running = False

    CompParser = Parser(file)
    CompParser.run()

    #free resources
    file.close()

if __name__ == '__main__':
    main()