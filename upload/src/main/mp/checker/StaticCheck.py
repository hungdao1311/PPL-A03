"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce

class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype
    def __str__(self):
        return 'MType(['+','.join(str(i) for i in self.partype)+']'+','+str(self.rettype)+')'

class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
        self.value = value
    def __str__(self):
        return 'Symbol('+self.name+','+str(self.mtype)+')'

class StaticChecker(BaseVisitor,Utils):

    global_envi = [Symbol("getInt",MType([],IntType())),
    			   Symbol("putIntLn",MType([IntType()],VoidType())),
                   Symbol("putFloatLn",MType([FloatType()],VoidType())),
                   Symbol("testPrintArr",MType([ArrayType(3,5,IntType())],VoidType()))]
            
    
    def __init__(self,ast):
        self.ast = ast
   
    def check(self):
        return self.visit(self.ast,StaticChecker.global_envi)

    def checkRedeclared(self,sym,kind,env):
        if self.lookup(sym.name,env,lambda x: x.name):
            raise Redeclared(kind,sym.name)
        else: 
            return sym

    def visitProgram(self, ast, c): 
        global_var = []
        for x in ast.decl:
            if type(x) is VarDecl:
                global_var.append(self.checkRedeclared(Symbol(x.variable.name,x.varType),Variable(),global_var))
            elif type(x) is FuncDecl:
                kind = Procedure() if type(x.returnType) is VoidType else Function()
                global_var.append(self.checkRedeclared(Symbol(x.name.name,MType([i.varType for i in x.param],x.returnType)),kind,global_var))   
        res = self.lookup("main",global_var,lambda x: x.name)
        if res is None or len(res.mtype.partype) != 0 or not type(res.mtype.rettype) is VoidType:
            raise NoEntryPoint()
        return reduce(lambda x,y: x + [self.visit(y,[x+c,global_var])], ast.decl, [])

    def visitVarDecl(self, ast, c):
        kind = Parameter() if c[1] == False else Variable()
        return self.checkRedeclared(Symbol(ast.variable.name,ast.varType),kind,c[0])
    

    def visitFuncDecl(self, ast, c): 
        kind = Procedure() if type(ast.returnType) is VoidType else Function()
        tmp = self.checkRedeclared(Symbol(ast.name.name,MType([i.varType for i in ast.param],ast.returnType)),kind,c[0])
        param = reduce(lambda x,y: x + [self.visit(y,(x,False))], ast.param, [])
        local_var = reduce(lambda x,y: x + [self.visit(y,(x,True))], ast.local, param)
        env = [local_var + c[1] + c[0],ast.returnType,False]
        stmt = list(map(lambda x: self.visit(x,env), ast.body))  
        return self.checkRedeclared(Symbol(ast.name.name,MType([i.varType for i in ast.param],ast.returnType)),kind,c[0])

    def checkSameArray(self,a,b):
        return True not in [a.lower != b.lower, a.upper != b.upper, type(a.eleType) != type(b.eleType)]

    def visitCallStmt(self, ast, c): 
        at = [self.visit(x,c[0]) for x in ast.param]

        res = self.lookup(ast.method.name,c[0],lambda x: x.name)
        if res is None or not type(res.mtype) is MType or not type(res.mtype.rettype) is VoidType:
            raise Undeclared(Procedure(),ast.method.name)
        elif len(res.mtype.partype) != len(at) or False in [type(a) == type(b) or (type(a) == IntType and type(b) == FloatType) for a,b in zip(at,res.mtype.partype)]:
            raise TypeMismatchInStatement(ast)
        elif ArrayType in [type(x) for x in at]:
            for a,b in zip(at,res.mtype.partype):
                if type(a) == ArrayType:
                    if not self.checkSameArray(a,b):
                        raise TypeMismatchInStatement(ast)        
        else:
            return res.mtype.rettype
   
    def visitBinaryOp(self, ast, c):
        left_type = type(self.visit(ast.left,c))
        right_type = type(self.visit(ast.right,c))
        if ast.op in ['andthen','orelse','and','or']:
            if left_type is BoolType:
                if right_type is BoolType:
                    return BoolType()
                else:
                    raise TypeMismatchInExpression(ast)
            else: 
                raise TypeMismatchInExpression(ast)
        elif ast.op in ['div','mod']:
            if left_type is IntType:
                if right_type is IntType:
                    return IntType()
                else:
                    raise TypeMismatchInExpression(ast)
            else: 
                raise TypeMismatchInExpression(ast)
        elif ast.op in ['+','-','*','/']:
            if left_type is IntType or left_type is FloatType:
                if right_type is IntType:
                    return self.visit(ast.left,c)
                elif right_type is FloatType:
                    return FloatType()
                else:
                    raise TypeMismatchInExpression(ast)
            else:
                raise TypeMismatchInExpression(ast)
        else: 
            if left_type is IntType or left_type is FloatType:
                if right_type is IntType or right_type is FloatType:
                    return BoolType()
                else:
                    raise TypeMismatchInExpression(ast)
            else:
                raise TypeMismatchInExpression(ast)
    
    def visitUnaryOp(self, ast, c):
        operand_type = type(self.visit(ast.body,c))
        if ast.op == 'not':
            if operand_type is BoolType:
                return BoolType()
            else:
                raise TypeMismatchInExpression(ast)
        elif ast.op == '-':
            if operand_type is FloatType:
                return FloatType()
            elif operand_type is IntType:
                return IntType()
            else:
                raise TypeMismatchInExpression(ast)
    
    def visitCallExpr(self, ast, c):
        at = [self.visit(x,c) for x in ast.param]
        
        res = self.lookup(ast.method.name,c,lambda x: x.name)
        if res is None or not type(res.mtype) is MType or type(res.mtype.rettype) is VoidType:
            raise Undeclared(Function(),ast.method.name)
        elif len(res.mtype.partype) != len(at) or False in [type(a) == type(b) or (type(a) == IntType and type(b) == FloatType) for a,b in zip(at,res.mtype.partype)]:
            raise TypeMismatchInExpression(ast)      
        elif ArrayType in [type(x) for x in at]:
            for a,b in zip(at,res.mtype.partype):
                if type(a) == ArrayType:
                    if not self.checkSameArray(a,b):
                        raise TypeMismatchInExpression(ast)      
        else:
            return res.mtype.rettype
    
    def visitId(self,ast,c):
        res = self.lookup(ast.name,c,lambda x: x.name)
        if res: 
            return res.mtype
        else:
            raise Undeclared(Identifier(),ast.name)
        
    def visitArrayCell(self, ast, c):
        arr = self.visit(ast.arr,c)
        if type(arr) is ArrayType:
            if type(self.visit(ast.idx,c)) is IntType:
                return arr.eleType
            else:
                 raise TypeMismatchInExpression(ast)
        else:
            raise TypeMismatchInExpression(ast)

    def visitAssign(self, ast, c):
        lhs = self.visit(ast.lhs,c[0])
        rhs = self.visit(ast.exp,c[0])
        if type(lhs) is StringType or type(lhs) is ArrayType:
            raise TypeMismatchInStatement(ast)
        else:
            if (type(rhs) is IntType and type(lhs) is FloatType) or type(rhs) == type(lhs):
                return True
            elif type(rhs) != type(lhs):
                raise TypeMismatchInStatement(ast)

    def visitWith(self, ast, c):
        local_var = reduce(lambda x,y: x + [self.visit(y,(x,True))], ast.decl, [])
        env = local_var + c[0]
        return True

    def visitIf(self, ast, c):
        if type(self.visit(ast.expr,c[0])) is not BoolType:
            raise TypeMismatchInStatement(ast)
        stmt = [self.visit(x,c) for x in ast.thenStmt]

    def visitFor(self, ast, c):
        if True in [type(a) != IntType for a in [self.visit(ast.id,c[0]), self.visit(ast.expr1,c[0]), self.visit(ast.expr2,c[0])]]:
            raise TypeMismatchInStatement(ast)

    def visitContinue(self, ast, c):
        if c[2] != True:
            raise ContinueNotInLoop()
    def visitBreak(self, ast, c):
        if c[2] != True:
            raise BreakNotInLoop()

    def visitReturn(self, ast, c):
        if type(c[1]) is VoidType:
            if ast.expr is not None:
                raise TypeMismatchInStatement(ast)
        elif type(c[1]) != type(self.visit(ast.expr,c[0])):
            raise TypeMismatchInStatement(ast)
        elif type(c[1]) is ArrayType:
            if not self.checkSameArray(c[1],self.visit(ast.expr,c[0])):
                raise TypeMismatchInStatement(ast)
        else:
            return True
    def visitWhile(self, ast, c):
        if type(self.visit(ast.exp,c[0])) is not BoolType:
            raise TypeMismatchInStatement(ast)

    def visitIntLiteral(self,ast, c): 
        return IntType()

    def visitFloatLiteral(self,ast,c):
        return FloatType()

    def visitBooleanLiteral(self,ast,c):
        return BoolType()

    def visitStringLiteral(self, ast, c):
        return StringType()
