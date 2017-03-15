# mokuton

Generates abstract syntax trees from function source code and then inserts it and the input types and output types back into MongoDB.

Dependencies: javalang, pymongo

Refer to https://docs.mongodb.com/getting-started/python/client/ for more info on pymongo

Note:
- All strings are returned as unicode
- javalang parser expects a syntactically correct class, so need a class template to place functions into (using HelloWorld in example below).

Example:
```
Given 'public class HelloWorld{public static float add(int a, int b){a+=5; return 3.14;}}'

Expanded manually:
public class HelloWorld
{
	public static float add(int a, int b)
	{
		a+=5;
		return 3.14;
	}
}

$ python mokuton.py

# AST
(MethodDeclaration(BasicType)(FormalParameter(BasicType))(FormalParameter(BasicType))(StatementExpression(Assignment(MemberReference)(int)))(ReturnStatement(float)))

# Expanded manually:
(MethodDeclaration
	(BasicType)
	(FormalParameter
		(BasicType)
	)
	(FormalParameter
		(BasicType)
	)
	(StatementExpression
		(Assignment
			(MemberReference)
				(int)
			)
		)
	(ReturnStatement
		(float)
	)
)

# Vectorized AST
['84', '49', '84', '8', '85', '84', '36', '84', '8', '85', '85', '84', '36', '84', '8', '85', '85', '84', '57', '84', '7', '84', '48', '85', '84', '77', '85', '85', '85', '84', '55', '84', '79', '85', '85', '85']

# Example document in MongoDB AST collection 
{ 
	"_id" : ObjectId("58c8acf01962cf4f27ea2800"), 
	"astvec" : [ 84, 49, 84, 8, 85, 84, 36, 84, 8, 85, 85, 84, 36, 84, 8, 85, 85, 84, 55, 84, 64, 84, 9, 84, 48, 85, 84, 48, 85, 85, 84, 48, 85, 84, 48, 85, 85, 85, 85 ], 
	"ast" : [ "(", "MethodDeclaration", "(", "BasicType", ")", "(", "FormalParameter", "(", "BasicType", ")", ")", "(", "FormalParameter", "(", "BasicType", ")", ")", "(", "ReturnStatement", "(", "TernaryExpression", "(", "BinaryOperation", "(", "MemberReference", ")", "(", "MemberReference", ")", ")", "(", "MemberReference", ")", "(", "MemberReference", ")", ")", ")", ")" ], 
	"intype" : "[u'float', u'float']", 
	"label" : [ 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0 ], 
	"outtype" : "[u'float']", 
	"func_id" : 1138874885, 
	"doc_id" : NumberLong("4152135009") 
}
*_id* is the unique if for this document in the AST collection.
*astvec* is the vectorized AST. Refer to ast.py for the AST nodes to integer mapping.
*ast* is the actual AST.
*intype* contains the type(s) of the function's input
*label* the label for training. Refer to the label section of this README for more info.
*outtype* contains the type(s) of the function's output
*func_id* is the unique id of the function this AST was generated from.
*doc_id* is the document containing the function this AST was generated from. Use this and the *func_id* to query the original source in the *source* MongoDB collection.

Corresponding document in *source* collection:
{ 
	"_id" : NumberLong("4152135009"), 
	"name" : "SloppyMath.java", 
	"path" : "/media/ch3njus/Seagate4TB/research/neurosyntax/data/github/java/deeplearning4j/deeplearning4j/deeplearning4j-nn/src/main/java/org/deeplearning4j/berkeley/SloppyMath.java", 
	"funcs" : [ 
				...
				{ 
					"id" : 1138874885, 
					"name" : "max", 
					"header" : "public static float max(float a, float b)", 
					"intype" : [ "float", "float" ], 
					"outtype" : [ "float" ], 
					"source" : "public static float max(float a, float b) {    return (a >= b) ? a : b;  }" 
				}
				...
			  ]
}
```

### Labels
Vector label convention:
The left seven indices represent the input function types and the right seven represent the output types.
Each index position represents a data type and the integer at that position represents how many of those types are contained in the input or output. The represented types are as follows in this exact order for both the input (left seven indices) and output (right seven indices: 
int, double, float, boolean, long short, byte.
e.g. "label" : [ 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0 ]
This vector indicates that there are 2 floats in the input, and 1 float in the output.