#!/usr/bin/env python
#Lexical Analyzer implementation
__author__ = "Felipe Alves"
__email__ = "felipealves@lavid.ufpb.br"

import sys
import re

#token lists
key_words = ['program', 'var', 'integer', 'real',
			 'boolean', 'procedure', 'begin', 'end',
			 'if', 'then', 'else', 'while', 'do', 'not']
delimiters = [';', '.', ':', '(', ')', ',']
assignment = [':=']
relational_operators = ['=', '<', '>']
relational_operators_2 = ['<=', '>=', '<>']
aditive_operators = ['+', '-']
multiplicative_operators = ['*', '/']
special_operators = ['or', 'and']
#end token lists

#defining dictionary with toke type (key) and token list (value)
token_type = {'Key Word': key_words,
		  'Delimiter': delimiters,
		  'Operator': relational_operators + relational_operators_2 + 
		  			  aditive_operators + multiplicative_operators + special_operators + assignment
		  # 'Relational Operator': relational_operators,
		  # 'Aditive Operator': aditive_operators,
		  # 'Multiplicative Operator': multiplicative_operators,
		  # 'Special Operator': special_operators
		 }
#end dictionary

#function for write tuple in file
def writeInTable(listTuple):
	f = open('files/outTable.txt', 'a')
	f.write(listTuple[0] + '\t' + listTuple[1] + '\t' + listTuple[2] + '\n')
	f.close()

def removeTrash(str):
	removed = str.replace('\t', '')
	removed = re.sub(r'\{.*?\}', '', removed)

	return removed

#check if the toen is an identifier
def isIdentifier(str):
	identifiers = re.compile('^[a-zA-Z][a-zA-Z0-9_]*$')
	result = identifiers.match(str)

	if result:
		return True
	else:
		return False

#check if the token is an integer
def isInt(str):
    try: 
        int(str)
        return True
    except ValueError:
        return False

#check if the token is a float
def isFloat(str):
	try:
		float(str)
		return True
	except ValueError:
		return False

#check if the string is a token
def isToken(token):
	for key in token_type:
		if any(token == value for value in token_type[key]):
			return (token, key)
	if isInt(token):
		return (token, "Integer")
	if isFloat(token):
		return (token, "Float")
	if isIdentifier(token):
		return (token, "Identifier")
	return None

#function for add spaces between simple tokens like: ;, :, . 
def spaceSimpleOperator(str, token_list):
	for i in token_list:
		for ap in range(str.count(i)):
			indices = [ind for ind, x in enumerate(str) if x == i]
			if indices:
				right_test = ''
				left_test = ''
				aux = indices[ap]
				if aux+1 <= len(str)-1:
					right_test = str[aux] + str[aux+1]
				if aux-1 >= str.index(str[0]):
					left_test = str[aux-1] + str[aux]
				
				if any(right_test in s for s in relational_operators_2 + assignment):
					str = str[:aux] + ' ' + str[aux:]
					str = str[:aux+3] + ' ' + str[aux+3:]
				elif any(left_test in s for s in relational_operators_2 + assignment):
					pass
				else:
					str = str[:aux] + ' ' + str[aux:]
					str = str[:aux+2] + ' ' + str[aux+2:]
	return str			

#function responsible for make the analyse of the input file, receive a list of all lines
def lexicalAnalysis(list_file):
	for index, line in enumerate(list_file):
		list_file[index] = spaceSimpleOperator(list_file[index], delimiters + relational_operators + 
											   aditive_operators + multiplicative_operators)

	for index, line in enumerate(list_file):
		for token in line.split():
			aux = isToken(token)
			if aux is not None:
				writeInTable(aux + (str(index + 1),))
			else:
				print "ERROR"
				return
	print "LEXICAL ANALYSIS SUCCESS"


#read file, split by line and put in a string
with open(sys.argv[1], 'r') as my_file:
	file = my_file.read()
#removing unused elements
file = removeTrash(file)
#split file by lines
list_file = file.splitlines()

# print list_file
lexicalAnalysis(list_file)
# print list_file

#DEBUG PRINTS
# number_test = 'aasdf123sd'
# token_test = 'v <=1;v <=1; valor1: integer;'
# ident_test = 'AAa066_'

# #get the number of lines
# print "-------------->Lines:", len(list_file)
# token_test = spaceSimpleOperator(token_test, delimiters)
# print "Token: ", token_test
# token_test = identifySpecialTokens(token_test, '1')
# print "Token: ", token_test
# insertRelationalSpace(token_test)
# print "Is Token: ", isToken(number_test)
# writeInTable(isToken(number_test))