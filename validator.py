from scanner import *



class Parser:

  ##### Parser header #####
  def __init__(self, scanner):
    self.next_token = scanner.next_token
    self.token = self.next_token()

  def take_token(self, token_type):
    if self.token.type != token_type:
      self.error("Unexpected token: %s" % token_type)
    if token_type != 'EOF':
      self.token = self.next_token()


  def error(self,msg):
    raise RuntimeError('Parser error, %s' % msg)

  ##### Parser body #####

  def start(self):
    # start -> program EOF
    if self.token.type == 'VAR' or self.token.type == 'FROM' or self.token.type == 'SELECT' or self.token.type == 'WHERE' or self.token.type == 'ORDERBY' or self.token.type == 'ID' or self.token.type == 'EOF':
      self.program()
      self.take_token('END')
    else:
      self.error("Epsilon not allowed")

  def program(self):
    # program -> statement program
    if self.token.type == 'VAR' or self.token.type == 'FROM' or self.token.type == 'SELECT' or self.token.type == 'WHERE' or self.token.type == 'ORDERBY' or self.token.type == 'ID':
      self.statement()
      self.program()


    # program -> eps
    else:
      print(self.token.value)



  def statement(self):
    # statement -> from_statement
    if self.token.type == 'VAR':
      self.variable()
    # statement -> from_statement
    elif self.token.type == 'FROM':
      self.from_statement()
    # statement -> where_statement
    elif self.token.type == 'WHERE':
      self.where_statement()
    # statement -> sort_statement
    elif self.token.type == 'ORDERBY':
      self.sort_statement()
    # # statement -> select_sentences
    elif self.token.type == 'SELECT':
      self.select_statement()
    else:
      self.error(self.token.value)

  def variable(self):
    # <variable> -> <VAR><parameter>
    if self.token.type == 'VAR':
      self.take_token('VAR')
      self.parameter()
      self.take_token('SYMBOL')
      print("variable OK")
    else:
      self.error("Epsilon not allowed")



  def from_statement(self):
    # from_statement -> FROM <parameter> IN <parameter>
    if self.token.type == 'FROM':
      self.take_token('FROM')
      self.parameter()
      self.take_token('IN')
      self.parameter()
      print("from statement OK")
    # from_statement -> <parameter><DOT>ORDERBYDECENDING<OB><condition><CB>
    elif self.token.type == 'ID':
      self.parameter()
      self.take_token('DOT')
      self.take_token('ORDERBYDESCENDING')
      self.take_token('OB')
      self.condition()
      self.take_token('CB')
      print("from statement OK")
    else:
      self.error("Epsilon not allowed")



  def where_statement(self):
      # <where_statement> -> <WHERE><negation><condition>
    if self.token.type == 'WHERE':
      self.take_token('WHERE')
      self.negation()
      self.condition()
      print("where statement OK")
    else:
      pass


  def sort_statement(self):
      # <sort_statement> -> <orderby><parameter><sort_type>
    if self.token.type == 'ORDERBY':
      self.take_token('ORDERBY')
      self.parameter()
      self.sort_type()
      print("sort statement OK")
      # <sort_statement> -> eps
    else:
      pass


  # select_statement -> 'SELECT'<select_body><order_function>
  def select_statement(self):
      # <select_statement> -> <SELECT><select_body><order_function>
    if self.token.type == 'SELECT':
      self.take_token('SELECT')
      self.select_body()
      self.order_function()

      print("select statement OK")
    else:
      self.error("Epsilon not allowed")


  def select_body(self):
   # select_body -> ID
    if self.token.type == 'ID':
      self.take_token('ID')
   # select_body -> NEW  ‘{‘ <select_sentences> ‘}’
    elif self.token.type == 'NEW':
      self.take_token('NEW')
      self.take_token('OCB')
      self.parameter()
      self.select_sentences()
      self.take_token('CCB')
    else:
      self.error("Epsilon not allowed")


  def select_sentences(self):
      # <select_sentences> -> <COMMA><parameter>
    if self.token.type == 'COMMA':
      self.take_token('COMMA')
      self.parameter()
      # <select_sentences> -> <SYMBOL><parameter><select_sentences>
    elif self.token.type == 'SYMBOL':
      self.take_token('SYMBOL')
      self.parameter()
      self.select_sentences()
      # <select_sentences> -> eps
    else:
      pass


  def order_function(self):
   # <order_function> -> <DOT> ‘min’ '('')'

   if self.token.type == 'DOT' :
      self.take_token('DOT')
      if self.token.type == 'MIN':
         self.take_token('MIN')
         self.take_token('OB')
         self.take_token('CB')
   # <order_function> -> <DOT> ‘max’ '('')'
   elif self.token.type == 'MAX':

      self.take_token('MAX')
      self.take_token('OB')
      self.take_token('CB')
   # <order_function> -> <DOT> ‘FirstOrDefault’ '('')'
   elif self.token.type == 'FIRSTORDEFAULT':

      self.take_token('FIRSTORDEFAULT')
      self.take_token('OB')
      self.take_token('CB')
   # <order_function> -> eps
   else:
      pass


  def parameter(self):
    # <parameter> -> <ID>
    if self.token.type == 'ID':
      self.take_token('ID')
    # <parameter> -> <parameter><DOT><parameter>
      if self.token.type == 'DOT':
        self.take_token('DOT')
        self.parameter()
    # <parameter> -> <parameter><COMMA><parameter>
      elif self.token.type == 'COMMA':
        self.take_token('COMMA')
        self.parameter()

    else:
      self.error("Epsilon not allowed")


  def condition(self):
    # condition -> <parameter><SYMBOL><parameter>
    if self.token.type == 'ID':
      self.take_token('ID')
      if self.token.type == 'SYMBOL':
        self.take_token('SYMBOL')
        self.parameter()
        # condition -> <parameter><DOT><function>
      elif self.token.type == 'DOT':
        self.take_token('DOT')
        self.function()

    # condition -> eps
    else:
      pass

# function production
  def function(self):
   # function -> <parameter><OB><parameter><CB>
    if self.token.type == 'ID':
      self.parameter()
      self.take_token('OB')
      self.parameter()
      self.take_token('CB')
   # function -> eps
    else:
      pass

# negation production
  def negation(self):
    # <negation> -> <EM>
    if self.token.type == 'EM':
      self.take_token('EM')
    # <negation> -> eps
    else:
      pass

# sort type production
  def sort_type(self):
   # <sort_type> -> <ASCENDING>
    if self.token.type == 'ASCENDING':
      self.take_token('ASCENDING')
   # <sort_type> -> <DESCENDING>
    elif self.token.type == 'DESCENDING':
      self.take_token('DESCENDING')
   # <sort_type> -> eps
    else:
      pass




# sprawdzanie poprawnosci


input_string = '''
VAR query_orderby1 = FROM c IN svcContext.ContactSet
                      WHERE !c.CreditLimit.Equals(null)
                      ORDERBY c.CreditLimit DESCENDING
                      SELECT NEW
                      {
                       limit = c.CreditLimit,
                       first = c.FirstName,
                       last = c.LastName
                      }.MIN();
'''

print(input_string)
scanner = Scanner(input_string)
for line in scanner.tokens:
    print(line)
parser = Parser(scanner)
parser.start()
