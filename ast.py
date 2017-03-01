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
	- Parser expects a syntactically correct class, so need a class template to place functions into.

'''

nodes = '''
CompilationUnit(Node)
Import(Node)
Documented(Node)
Declaration(Node)
Type(Node)
TypeArgument(Node)
TypeParameter(Node)
Annotation(Node)
ElementValuePair(Node)
ElementArrayValue(Node)
ArrayInitializer(Node)
VariableDeclarator(Node)
InferredFormalParameter(Node)
Statement(Node)
SwitchStatementCase(Node)
ForControl(Node)
EnhancedForControl(Node)
Expression(Node)
EnumBody(Node)
VariableDeclaration(Declaration)
FormalParameter(Declaration)
TryResource(Declaration)
CatchClauseParameter(Declaration)
AnnotationMethod(Declaration)
BasicType(Type)
ReferenceType(Type)
TypeDeclaration(Declaration, Documented)
PackageDeclaration(Declaration, Documented)
ConstructorDeclaration(Declaration, Documented)
EnumConstantDeclaration(Declaration, Documented)
ClassDeclaration(TypeDeclaration)
EnumDeclaration(TypeDeclaration)
InterfaceDeclaration(TypeDeclaration)
AnnotationDeclaration(TypeDeclaration)
Member(Documented)
MethodDeclaration(Member, Declaration)
FieldDeclaration(Member, Declaration)
ConstantDeclaration(FieldDeclaration)
LocalVariableDeclaration(VariableDeclaration)
IfStatement(Statement)
WhileStatement(Statement)
DoStatement(Statement)
ForStatement(Statement)
AssertStatement(Statement)
BreakStatement(Statement)
ContinueStatement(Statement)
ReturnStatement(Statement)
ThrowStatement(Statement)
SynchronizedStatement(Statement)
TryStatement(Statement)
SwitchStatement(Statement)
BlockStatement(Statement)
StatementExpression(Statement)
CatchClause(Statement)
Assignment(Expression)
TernaryExpression(Expression)
BinaryOperation(Expression)
Cast(Expression)
MethodReference(Expression)
LambdaExpression(Expression)
Primary(Expression)
ArraySelector(Expression)
Literal(Primary)
This(Primary)
MemberReference(Primary)
Invocation(Primary)
SuperMemberReference(Primary)
ClassReference(Primary)
Creator(Primary)
ExplicitConstructorInvocation(Invocation)
SuperConstructorInvocation(Invocation)
MethodInvocation(Invocation)
SuperMethodInvocation(Invocation)
VoidClassReference(ClassReference)
ArrayCreator(Creator)
ClassCreator(Creator)
InnerClassCreator(Creator)
'''

nodes = [s.strip().split('(')[0] for s in nodes.splitlines() if len(s.strip()) > 0]