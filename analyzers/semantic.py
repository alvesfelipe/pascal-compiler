#!/usr/bin/env python
# coding=utf-8
#Lexical Analyzer implementation
__author__ = "Renê Alves Barbosa"
__email__ = "renealves@lavid.ufpb.br"

import re
from lexical import lexicalTable

def loadLexicalTable():

	with open(lexicalTable, 'r') as my_file:
		file = my_file.read()
		aux_file = file.splitlines()

	table = []
	for line in aux_file:
		table.append(tuple(re.split(r'\t+', line)))
	
	return table

table = loadLexicalTable()

def listIdentifierOfScope():
	idetifierTuple = []
	numberScope = 0
	initDeclaration = False
	countBegin = 0
	i = 0
	j = 0

	while i < len(table):
		if table[i][0] == 'program':
			numberScope += 1
		elif table[i][0] == 'procedure':
			numberScope += 1
			initDeclaration = True
		elif table[i][0] == 'begin' and initDeclaration:
			countBegin += 1
			initDeclaration = False
		elif table[i][0] == 'var':
			initDeclaration = True
		elif table[i][0] == 'end':
			if countBegin == 1:
				numberScope -= 1
			countBegin -= 1
		elif table[i][1] == 'identifier':
			aux = (numberScope, table[i][0], initDeclaration)
			idetifierTuple.insert(j,aux)
			j += 1
		i += 1

	return idetifierTuple

idetifierTuple = listIdentifierOfScope()

def checkIdentifiers(idTuple, val):
	i = 1
	countOccurrence = 0
	while i < len(idetifierTuple):
		if idetifierTuple[i][1] == idTuple[1] and val != i: #verifica se o nome é igual e que não é ela mesma
			if idetifierTuple[i][0] == idTuple[0]: #verifico se é do mesmo escopo
				countOccurrence += 1
				if idTuple[2]: #verifica se ele é declaração
					if i < val:
						print idTuple
						return False
		i += 1

	if not idTuple[2] and countOccurrence == 0:
		print idTuple
		return False

	return True
 
def scrollList():
	j = 1
	while j < len(idetifierTuple):
		print "teste";
		if not checkIdentifiers(idetifierTuple[j], j):
			return False
		j += 1
	return True

tupleTypeIdentifier = []

def typeVerification():
	i = 0
	j = 0
	while i < len(table):
		if table[i][0] == 'var':
			while i < len(table):
				if table[i][0] == 'procedure' or table[i][0] == 'begin':
					break
				if table[i][1] == 'identifier':
					aux = i
					while aux < len(table):
						if table[aux][0] == ':':
							auxTuple = (table[aux+1][0],table[i][0])
							tupleTypeIdentifier.insert(j,auxTuple)
							j += 1
						aux += 1
				i += 1
		i += 1
	print tupleTypeIdentifier

def main():
	if not scrollList():
		print "Error in semantic analyzer"
		return
	print "Success, the program has been analyzed"

# main();
typeVerification();