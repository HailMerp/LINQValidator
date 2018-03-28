import collections
import re

Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])

class Scanner:

  def __init__(self, input):
    self.tokens = []
    self.current_token_number = 0
    for token in self.tokenize(input):
	       self.tokens.append(token)

  def tokenize(self, input_string):
    keywords = {'VAR','FROM', 'IN', 'WHERE', 'ORDERBY', 'SELECT', 'NEW', 'ORDERBYDECENDING', 'MIN','MAX','FIRSTORDEFAULT','ASCENDING','DESCENDING', 'EOF'}
    KEYWORDS = [x.lower() for x in keywords] # zamiana na małe litery

    token_specification = [
        ('ID',      r'[A-Za-z0-9_*]+'), # text
        ('SYMBOL',  r'=|>|=>|<=|<|=='),          # Assignment operators
        ('END',     r';'),           # Statement terminator
        ('COMMA',      r'\,'),   # comma
        ('DOT',      r'\.'),    # dot
        ('VAR',      r'VAR|INT|FLOAT|DOUBLE|STRING'), # var type
        ('NEWLINE', r'\n'),          # Line endings
        ('SKIP',    r'[ \t]'),       # Skip over spaces and tabs
        ('EM',      r'[!]'),        # exclamation mark
        ('OB',      r'[(]'),        # opening bracket
        ('CB',      r'[)]'),        # closing bracket
        ('OCB',      r'[{]'),       # opening curly bracket
        ('CCB',      r'[}]'),       # closing curly bracket
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(tok_regex).match
    line_number = 1
    current_position = line_start = 0
    match = get_token(input_string)
    while match is not None:
        type = match.lastgroup
        if type == 'NEWLINE':
            line_start = current_position
            line_number += 1
        elif type != 'SKIP':
            value = match.group(type)
            if type == 'ID' and value in keywords: # jeśli typ jest z dużych liter
                type = value
            if type == 'ID' and value in keywords: # jeśli typ jest z małych liter
                type = value.upper()
            yield Token(type, value, line_number, match.start()-line_start)
        current_position = match.end()
        match = get_token(input_string, current_position)
    if current_position != len(input_string):
        raise RuntimeError('Error: Unexpected character %r on line %d' % \
                              (input_string[current_position], line_number))
    yield Token('EOF', '', line_number, current_position-line_start)

  def next_token(self):
    self.current_token_number += 1
    if self.current_token_number-1 < len(self.tokens):
      return self.tokens[self.current_token_number-1]
    else:
      raise RuntimeError('Error: No more tokens')
