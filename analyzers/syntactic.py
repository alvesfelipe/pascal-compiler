#!/usr/bin/env python
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
		print "is VAR checkProcedure: ", updatedCurrent()
		if not listVariableDeclaration():
			return False
		if isCommand(nextInTable()):
			print "is COMMAND checkProcedure: ", updatedCurrent()
			print "******PARTE DE RENE"
			nextInTable()
			compoundCommand()
			return
		elif isProcedure(updatedCurrent()):
			print "isProcedure checkProcedure: ", updatedCurrent()
			return checkProcedure()
	if isCommand(updatedCurrent()):
		print "is COMMAND checkProcedure: ", updatedCurrent()
		print "******PARTE DE RENE"
		nextInTable()
		compoundCommand()
		return
	elif isProcedure(updatedCurrent()):
		print "isProcedure checkProcedure: ", updatedCurrent()
		return checkProcedure()

def checkProcedure():

	print "current_element checkProcedure: ", updatedCurrent()

	if isIdentifier(nextInTable()):
		print "isIdentifier checkProcedure: ", updatedCurrent()
		if table[nextInTable()][0] == '(':
			print "( checkProcedure: ", updatedCurrent()
			if not listVariableDeclaration():
				return False
			if table[nextInTable()][0] == ';':
				print "is ; checkProcedure: ", updatedCurrent()
				insideProcedure()
		elif table[updatedCurrent()][0] == ';':
			insideProcedure()

	return False

def checkCommand():
	print "checagem de comando composto"
	return

def checkProgram():
	if table[nextInTable()][0] == 'program':
		if isIdentifier(nextInTable()):
			if table[nextInTable()][0] == ';':
				return True
	return False

def listVariableDeclaration():

	global LIST_OF_TYPES

	print "current_element comeco: ", updatedCurrent()

	if isIdentifier(nextInTable()):
		print "isIdentifier: ", updatedCurrent()
		print "updatedCurrent(): ", updatedCurrent()
		if table[nextInTable()][0] == ':':
			print "is : ", updatedCurrent()
			if table[nextInTable()][0] in LIST_OF_TYPES:
				print "is LIST_OF_TYPES: ", updatedCurrent()
				if table[nextInTable()][0] == ';':
					print "is ; ", updatedCurrent()
					#check if exists new declaration of variables
					if isProcedure(updatedCurrent() + 1):
						print "isProcedure", table[updatedCurrent()]
						return True
					if isCommand(updatedCurrent() + 1):
						print "isCommand", table[updatedCurrent()]
						return True
					return listVariableDeclaration()
				elif table[updatedCurrent()][0] == ')':
					print "is )", updatedCurrent()
					return True
		elif table[updatedCurrent()][0] == ',':
			print "is , ", updatedCurrent()
			return listVariableDeclaration()

	return False

#parte de RENE
def checkFactor():
	print "checkFactor: ", updatedCurrent()
	if isIdentifier(updatedCurrent()):
		print "checkFactor isIdentifier: ", updatedCurrent()
		if table[updatedCurrent()][0] == '(':
			print "checkFactor is (: ", updatedCurrent()
			if listOfExpression():
				print "checkFactor listOfExpression: ", updatedCurrent()
				if table[nextInTable()][0] == ')':
					print "checkFactor is ): ", updatedCurrent()
					return True
		return True
	elif table[updatedCurrent()][1] in LIST_OF_TYPES:
		print "checkFactor LIST_OF_TYPES: ", updatedCurrent()
		return True
	elif table[updatedCurrent()][0] == 'not':
		print "checkFactor is not: ", updatedCurrent()
		return checkFactor()
	elif table[updatedCurrent()][0] == '(':
		print "checkFactor is (: ", updatedCurrent()
		if checkExpression():
			print "checkFactor checkExpression: ", updatedCurrent()
			if table[nextInTable()][0] == ')':
				print "checkFactor is ): ", updatedCurrent()
				return True
	return False

def checkTerm():
	print "checkTerm: ", updatedCurrent()
	if checkFactor():
		print "checkTerm checkFactor***: ", updatedCurrent()
		if table[updatedCurrent()+1][0] in LIST_OP_MULTIPLICATIVE:
			print "LIST_OP_MULTIPLICATIVE checkTerm: ", updatedCurrent()
			nextInTable()
			nextInTable()
			return checkTerm()
		return True
	return False


def simpleExpression():
	print "simpleExpression: ", updatedCurrent()
	if table[nextInTable()][0] in LIST_OP_SIGNALS:
		print "LIST_OP_SIGNALS: ", updatedCurrent()
		nextInTable()
		return checkTerm()
	elif checkTerm():
		print "checkTerm in simpleExpression: ", updatedCurrent()
		if table[nextInTable()][0] in LIST_OP_ADITIVE:
			print "LIST_OP_ADITIVE: ", updatedCurrent()
			return checkTerm()
		return True
	return False

def checkExpression():
	print "checkExpression: ", updatedCurrent()
	if simpleExpression():
		print "checkExpression simpleExpression: ", updatedCurrent()
		if table[updatedCurrent()][0] == ';':
			print "is ; checkExpression: ", updatedCurrent()
			return True
		if table[updatedCurrent()][0] in LIST_OP_RELATIONAL:
			print "LIST_OP_RELATIONAL checkExpression: ", updatedCurrent()
			return simpleExpression()
		return True
	return False

def listOfExpression():
	print "listOfExpression: ", updatedCurrent()
	nextInTable()
	if checkExpression():
		print "listOfExpression checkExpression: ", updatedCurrent()
		if table[nextInTable()][0] == ',':
			print "listOfExpression is , : ", updatedCurrent()
			listOfExpression()
		return True
	return False

def checkCommand():
	print "checkCommand: ", updatedCurrent()
	if isIdentifier(updatedCurrent()):
		print "is isIdentifier checkCommand: ", updatedCurrent()
		if table[nextInTable()][0] == ':=':
			print "is := checkCommand: ", updatedCurrent()
			if checkExpression():
				return True
		elif table[updatedCurrent()][0] == '(':
			print "is ( checkCommand: ", updatedCurrent()
			if listOfExpression():
				if table[nextInTable()][0] == ')':
					print "is ) checkCommand: ", updatedCurrent()
					return True
		elif table[updatedCurrent()][0] == ';':
			print "is ; checkCommand: ", updatedCurrent()
			return True

	elif table[updatedCurrent()][0] == 'begin':
		print "is begin checkCommand: ", updatedCurrent()
		return compoundCommand()
	elif table[updatedCurrent()][0] == 'if':
		print "is if checkCommand: ", updatedCurrent()
		if checkExpression():
			print "checkExpression checkCommand: ", updatedCurrent()
			if table[updatedCurrent()][0] == 'then':
				print "is then checkCommand: ", updatedCurrent()
				if checkCommand():		
					print "checkCommand checkCommand: ", updatedCurrent()
					if table[nextInTable()][0] == 'else':
						print "is else checkCommand: ", updatedCurrent()
						nextInTable()
						return checkCommand()
					return True
	elif table[updatedCurrent()][0] == 'while':
		print "is while checkCommand: ", updatedCurrent()
		if checkExpression():
			print "checkExpression checkCommand: ", updatedCurrent()
			if table[nextInTable()][0] == 'do':
				print "is do checkCommand: ", updatedCurrent()
				return checkCommand()
	return False

def listOfCommand():
	print "listOfCommand: ", updatedCurrent()
	return checkCommand()

def compoundCommand():
	print "compoundCommand: ", updatedCurrent()
	if(table[updatedCurrent()][0] == 'end'):
		print "is end compoundCommand: ", updatedCurrent()
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

	print "updatedCurrent() Main: ", updatedCurrent()
	return True
	
if main():
	print "Syntactic analysis was performed and no problems were found."
else:
	print "Syntax analysis detected error"