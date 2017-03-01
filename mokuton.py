'''
	mokuton.py
	2.24.17

	Generates abstract syntax trees from function source code and then inserts it and the 
	input types and output types back into MongoDB.
	
	MOKUTON NO JUTSU!!!

	Dependencies: javalang, pymongo

	Refer to https://docs.mongodb.com/getting-started/python/client/ for more info on pymongo
	
	Note:
	- All strings are returned as unicode
	- Parser expects a syntactically correct class, so need a class template to place functions into.

'''

import javalang
from ast     import nodes
from pymongo import MongoClient

# Traverse nodes to generate AST
def generateAST(tree):
	sub = '('+str(tree)+' '
	leaves = ''
	for n in tree.children:
		if type(n) == type(list()) and len(n) > 0 and str(n[0]) in nodes:
			sub += generateAST(n[0])
			# print sub
		elif str(n) in nodes:
			leaves += generateAST(n)
	return sub.strip()+leaves.strip()+')'

# Inject function source into template to satisfy javalang module
def template(func):
	return 'public class Hello{'+func+'}'

# Extracts the function AST out of the template
def extractFunc(tree):
	return '('+'('.join(tree.split('(')[3:])[:-2]

if __name__ == "__main__":
	# Set to False if you want the AST including the template, else leave as True for only the function AST
	funcOnly = True
	# Defaults to localhost:27017
	client = MongoClient()

	# Access database github-repos
	db = client['github_repos']

	# Access collection source
	cursor = db['source'].find()

	for document in cursor:
		for fnc in document['funcs']:
			sample = {}
			code = template(str(fnc['source']))
			tree = javalang.parse.parse(code)
			if funcOnly:
				sample = {'ast': extractFunc(generateAST(tree)), 'intype': str(fnc['intype']), 'outtype': str(fnc['outtype'])}
			else:
				sample = {'ast': generateAST(tree), 'intype': str(fnc['intype']), 'outtype': str(fnc['outtype'])}
			db.AST.insert_one(sample)
