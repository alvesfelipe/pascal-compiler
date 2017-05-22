#!/usr/bin/env python
#Lexical Analyzer implementation
__author__ = "Felipe Alves"
__email__ = "felipealves@lavid.ufpb.br"

import re
from lexical import lexicalTable

table_index = -1
actual_position = None

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
	table_index += 1
	return table_index

def isIdentifier(element):
	if table[element][1] == 'Identifier':
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

def checkProcedure():
	print "checagem de procedimento"
	return

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

	current_element = nextInTable()
	global LIST_OF_TYPES

	print "current_element: ", current_element

	if isIdentifier(current_element):
		print "isIdentifier: ", table_index
		current_element = nextInTable()
		print "current_element: ", table_index
		if table[current_element][0] == ':':
			print "is : ", table_index
			if table[nextInTable()][0] in LIST_OF_TYPES:
				print "is LIST_OF_TYPES: ", table_index
				if table[nextInTable()][0] == ';':
					print "is ; ", table_index
					#check if exists new declaration of variables
					if isProcedure(current_element + 1):
						print "isProcedure", table[current_element]
						return True
					if isCommand(current_element + 1):
						print "isCommand", table[current_element]
						return True
					return listVariableDeclaration()
		elif table[current_element][0] == ',':
			print "is , ", table_index
			return listVariableDeclaration()

	return False

def main():

	if not checkProgram():
		return False

	current_element = nextInTable()

	if table[current_element][0] == 'var':
		if not listVariableDeclaration():
			return False

	current_element = table_index
	if isProcedure(current_element):
		checkProcedure()

	current_element = table_index
	if isCommand(current_element):
		checkCommand()

	print "current_element Main: ", current_element
	return True
	
if main():
	print "Syntactic analysis was performed and no problems were found."
else:
	print "Syntax analysis detected error"

# def identifyProgram():