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
 		 'VariableDeclaration', 'VariableDeclarator', 'VoidClassReference', 'WhileStatement']

# Generated from nodeVect = {k: v for v, k in enumerate(nodes)} and then manually added the rest
nodeVect = {'Annotation': 0, 'AnnotationDeclaration': 1, 'AnnotationMethod': 2, 'ArrayCreator': 3, 
			'ArrayInitializer': 4, 'ArraySelector': 5, 'AssertStatement': 6, 'Assignment': 7, 
			'BasicType': 8, 'BinaryOperation': 9, 'BlockStatement': 10, 'BreakStatement': 11, 
			'Cast': 12, 'CatchClause': 13, 'CatchClauseParameter': 14, 'ClassCreator': 15, 
			'ClassDeclaration': 16, 'ClassReference': 17, 'CompilationUnit': 18, 'ConstantDeclaration': 19, 
			'ConstructorDeclaration': 20, 'ContinueStatement': 21, 'Creator': 22, 'Declaration': 23, 
			'Documented': 24, 'DoStatement': 25, 'ElementArrayValue': 26, 'ElementValuePair': 27, 
			'EnhancedForControl': 28, 'EnumBody': 29, 'EnumConstantDeclaration': 30, 'EnumDeclaration': 31, 
			'ExplicitConstructorInvocation': 32, 'Expression': 33, 'FieldDeclaration': 34, 'ForControl': 35, 
			'FormalParameter': 36, 'ForStatement': 37, 'IfStatement': 38, 'Import': 39, 'InferredFormalParameter': 40, 
			'InnerClassCreator': 41, 'InterfaceDeclaration': 42, 'Invocation': 43, 'LambdaExpression': 44, 'Literal': 45, 
			'LocalVariableDeclaration': 46, 'Member': 47, 'MemberReference': 48, 'MethodDeclaration': 49, 
			'MethodInvocation': 50, 'MethodReference': 51, 'PackageDeclaration': 52, 'Primary': 53, 'ReferenceType': 54, 
			'ReturnStatement': 55, 'Statement': 56, 'StatementExpression': 57, 'SuperConstructorInvocation': 58, 
			'SuperMemberReference': 59, 'SuperMethodInvocation': 60, 'SwitchStatement': 61, 'SwitchStatementCase': 62, 
			'SynchronizedStatement': 63, 'TernaryExpression': 64, 'This': 65, 'ThrowStatement': 66, 'TryResource': 67, 
			'TryStatement': 68, 'Type': 69, 'TypeArgument': 70, 'TypeDeclaration': 71, 'TypeParameter': 72, 
			'VariableDeclaration': 73, 'VariableDeclarator': 74, 'VoidClassReference': 75, 'WhileStatement': 76, 'int':77, 
			'double':78, 'float':79, 'boolean':80, 'long':81, 'short':82, 'byte':83, '(':84, ')':85}