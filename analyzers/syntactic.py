#!/usr/bin/env python
# coding=utf-8
#Lexical Analyzer implementation
__author__ = "Felipe Alves"
__email__ = "felipealves@lavid.ufpb.br"

import re
from lexical import lexicalTable

table_index = -1

LIST_OF_TYPES = ['integer','real','boolean']
LIST_OP_RELATIONAL = ['=','<','>','<=','>=','<>']
LIST_OP_SIGNALS = ['-','+']
LIST_OP_ADITIVE = ['+','-','or']
LIST_OP_MULTIPLICATIVE = ['*','/','and']

#load lexical table previously generated and put in a list of tuples
def loadLexicalTable():

	with open(lexicalTable, 'r') as my_file:
		file = my_file.read()
		aux_file = file.splitlines()

	table = []
	for line in aux_file:
		table.append(tuple(re.split(r'\t+', line)))
	
	return table

table = loadLexicalTable()

def nextInTable():
	global table_index
	table_index += 1
	return table_index

def incrementInTable(value):
	global table_index
	table_index += value
	return table_index

def updatedCurrent():
	return table_index

def isIdentifier(element):
	if table[element][1] == 'identifier':
		return True
	return False

def isProcedure(element):
	if table[element][0] == 'procedure':
		return True
	return False

def isCommand(element):
	if table[element][0] == 'begin':
		return True
	return False

def insideProcedure():
	if table[nextInTable()][0] == 'var':
		# print "is VAR checkProcedure: ", updatedCurrent()
		if not listVariableDeclaration():
			return False
		if isCommand(nextInTable()):
			# print "is COMMAND checkProcedure: ", updatedCurrent()
			# print "******PARTE DE RENE"
			nextInTable()
			if compoundCommand():
				pass
		elif isProcedure(updatedCurrent()):
			# print "isProcedure checkProcedure: ", updatedCurrent()
			return checkProcedure()
	if isCommand(updatedCurrent()):
		# print "is COMMAND checkProcedure: ", updatedCurrent()
		# print "******PARTE DE RENE"
		nextInTable()
		if compoundCommand():
			pass
	elif isProcedure(updatedCurrent()):
		# print "isProcedure checkProcedure: ", updatedCurrent()
		return checkProcedure()

def checkProcedure():

	# print "checkProcedure: ", updatedCurrent()

	if isIdentifier(nextInTable()):
		# print "checkProcedure: isIdentifier", updatedCurrent()
		if table[nextInTable()][0] == '(':
			# print "checkProcedure is ( : ", updatedCurrent()
			if not listVariableDeclaration():
				return False
			if table[nextInTable()][0] == ';':
				# print "checkProcedure is ; : ", updatedCurrent()
				insideProcedure()
		elif table[updatedCurrent()][0] == ';':
			insideProcedure()

	return False

def checkProgram():
	if table[nextInTable()][0] == 'program':
		if isIdentifier(nextInTable()):
			if table[nextInTable()][0] == ';':
				return True
	return False

def listVariableDeclaration():

	global LIST_OF_TYPES

	# print "current_element comeco: ", updatedCurrent()

	if isIdentifier(nextInTable()):
		# print "isIdentifier: ", updatedCurrent()
		# print "updatedCurrent(): ", updatedCurrent()
		if table[nextInTable()][0] == ':':
			# print "is : ", updatedCurrent()
			if table[nextInTable()][0] in LIST_OF_TYPES:
				# print "is LIST_OF_TYPES: ", updatedCurrent()
				if table[nextInTable()][0] == ';':
					# print "is ; ", updatedCurrent()
					#check if exists new declaration of variables
					if isProcedure(updatedCurrent() + 1):
						# print "isProcedure", table[updatedCurrent()]
						return True
					if isCommand(updatedCurrent() + 1):
						# print "isCommand", table[updatedCurrent()]
						return True
					return listVariableDeclaration()
				elif table[updatedCurrent()][0] == ')':
					# print "is )", updatedCurrent()
					return True
		elif table[updatedCurrent()][0] == ',':
			# print "is , ", updatedCurrent()
			return listVariableDeclaration()

	return False

def listOfExpression():
	# print "listOfExpression: ", updatedCurrent()
	if checkExpression():
		# print "listOfExpression checkExpression: ", updatedCurrent()
		if table[nextInTable()][0] == ',':
			# print "listOfExpression is ,: ", updatedCurrent()
			return listOfExpression();
		elif table[updatedCurrent()][0] == ')':
			# print "listOfExpression is ) : ", updatedCurrent()
			nextInTable()
			return True
		return False
	return False

def checkFactor():
	# print "checkFactor: ", updatedCurrent()
	if isIdentifier(updatedCurrent()):
		# print "checkFactor isIdentifier: ", updatedCurrent()
		nextInTable()
		if table[updatedCurrent()][0] == '(':
			# print "checkFactor is ( : ", updatedCurrent()
			nextInTable()
			return  listOfExpression()
		return True
	elif table[updatedCurrent()][1] in LIST_OF_TYPES:
		# print "checkFactor in LIST_OF_TYPES: ", updatedCurrent()
		#alterei
		if table[updatedCurrent() + 1][0] == ';':
			# print "checkFactor is ; : ", updatedCurrent()
			nextInTable()
			nextInTable()
		return True
	elif table[updatedCurrent()][0] == 'not':
		# print "checkFactor is not: ", updatedCurrent()
		nextInTable()
		return checkFactor()
	return False

def checkTerm():
	# print "checkTerm: ", updatedCurrent()
	if checkFactor():
		# print "checkTerm checkFactor: ", updatedCurrent()
		#alterei
		if table[updatedCurrent() + 1][0] in LIST_OP_MULTIPLICATIVE:
			# print "checkTerm in LIST_OP_MULTIPLICATIVE: ", updatedCurrent()
			nextInTable()
			nextInTable()
			return checkTerm()
		return True
	return False


def simpleExpression():
	# print "simpleExpression: ", updatedCurrent()
	if table[updatedCurrent()][0] in LIST_OP_SIGNALS:
		# print "simpleExpression in LIST_OP_SIGNALS:", updatedCurrent()
		nextInTable()
		return checkTerm()
	elif checkTerm():
		# print "simpleExpression checkTerm:", updatedCurrent()
		#alterei
		if table[updatedCurrent() + 1][0] in LIST_OP_ADITIVE:
			# print "simpleExpression in LIST_OP_ADITIVE: ", updatedCurrent()
			nextInTable()
			nextInTable()
			return checkFactor()
			# return simpleExpression()
		return True
	return False


def checkExpression(): #Para sempre antes do delimitador = , ) = < > <= >= <>
	# print "checkExpression: ", updatedCurrent()
	if simpleExpression():
		# print "checkExpression simpleExpression: ", updatedCurrent()
		if table[updatedCurrent()][0] in LIST_OP_RELATIONAL:
			# print "checkExpression in LIST_OP_RELATIONAL: ", updatedCurrent()
			nextInTable()
			return checkExpression()
		elif table[updatedCurrent()][0] in [',',')','then']:
			# print "checkExpression in [',',')','then']: ", updatedCurrent()
			return True
		elif table[updatedCurrent() + 1][0] in LIST_OP_ADITIVE:
			return simpleExpression()
	#alterei
	if table[updatedCurrent()][0] == 'else':
		# print "checkExpression is else: ", updatedCurrent()
		return True
	if table[updatedCurrent()][0] == ';':
		# print "checkExpression is ;: ", updatedCurrent()
		return True
	return False



def checkCommand(): #Analisa o delimitador
	# print "checkCommand: ", updatedCurrent()
	#alterei
	if isIdentifier(updatedCurrent()) or isIdentifier(updatedCurrent() - 1): #variável := expressAO
		# print "checkCommand isIdentifier: ", updatedCurrent()
		if table[nextInTable()][0] == ':=': #variável := expressão
			# print "checkCommand is := : ", updatedCurrent()
			nextInTable()
			return checkExpression() #variável := expressão
		elif table[updatedCurrent()][0] == '(':
			# print "checkCommand is ( : ", updatedCurrent()
			return listOfExpression() #ativação_de_procedimento 
		return True
	elif table[updatedCurrent()][0] == 'begin': #comando_composto
		# print "checkCommand is begin : ", updatedCurrent()
		nextInTable()
		return compoundCommand()
	elif table[updatedCurrent()][0] == 'if':
		# print "checkCommand is if : ", updatedCurrent()
		nextInTable()
		if checkExpression():
			# print "checkCommand checkExpression : ", updatedCurrent()
			if table[updatedCurrent()][0] == 'then':
				# print "checkCommand is then ", updatedCurrent()
				nextInTable()
				if checkCommand():
					# print "checkCommand checkCommand: ", updatedCurrent()
					if table[updatedCurrent()][0] == 'else':
						# print "checkCommand is else: ", updatedCurrent()
						nextInTable()
						return checkCommand()
					elif table[updatedCurrent()][0] == ';':
						# print "checkCommand is ; : ", updatedCurrent()
						nextInTable()
						return True
					return False
				return False
			return False
		return False
	elif table[updatedCurrent()][0] == 'while':
		# print "checkCommand is while : ", updatedCurrent()
		nextInTable()
		if checkExpression():
			# print "checkCommand checkExpression fora: ", updatedCurrent()
			if table[updatedCurrent()][0] == 'do':
				# print "checkCommand is do: ", updatedCurrent()
				nextInTable()
				return checkCommand()
			return False
		return False
	if table[updatedCurrent()][0] == 'else':
		# print "checkCommand is else: ", updatedCurrent()
		nextInTable()
		return True
	return False		

def listOfCommand():
	# print "listOfCommand: ", updatedCurrent()
	return checkCommand()

def compoundCommand():
	# print "compoundCommand: ", updatedCurrent()
	if(table[updatedCurrent()][0] == 'end'):
		# print "is end compoundCommand: ", updatedCurrent()
		#alterei
		if table[nextInTable()][0] == '.':
			# print "compoundCommand is . : ", updatedCurrent()
			nextInTable()
			return True
		elif table[updatedCurrent()][0] == ';':
			# print "compoundCommand is ; : ", updatedCurrent()
			nextInTable()
			return True
	if not listOfCommand():
		return False
	return compoundCommand()
#parte de RENE

def main():

	if not checkProgram():
		return False

	nextInTable()

	if table[updatedCurrent()][0] == 'var':
		if not listVariableDeclaration():
			return False

	if isProcedure(nextInTable()):
		if not checkProcedure():
			return False

	nextInTable()
	if isCommand(updatedCurrent()):
		return compoundCommand()

	# print "updatedCurrent() Main: ", updatedCurrent()
	return True
	
if main():
	  print "Syntactic analysis was performed and no problems were found."
else:
	  print "Syntax analysis detected error"