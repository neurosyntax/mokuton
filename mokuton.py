'''
	mokuton.py
	2.24.17

	Generates abstract syntax trees from function source code and then inserts it and the 
	input types and output types back into MongoDB.

	Dependencies: javalang, pymongo

	Refer to https://docs.mongodb.com/getting-started/python/client/ for more info on pymongo
	
	Note:
	- All strings are returned from Mongo are unicode
	- Parser expects a syntactically correct Java class, so need a class template to place functions into.
'''

import javalang
import collections
from ast         import nodes
from ast 		 import nodeVect
from pymongo     import MongoClient
from collections import Counter

# Convert string to numeric
def num(s):
	try:
		return int(s)
	except ValueError:
		try:
			return float(s)
		except ValueError:
			return s

# Get string of type of literal
def getLiteral(vals):
	for v in vals:
		if isinstance(v, basestring):
			if not(type(num(v)).__name__.strip() in nodeVect):
				global malformed
				malformed = True
			return type(num(v)).__name__

# Recursively construct AST
def generateAST(tree):
	sub = []
	curr = str(tree)
	if curr in nodes:
		sub.append('(')
		if curr == 'Literal':
			sub.append(str(getLiteral(tree.children))) 
			sub.append(')')
		else:
			sub.append(curr)
			try:
				for ch in tree.children:
					if type(ch) == type(list()):
						for e in ch:
							if str(e) in nodes:
								subtree = generateAST(e)
								if len(subtree) > 0:
									sub.extend(subtree)
					elif str(ch) in nodes:
						subtree = generateAST(ch)
						if len(subtree) > 0:
							sub.extend(subtree)
			except AttributeError:
				pass
			sub.append(')')
		return sub
	return sub
			
# Vectorize AST
def vectorize(tree):
	for i, t in enumerate(tree):
		if t in nodeVect:
			tree[i] = nodeVect[t]
	return tree

# Inject function source into template to satisfy javalang module
def template(func):
	return 'public class m{'+func+'}'

# Return a 1x14 label vector
# The left seven indices represent the inputs and the right seven represent outputs
# Each position contains the number of each type
# e.g. 
# public static int findFirst(int value, int idx)
# [2 0 0 0 0 0 0 1 0 0 0 0 0 0] 
# The order is defined by the indx dict in the function below
def createLabel(intype, outtype):
	indx = {'int':0, 'double':1, 'float':2, 'boolean':3, 'long':4, 'short':5, 'byte':6}
	label = [0]*14
	typ = Counter(intype).keys()
	cnt = Counter(intype).values()
	for t, c in zip(typ, cnt):
		label[indx[t]] = c

	typ = Counter(outtype).keys()
	cnt = Counter(outtype).values()
	for t, c in zip(typ, cnt):
		label[indx[t]+7] = c

	return label

if __name__ == "__main__":
	# Defaults to localhost:27017
	client = MongoClient()

	# Access database github-repos
	db = client['github_repos']

	# Access collection source
	cursor = db['source'].find()

	# Example document generated by Pakkun. Each document is a Java class containing functions with the desired type, here, numeric->numeric.
	# { 
	# "_id" : "3697816498", 
	# "name" : "Bits.java", 
	# "path" : "/home/ubuntu/research/data/neurosyntax_data/github/java/android/platform_dalvik/dx/src/com/android/dx/util/Bits.java", 
	# "funcs" : 
	# 	[ 
	# 		{ 
	# 			"id" : "4108688843", 
	# 			"name" : "findFirst", 
	# 			"header" : "public static int findFirst(int value, int idx)", 
	# 			"intype" : [ "int", "int" ], 
	# 			"outtype" : [ "int" ], 
	# 			"source" : "public static int findFirst(int value, int idx) {        value &= ~((1 << idx) - 1); int result = Integer.numberOfTrailingZeros(value);        return (result == 32) ? -1 : result;    }" 
	# 		}
	# 	]
	# }
	for document in cursor:
		doc_id = document['_id']
		for fnc in document['funcs']:
			global malformed
			malformed = False
			sample = {}
			code   = template(str(fnc['source']))
			try:
				tree   = javalang.parse.parse(code)
			except javalang.parser.JavaSyntaxError:
				print 'JavaSyntaxError:\n',code

			sample = {'doc_id':doc_id, 'func_id':fnc['id'], 'intype': str(fnc['intype']), 'outtype': str(fnc['outtype']), 
					  'label':createLabel(fnc['intype'], fnc['outtype'])}
			
			sample['ast'] = list(generateAST(tree))

			if not malformed:
				# Remove empty strings, and nodes and parentheses from dumby class
				sample['ast']    = [v for v in sample['ast'] if len(v) > 0][4:][:-2]
				sample['astvec'] = vectorize(sample['ast'][:])
				db.AST.insert_one(sample)
			else:
				print 'malformed literals\ndocument id: ',str(document['_id']),'\nfunc id: ',str(fnc['id']),'\n'