# My own programming language - Essant!

#Importing sys so we can use the commmand line
import sys
from EssantErrors import ErrorHandler
from EssantScanner import Scanner
from EssantParser import Parser
from EssantEvaluator import Evaluator


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

        #We put this here to to reset any errors we experience as this is a new run
        self.error_handler.has_error = False

        #Convert the source code into tokens
        scanner = Scanner(source, self.error_handler)
        tokens = scanner.scan_tokens()


        #If we detect an error, stop the program
        if self.error_handler.has_error:
            return

        #Give the tokens to the parser so we can form an AST Tree
        parser = Parser(tokens)
        statements = parser.parse()

        #If we detect an error, stop the program
        if self.error_handler.has_error:
            return

        #Give the AST to the evaluator so it may evaluate
        evaluator = Evaluator(self.error_handler)
        
        #execute each statement one by one
        for statement in statements:
            evaluator.execute(statement)

            #Remember to handle any errors during runtime
            if self.error_handler.has_error:
                break


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