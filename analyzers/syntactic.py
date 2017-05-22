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
			return
		elif isProcedure(updatedCurrent()):
			print "isProcedure checkProcedure: ", updatedCurrent()
			return checkProcedure()
	if isCommand(updatedCurrent()):
		print "is COMMAND checkProcedure: ", updatedCurrent()
		print "******PARTE DE RENE"
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

	if isCommand(updatedCurrent()):
		checkCommand()

	print "updatedCurrent() Main: ", updatedCurrent()
	return True
	
if main():
	print "Syntactic analysis was performed and no problems were found."
else:
	print "Syntax analysis detected error"