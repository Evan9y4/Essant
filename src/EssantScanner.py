#Code for the scanner and tokens (as of now)

#Tokens created by the scanner
class Token:
    def __init__(self, token_type, lexeme, literal, line):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line


    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal}"


#The scanner itself
class Scanner:

    #Words that have special meaning or functionality
    keywords = {
        "if": "IF",
        "else": "ELSE",
        "or": "OR",
        "and": "AND",
        "for": "FOR",
        "while": "WHILE",
        "true": "TRUE",
        "false": "FALSE",
        "var": "VAR",
        "return": "RETURN",
        "print": "PRINT",
        "null": "NULL"  
    }


    def __init__(self, source, error_handler):
        self.source = source
        #Positions to go over every individual character
        self.start = 0
        self.current = 0
        self.line = 1
        #A list of the tokens it creates from the source
        self.tokens = []

        #We pass an error handler in case the scanner meets errors
        self.error_handler = error_handler

    #Method 
    def scan_tokens(self):
        while not self.last_character():
            self.start = self.current
            self.scan_token()

        #We put the end of file token after the source has been completely scanned
        self.tokens.append(Token("EOF", "", None, self.line))

        return self.tokens


    #Method
    def scan_token(self):
        #c is how we look ahead, as it is set to the character right after the current character
        c = self.advance()

        #Bunch of if statements for individual tokens
        if c == '+':
            self.add_token("PLUS")

        elif c == '-':
            self.add_token("MINUS")

        elif c == '*':
            self.add_token("STAR")

        elif c == '%':
            self.add_token("PERCENT")

        elif c == '/':
            if self.match('/'):
                #If it's a comment then do the following:
                while self.glance() != '\n' and not self.last_character():
                    self.advance()
            else:
                self.add_token("SLASH")

        elif c == '=':
            if self.match('='):
                self.add_token("EQUAL_EQUAL")
            else:
                self.add_token("EQUAL")

        elif c == '!':
            if self.match('='):
                self.add_token("EXCLAMATION_EQUAL")
            else:
                self.add_token("EXCLAMATION")

        elif c == '<':
            if self.match('='):
                self.add_token("LESS_EQUAL")
            else:
                self.add_token("LESS")

        elif c == '>':
            if self.match('='):
                self.add_token("GREATER_EQUAL")
            else:
                self.add_token("GREATER")

        elif c == '(':
            self.add_token("LEFT_PAREN")

        elif c == ')':
            self.add_token("RIGHT_PAREN")

        elif c == '{':
            self.add_token("LEFT_BRACE")

        elif c == '}':
            self.add_token("RIGHT_BRACE")

        elif c == ';':
            self.add_token("SEMICOLON")

        elif c == ',':
            self.add_token("COMMA")

        elif c == '.':
            self.add_token("DOT")

        #We dont want whitespace to get a token
        elif c in (' ', '\r', '\t'):
            pass

        #We need to identify newlines, especially for error messages
        elif c == '\n':
            self.line += 1

        #We have a different method handle numbers
        elif c.isdigit():
            self.number()

        #A different method handles strings we encounter
        elif c == '"':
            self.string()

        #If the character is a letter or underscore, than it's an identifier
        elif c.isalpha() or c == '_':
            self.identifier()


        #If the character matches none of the many characters the scanner knows, raise an error
        else:
            self.error_handler.error(f"Unexpected character {c} at line {self.line}")


    #This is where we actually create the tokens from the characters
    def add_token(self, token_type, literal=None):
        #[self.start:self.current] basically means from and including start all the way until current. So tokens can be more than one character :)
        text = self.source[self.start:self.current]

        self.tokens.append(Token(token_type, text, literal, self.line))


    #This is where numbers are sent
    def number(self):
        #While the next character is a number
        while self.glance().isdigit():
            self.advance()

        #If there is a dot, we are dealing with decimals
        if self.glance() == '.' and self.glance_next().isdigit():
            self.advance()

            while self.glance().isdigit():
                self.advance()

        value = self.source[self.start:self.current]

        if '.' in value:
            self.add_token("NUMBER", float(value))
        else:
            self.add_token("NUMBER", int(value))


    #This is where we handle strings
    def string(self):
        while self.glance() != '"' and not self.last_character():
            if self.glance() == '\n':
                self.line += 1

            self.advance()

        #If we have a " and we don't see another before the source ends, raise an error for unterminated string
        if self.last_character():
            self.error_handler.error(f"Unterminated string at line {self.line}")
            return

        #The code will only reach this point if it detects a second "
        self.advance()

        #We mess with the values here to remove the quotes
        value = self.source[self.start + 1:self.current - 1]

        self.add_token("STRING", value)


    #Method for handling identifiers
    def identifier(self):
        while self.glance().isalnum() or self.glance() == '_':
            self.advance()

        text = self.source[self.start:self.current]

        #This is where those keywords we established earlier come in
        if text in self.keywords:
            token_type = self.keywords[text]
            self.add_token(token_type)

        else:
            self.add_token("IDENTIFIER")

    #This is used for when we need operations that are more than just one character
    def match(self, expected_character):
        #First it just goes over an edge case
        if self.last_character():
            return False

        #Than we compare
        if self.source[self.current] != expected_character:
            return False

        self.current += 1
        return True


    #Used for actually moving forward in the source
    def advance(self):
        character = self.source[self.current]
        self.current += 1
        return character


    #Same thing as advance but we DO NOT move forward
    def glance(self):
        #This is where we get our EOF
        if self.last_character():
            return '\0'

        return self.source[self.current]

    
    #glance but at the next character
    def glance_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'

        return self.source[self.current + 1]

    #Used to identify when the scanner reaches the end of the file
    def last_character(self):
        return self.current >= len(self.source)
