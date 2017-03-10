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
from ast         import nodes
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

def getLiteral(vals):
	for v in vals:
		if isinstance(v, basestring):
			return type(num(v)).__name__

def generateAST(tree):
	# if str(tree) == 'BasicType':
		# print tree.children
	if str(tree) == 'Literal':
		sub = '('+getLiteral(tree.children)+' '
	else:
		sub = '('+str(tree)+' '
	leaves = ''
	for n in tree.children:
		if type(n) == type(list()) and len(n) > 0 and (str(n[0]) in nodes or str(n) in nodes):
			for e in n:
				sub += flatTree(e)
		elif str(n) in nodes:
			leaves += flatTree(n)
	return sub.strip()+leaves.strip()+')'

# Inject function source into template to satisfy javalang module
def template(func):
	return 'public class m{'+func+'}'

# Extracts the function AST out of the template
def extractFunc(tree):
	return '('+'('.join(tree.split('(')[3:])[:-2]

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

# Vectorize AST
def vectorize(tree):


if __name__ == "__main__":
	# True  = function AST excluding template
	# False = AST including the template
	funcOnly = True
	vectOnly = False
	# Defaults to localhost:27017
	client = MongoClient()

	# Access database github-repos
	db = client['github_repos']

	# Access collection source
	cursor = db['source'].find()

	# Example document generated by Pakkun. Each document is a Java class containing functions with the desired type, here, numeric->numeric.
	# { 
	# "_id" : NumberLong("3697816498"), 
	# "name" : "Bits.java", 
	# "path" : "/home/ubuntu/research/data/neurosyntax_data/github/java/android/platform_dalvik/dx/src/com/android/dx/util/Bits.java", 
	# "funcs" : 
	# 	[ 
	# 		{ 
	# 			"id" : NumberLong("4108688843"), 
	# 			"name" : "findFirst", 
	# 			"header" : "public static int findFirst(int value, int idx)", 
	# 			"intype" : [ "int", "int" ], 
	# 			"outtype" : [ "int" ], 
	# 			"source" : "public static int findFirst(int value, int idx) {        value &= ~((1 << idx) - 1); // Mask off too-low bits.        int result = Integer.numberOfTrailingZeros(value);        return (result == 32) ? -1 : result;    }" 
	# 		}
	# 	]
	# }
	for document in cursor:
		for fnc in document['funcs']:
			sample = {}
			code   = template(str(fnc['source']))
			tree   = javalang.parse.parse(code)
			sample = {'id':fnc['id'], 'intype': str(fnc['intype']), 'outtype': str(fnc['outtype']), 
					  'label':createLabel(fnc['intype'], fnc['outtype'])}
			if funcOnly:
				sample['ast'] = extractFunc(generateAST(tree))
			else:
				sample['ast'] = generateAST(tree)

			if vectOnly:
				sample['ast'] = vectorize(sample['ast'])

			db.AST.insert_one(sample)
		break
