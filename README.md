# mokuton

Generates abstract syntax trees from function source code and then inserts it and the input types and output types back into MongoDB.

Dependencies: javalang, pymongo

Refer to https://docs.mongodb.com/getting-started/python/client/ for more info on pymongo

Note:
- All strings are returned as unicode
- javalang parser expects a syntactically correct class, so need a class template to place functions into.

Example:
```
Given 'public class HelloWorld{public static int findFirst(int value, int idx) { value &= ~((1 << idx) - 1); int result = Integer.numberOfTrailingZeros(value);        return (result == 32) ? -1 : result;}}'

Expanded (manually):
public class HelloWorld
{
	public static int findFirst(int value, int idx) 
	{
		value &= ~((1 << idx) - 1);
		int result = Integer.numberOfTrailingZeros(value);
		return (result == 32) ? -1 : result;
	}
}

$ python mokuton.py

(MethodDeclaration (FormalParameter(ReferenceType))(IfStatement(Literal)(BlockStatement (WhileStatement(Literal)(BlockStatement)))(BlockStatement)))

Expanded (manually):
(MethodDeclaration 
	(FormalParameter
		(BasicType)
	)
	(FormalParameter
		(BasicType)
	)
	(StatementExpression
		(Assignment
			(MemberReference)
			(BinaryOperation
				(BinaryOperation
					(Literal)
					(MemberReference)
				)
				(Literal)
			)
		)
	)
	(LocalVariableDeclaration
		(VariableDeclarator
			(MethodInvocation
				(MemberReference)
			)
		)
		(BasicType)
	)
	(ReturnStatement
		(TernaryExpression
			(BinaryOperation
				(MemberReference)
				(Literal)
			)
			(Literal)
			(MemberReference)
		)
	)
	(BasicType)
)
```