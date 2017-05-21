#!/usr/bin/env python
#Lexical Analyzer implementation
__author__ = "Felipe Alves"
__email__ = "felipealves@lavid.ufpb.br"

import re
from lexical import lexicalTable

table_index = -1

LIST_OF_TYPES = ['integer','real','boolean']

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
	table_index += 1;
	return table[table_index]

def isIdentifier(element):
	if element[1] == 'Identifier':
		return True
	return False

def isProcedure(element):
	if element[0] == 'Procedure':
		return True
	return False

def isCommand(element):
	if element[0] == 'begin':
		return True
	return False

def checkProcedure():
	print "checagem de procedimento"
	return True

def checkCommand():
	print "checagem de comando composto"
	return True

def checkProgram():
	if nextInTable()[0] == 'program':
		if isIdentifier(nextInTable()):
			if nextInTable()[0] == ';':
				return True		
	return False

def checkVariable():
	current_element = nextInTable() 
	global LIST_OF_TYPES
	if isIdentifier(current_element):
		if nextInTable()[0] == ':':
			if nextInTable()[0] in LIST_OF_TYPES:
				if nextInTable()[0] == ';':
					return checkVariable()		

	elif isProcedure(current_element):
		return checkProcedure()

	elif isCommand(current_element):
		return checkCommand()

	return False

def checkVariableDeclaration():
	current_element = nextInTable() 
	if current_element[0] == 'var':
		return checkVariable()

	elif isProcedure(current_element):
		return checkProcedure()

	elif isCommand(current_element):
		return checkCommand()

	return False

	
if checkProgram() and checkVariableDeclaration():
	print "Syntactic analysis was performed and no problems were found."
else:
	print "Syntax analysis detected error"

# def identifyProgram():