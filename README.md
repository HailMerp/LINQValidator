# LINQValidator
A project for 'Languages and compilators class' containg files neccessary to validate LINQ grammar strings\

Scanner.py takes input string, scans it and cuts into separate tokens (objects on list, where each token has 4 objects : type, value, line and column) 
Scanner cuts the string and matches token value with a type, line and column through regular expressions.

Validator.py contains a class Parser which is responsible for definig gramatics for LINQ ( each function is a different production) and taking care of errors.
Validator also contains a sample string in LINQ language to test the program.
