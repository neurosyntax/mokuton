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
	- Parser expects a syntactically correct class, so need a class template (using HelloWorld in this example) to place functions into.

'''

import javalang
from ast import nodes

code = 'public class HelloWorld{public static int findFirst(int value, int idx) { value &= ~((1 << idx) - 1); int result = Integer.numberOfTrailingZeros(value);        return (result == 32) ? -1 : result;}}'
tree = javalang.parse.parse(code)


def flatTree(tree):
	sub = '('+str(tree)+' '
	leaves = ''
	for n in tree.children:
		if type(n) == type(list()) and len(n) > 0 and (str(n[0]) in nodes or str(n) in nodes):
			for e in n:
				sub += flatTree(e)
		elif str(n) in nodes:
			leaves += flatTree(n)
	return sub.strip()+leaves.strip()+')'

if __name__ == "__main__":
	# This bit assumes the tree returned contains 
	print '('+'('.join(flatTree(tree).split('(')[3:])[:-2]