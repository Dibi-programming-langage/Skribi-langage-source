# ====== #
# tokens #
# ====== #

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_STRING = 'STRING'
TT_OPERATOR = 'OPERATOR'
TT_BRACKET = 'BRACKET'


class Token:

    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


# ===== #
# lexer #
# ===== #

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return Token(TT_FLOAT, float(result))
        return Token(TT_INT, int(result))

    def string(self, sep='"'):
        result = ''
        backslash = False
        while self.current_char is not None and (self.current_char != sep or backslash):
            result += self.current_char
            if self.current_char == '\\' and not backslash:
                backslash = True
            else:
                backslash = False
            self.advance()
        self.advance()
        return Token(TT_STRING, result)

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.integer()

            if self.current_char == '+':
                self.advance()
                return Token(TT_OPERATOR, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TT_OPERATOR, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TT_OPERATOR, '*')

            if self.current_char == '/':
                self.advance()
                return Token(TT_OPERATOR, '/')

            if self.current_char == '(':
                self.advance()
                return Token(TT_BRACKET, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TT_BRACKET, ')')

            if self.current_char == '"':
                return self.string()

            self.error()

        return Token(None, None)

    def error(self):
        raise Exception('Invalid character')

    def __iter__(self):
        while self.current_char is not None:
            token = self.get_next_token()
            print(token)
            yield token