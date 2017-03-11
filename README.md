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
```