# mokuton

Generates abstract syntax trees from function source code and then inserts it and the input types and output types back into MongoDB.

Dependencies: javalang, pymongo

Refer to https://docs.mongodb.com/getting-started/python/client/ for more info on pymongo

Note:
- All strings are returned as unicode
- javalang parser expects a syntactically correct class, so need a class template to place functions into.

Example:
```
Given "public class HelloWorld{public static void main(String args[]){if(true){while(true){}}else{}}}"

$ python mokuton.py

(MethodDeclaration (FormalParameter(ReferenceType))(IfStatement(Literal)(BlockStatement (WhileStatement(Literal)(BlockStatement)))(BlockStatement)))

Expanded (manually):
(MethodDeclaration 
	(FormalParameter
		(ReferenceType)
	)
	(IfStatement
		(Literal)
		(BlockStatement
			(WhileStatement
				(Literal)
				(BlockStatement)
			)
		)
		(BlockStatement)
	)
)
```

### MOKUTON NO JUTSU!!! ![senju](./images/Senju.gif)