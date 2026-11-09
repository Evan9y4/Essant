#This is the file for the error handler


#This is the class that handles all the errors
class ErrorHandler:
    def __init__(self):
        self.has_error = False

    #Print given message and set error to true (which does nothing for now)
    def error(self, message):
        self.has_error = True
        print(f"ERROR: {message}")
