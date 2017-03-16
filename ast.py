'''
	mokuton.py
	2.24.17

	Generates abstract syntax trees from function source code and then inserts it and the 
	input types and output types back into MongoDB.
	
	Dependencies: javalang, pymongo

	Refer to https://docs.mongodb.com/getting-started/python/client/ for more info on pymongo
	
	Note:
	- All strings are returned as unicode
	- Parser expects a syntactically correct class, so need a class template to place functions into.

'''

nodes = ['Annotation', 'AnnotationDeclaration', 'AnnotationMethod', 'ArrayCreator', 
 		 'ArrayInitializer', 'ArraySelector', 'AssertStatement', 'Assignment', 
 		 'BasicType', 'BinaryOperation', 'BlockStatement', 'BreakStatement', 'Cast', 
 		 'CatchClause', 'CatchClauseParameter', 'ClassCreator', 'ClassDeclaration', 
 		 'ClassReference', 'CompilationUnit', 'ConstantDeclaration', 'ConstructorDeclaration', 
 		 'ContinueStatement', 'Creator', 'Declaration', 'Documented', 'DoStatement', 
 		 'ElementArrayValue', 'ElementValuePair', 'EnhancedForControl', 'EnumBody', 
 		 'EnumConstantDeclaration', 'EnumDeclaration', 'ExplicitConstructorInvocation', 
 		 'Expression', 'FieldDeclaration', 'ForControl', 'FormalParameter', 'ForStatement', 
 		 'IfStatement', 'Import', 'InferredFormalParameter', 'InnerClassCreator', 
 		 'InterfaceDeclaration', 'Invocation', 'LambdaExpression', 'Literal', 
 		 'LocalVariableDeclaration', 'Member', 'MemberReference', 'MethodDeclaration', 
 		 'MethodInvocation', 'MethodReference', 'PackageDeclaration', 'Primary', 'ReferenceType', 
 		 'ReturnStatement', 'Statement', 'StatementExpression', 'SuperConstructorInvocation', 
 		 'SuperMemberReference', 'SuperMethodInvocation', 'SwitchStatement', 'SwitchStatementCase', 
 		 'SynchronizedStatement', 'TernaryExpression', 'This', 'ThrowStatement', 'TryResource', 
 		 'TryStatement', 'Type', 'TypeArgument', 'TypeDeclaration', 'TypeParameter', 
 		 'VariableDeclaration', 'VariableDeclarator', 'VoidClassReference', 'WhileStatement',
 		 'int', 'double', 'float', 'boolean', 'long', 'short', 'byte', '(', ')']

nodeVect = {k: v for v, k in enumerate(nodes)}