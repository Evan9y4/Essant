# My own programming language - Essant!

#Importing sys so we can use the commmand line
import sys
from EssantScanner import Scanner
from EssantParser import Parser
from EssantAST import ASTPrinter


# The interpreter
class Essant:
    def __init__(self):
        # Create an error handler for essant
        self.error_handler = ErrorHandler()

    #Giving Essant a file in the command line
    def run_file(self, path):
        try:
            with open(path, "r") as file:
                #Grab the data from the file
                source = file.read()
        except OSError as error:
            self.error_handler.error(str(error))
            return

        #Give the method that actually "runs" the content on the file
        self.run(source)


    #Enter REPL mode if there are no arguments given 
    def run_REPL(self):
        while True:
            try:
                #This just creates a little arrow in front of the input
                code_line = input("--> ")
            except KeyboardInterrupt:
                #Outputs a small message before exiting
                print("Closed Manually")
                break

            #Give the method that actually "runs" the users input
            self.run(code_line)


    #This is where we actually "run" the language
    def run(self, source):
        print(source)
        scanner = Scanner(source, self.error_handler)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        expression = parser.parse()

        if expression is not None:
            printer = ASTPrinter()
            print(printer.print(expression))

        for token in tokens:
            print(token)


#This is the class that handles all the errors
class ErrorHandler:
    def __init__(self):
        self.has_error = False

    #Print given message and set error to true (which does nothing for now)
    def error(self, message):
        self.has_error = True
        print(message)


#Run our interpreter
def main():
    essant = Essant()

    if len(sys.argv) > 2:
        print("I don't actually know what to do here ")
        return

    if len(sys.argv) == 2:
        essant.run_file(sys.argv[1])
    else:
        essant.run_REPL()


if __name__ == "__main__":
    main()