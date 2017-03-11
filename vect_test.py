'''
	mokuton.py
	2.24.17

	Generates abstract syntax trees from function source code and then inserts it and the 
	input types and output types back into MongoDB.

	Dependencies: javalang, pymongo

	Refer to https://docs.mongodb.com/getting-started/python/client/ for more info on pymongo
	
	Note:
	- All strings are returned as unicode
	- Parser expects a syntactically correct class, so need a class template (using HelloWorld in this example) to place functions into.

'''

import javalang
import collections
from ast import nodes
from ast import nodeVect

# code = 'public class HelloWorld{public static int findFirst(int value, int idx) { value &= ~((1 << idx) - 1); int result = Integer.numberOfTrailingZeros(value);        return (result == 32) ? -1 : result;}}'
code = 'public class HelloWorld{public static float add(int a, int b){a+=5; return 3.14;}}'
tree = javalang.parse.parse(code)

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
	sub = []
	if str(tree) == 'Literal':
		sub.append(str('('))
		sub.append(str(getLiteral(tree.children)))
	else:
		sub.append(str('('))
		# sub.append(str(nodeVect[str(tree)]))
		sub.append(str(tree))
	leaves = ''
	for n in tree.children:
		if type(n) == type(list()) and len(n) > 0 and (str(n[0]) in nodes or str(n) in nodes):
			for e in n:
				sub.append(generateAST(e))
		elif str(n) in nodes:
			sub.append(generateAST(n))
	sub.append(leaves.strip())
	# sub.append(str(nodeVect[')']))
	sub.append(str(')'))
	return sub

def flatten(l):
	for el in l:
		if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
			for sub in flatten(el):
				yield sub
		else:
			yield el

def vectorize(tree):
	for i, t in enumerate(tree):
		tree[i] = nodeVect[t]
	return tree

if __name__ == "__main__":
	# This bit assumes the tree returned contains  
	vec = list(flatten(generateAST(tree)))
	print vectorize([v for v in vec if len(v) > 0][4:][:-2])