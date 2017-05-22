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
			compoundCommand()
			return
		elif isProcedure(updatedCurrent()):
			# print "isProcedure checkProcedure: ", updatedCurrent()
			return checkProcedure()
	if isCommand(updatedCurrent()):
		# print "is COMMAND checkProcedure: ", updatedCurrent()
		# print "******PARTE DE RENE"
		nextInTable()
		compoundCommand()
		return
	elif isProcedure(updatedCurrent()):
		# print "isProcedure checkProcedure: ", updatedCurrent()
		return checkProcedure()

def checkProcedure():

	# print "current_element checkProcedure: ", updatedCurrent()

	if isIdentifier(nextInTable()):
		# print "isIdentifier checkProcedure: ", updatedCurrent()
		if table[nextInTable()][0] == '(':
			# print "( checkProcedure: ", updatedCurrent()
			if not listVariableDeclaration():
				return False
			if table[nextInTable()][0] == ';':
				# print "is ; checkProcedure: ", updatedCurrent()
				insideProcedure()
		elif table[updatedCurrent()][0] == ';':
			insideProcedure()

	return False

def checkCommand():
	# print "checagem de comando composto"
	return

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
	if checkExpression():
		if table[nextInTable()][0] == ',':
			return listOfExpression();
		elif table[updatedCurrent()][0] == ')':
			nextInTable()
			return True
		return False
	return False

def checkFactor():
	if isIdentifier(updatedCurrent()):
		nextInTable()
		if table[updatedCurrent()][0] == '(':
			nextInTable()
			return  listOfExpression()
		return True
	elif table[updatedCurrent()][1] in LIST_OF_TYPES:
		return True
	elif table[updatedCurrent()][0] == 'not':
		nextInTable()
		return checkFactor()
	return False

def checkTerm():
	if checkFactor():
		if table[updatedCurrent()][0] in LIST_OP_MULTIPLICATIVE:
			nextInTable()
			return checkTerm()
		return True
	return False


def simpleExpression():
	if table[updatedCurrent()][0] in LIST_OP_SIGNALS:
		nextInTable()
		return checkTerm()
	elif checkTerm():
		if table[updatedCurrent()][0] in LIST_OP_ADITIVE:
			nextInTable()
			return simpleExpression()
		return True
	return False


def checkExpression(): #Para sempre antes do delimitador = , ) = < > <= >= <>
	if simpleExpression():
		if table[updatedCurrent()][0] in LIST_OP_RELATIONAL:
			nextInTable()
			return checkExpression()
		elif table[updatedCurrent()][0] in [',',')','then']:
			return True
	return False



def checkCommand(): #Analisa o delimitador
	if isIdentifier(updatedCurrent()): #variável := expressAO
		if table[nextInTable()][0] == ':=': #variável := expressão
			return checkExpression() #variável := expressão
		elif table[updatedCurrent()][0] == '(':
			return listOfExpression() #ativação_de_procedimento 
		return True
	elif table[updatedCurrent()][0] == 'begin': #comando_composto 
		nextInTable()
		return compoundCommand()
	elif table[updatedCurrent()][0] == 'if':
		nextInTable()
		if checkExpression():
			if table[updatedCurrent()][0] == 'then':
				nextInTable()
				if checkCommand():
					if table[updatedCurrent()][0] == 'else':
						nextInTable()
						return checkCommand()
					elif table[updatedCurrent()][0] == ';':
						nextInTable()
						return True
					return False
				return False
			return False
		return False
	elif table[updatedCurrent()][0] == 'while':
		nextInTable()
		if checkExpression():
			if table[updatedCurrent()][0] == 'do':
				nextInTable()
				return checkCommand()
			return False
		return False
	return False		

def listOfCommand():
	# print "listOfCommand: ", updatedCurrent()
	return checkCommand()

def compoundCommand():
	# print "compoundCommand: ", updatedCurrent()
	if(table[updatedCurrent()][0] == 'end'):
		# print "is end compoundCommand: ", updatedCurrent()
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