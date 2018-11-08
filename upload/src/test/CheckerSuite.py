import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    def test_global_var1(self):
        input = Program(
            [
                VarDecl(Id("a"), FloatType()),
                VarDecl(Id("b"), IntType()),
                VarDecl(Id("z"), StringType()),
                FuncDecl(Id("main"), [VarDecl(Id("m"), StringType()),VarDecl(Id("h"), IntType())], [], [])# procedure

            ])
        expect = 'No entry point'
        self.assertTrue(TestChecker.test(input, expect, 300))

    def test_redecl_vardecl(self):
        input = Program(
            [
                VarDecl(Id("a"), FloatType()),
                FuncDecl(Id("main"), [], [], []),# procedure
                VarDecl(Id("a"), IntType()),
            ])
        expect = 'Redeclared Variable: a'
        self.assertTrue(TestChecker.test(input, expect, 301))

    def test_redecl_func(self):
        input = Program(
            [
                VarDecl(Id("a"), FloatType()),
                FuncDecl(Id("main"), [VarDecl(Id("m"), StringType()),VarDecl(Id("h"), IntType())], [], [],IntType()),
                FuncDecl(Id("main"), [VarDecl(Id("m"), StringType()),VarDecl(Id("h"), IntType())], [], [],IntType()),
                FuncDecl(Id("main"), [VarDecl(Id("m"), StringType()),VarDecl(Id("h"), IntType())], [], [])

            ])
        expect = 'Redeclared Function: main'
        self.assertTrue(TestChecker.test(input, expect, 302))

    def test_redecl_proce(self):
        input = Program(
            [
                VarDecl(Id("a"), FloatType()),
                FuncDecl(Id("main"), [VarDecl(Id("m"), StringType()),VarDecl(Id("h"), IntType())], [], [],IntType()),
                FuncDecl(Id("main"), [VarDecl(Id("m"), StringType()),VarDecl(Id("h"), IntType())], [], []),
                FuncDecl(Id("main"), [VarDecl(Id("h"), IntType())], [], []),
                FuncDecl(Id("main1s"), [VarDecl(Id("m"), StringType()),VarDecl(Id("h"), IntType())], [], [],IntType()),
            ])
        expect = 'Redeclared Procedure: main'
        self.assertTrue(TestChecker.test(input, expect, 303))

    def test_q3_float(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[IntLiteral(1)]),
                    CallStmt(Id("putIntLn"),[FloatLiteral(2.3)])
                ])
        ])
        expect = 'Type Mismatch In Statement: CallStmt(Id(putIntLn),[FloatLiteral(2.3)])'
        self.assertTrue(TestChecker.test(input,expect,304))

    def test_BinOp1(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp("+",StringLiteral("2.3"),IntLiteral(2))])
                ])
        ])
        expect = 'Type Mismatch In Expression: BinaryOp(+,StringLiteral(2.3),IntLiteral(2))'
        self.assertTrue(TestChecker.test(input,expect,305))
    
    def test_BinOp2(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp("div",FloatLiteral(2.3),IntLiteral(2))])
                ])
        ])
        expect = 'Type Mismatch In Expression: BinaryOp(div,FloatLiteral(2.3),IntLiteral(2))'
        self.assertTrue(TestChecker.test(input,expect,306))

    def test_BinOp3(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp("andthen",BooleanLiteral(True),IntLiteral(2))])
                ])
        ])
        expect = 'Type Mismatch In Expression: BinaryOp(andthen,BooleanLiteral(True),IntLiteral(2))'
        self.assertTrue(TestChecker.test(input,expect,307))

    def test_BinOp4(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp("div",IntLiteral(2),FloatLiteral(2.3))])
                ])
        ])
        expect = 'Type Mismatch In Expression: BinaryOp(div,IntLiteral(2),FloatLiteral(2.3))'
        self.assertTrue(TestChecker.test(input,expect,308))

    
    def test_UnOp2(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[UnaryOp("not",FloatLiteral(2.3))])
                ])
        ])
        expect = 'Type Mismatch In Expression: UnaryOp(not,FloatLiteral(2.3))'
        self.assertTrue(TestChecker.test(input,expect,310))

    def test_arrayCell(self):
        input = Program([
                FuncDecl(Id("main"),[],[VarDecl(Id("a"),ArrayType(2,5,FloatType()))],[
                    CallStmt(Id("putIntLn"),[ArrayCell(Id("a"),IntLiteral(4))])
                ])
        ])
        expect = 'Type Mismatch In Statement: CallStmt(Id(putIntLn),[ArrayCell(Id(a),IntLiteral(4))])'
        self.assertTrue(TestChecker.test(input,expect,311))

    def test_FunCall(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putFloatLn"),[StringLiteral("4")])
                ])
        ])
        expect = 'Type Mismatch In Statement: CallStmt(Id(putFloatLn),[StringLiteral(4)])'
        self.assertTrue(TestChecker.test(input,expect,312))
    
    def test_FunCall2(self):
        input = Program([
                FuncDecl(Id("main"),[],[VarDecl(Id("a"),ArrayType(3,5,FloatType()))],[
                    CallStmt(Id("testPrintArr"),[Id("a")])
                ])
        ])
        expect = 'Type Mismatch In Statement: CallStmt(Id(testPrintArr),[Id(a)])'
        self.assertTrue(TestChecker.test(input,expect,313))

    def test_GlobalVar(self):
        input = Program(
            [
                VarDecl(Id("a"), FloatType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[Id("b")]),
                    CallStmt(Id("putIntLn"),[Id("c")])
                ]),# procedure
                VarDecl(Id("b"), IntType()),
            ])
        expect = 'Undeclared Identifier: c'
        self.assertTrue(TestChecker.test(input, expect, 314))

# Redeclared Variable: 5
    def test_redeclared_variable_1(self):
        """Simple program: int main() {} """
        input = """
        
var conbocuoi1, conbocuoi2:integer;

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
    conbocuoi2:string;
begin 
    return;
end
"""
        expect = "Redeclared Variable: conbocuoi2"
        self.assertTrue(TestChecker.test(input,expect,400))
        
    def test_redeclared_variable_2(self):
        """Simple program: int main() {} """
        input = """
        
var conbocuoi1, conbocuoi2:integer;

function conbocuoi4(conbocuoi5:integer):integer;
var conbocuoi1:integer;
    conbocuoi1:real;
begin
    return 0;
end

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
    conbocuoi2:string;
begin 
    return;
end
"""
        expect = "Redeclared Variable: conbocuoi1"
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_redeclared_variable_3(self):
        """Simple program: int main() {} """
        input = """
        
var conbocuoi3, conbocuoi2:integer;
    conbocuoi3:array [1 .. 10] of real;
procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
    conbocuoi2:string;
begin 
    return;
end
"""
        expect = "Redeclared Variable: conbocuoi3"
        self.assertTrue(TestChecker.test(input,expect,402))
    
    def test_redeclared_variable_4(self):
        input = """
var conbocuoi1, conbocuoi2:integer;

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
    conbocuoi3:string;
begin
    with conbocuoi4:integer;
         conbocuoi4:array [1 .. 2] of real;
    do
        conbocuoi4 := 10;

    return;
end
"""
        expect = "Redeclared Variable: conbocuoi4"
        self.assertTrue(TestChecker.test(input,expect,403))
    
    def test_redeclared_variable_5(self):
        input = """
        
var conbocuoi5, conbocuoi2, conbocuoi3, conbocuoi5:integer;

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
    conbocuoi2:string;
begin 
    return;
end
"""
        expect = "Redeclared Variable: conbocuoi5"
        self.assertTrue(TestChecker.test(input,expect,404))
        
    
# Redeclared Function: 5
    def test_redeclared_function_1(self):
        input = """
var conbocuoi1, conbocuoi2:integer;

function conbocuoi1(hihi:integer):integer;
begin
    return 10;
end

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
begin 
    conbocuoi1();
end
"""
        expect = "Redeclared Function: conbocuoi1"
        self.assertTrue(TestChecker.test(input,expect,405))
        
    def test_redeclared_function_2(self):
        input = """
        
var conbocuoi1:integer;

procedure conbocuoi2();
begin
    return;
end

function conbocuoi2():integer;
begin
    return 10;
end

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
    conbocuoi2:string;
begin 
    return;
end
"""
        expect = "Redeclared Function: conbocuoi2"
        self.assertTrue(TestChecker.test(input,expect,406))

    def test_redeclared_function_3(self):
        input = """
        
var conbocuoi1:integer;

procedure conbocuoi2();
begin
    return;
end

function conbocuoi3():integer;
begin
    return 10;
end

function conbocuoi3():integer;
begin
    return 100;
end

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
    conbocuoi2:string;
begin 
    return;
end
"""
        expect = "Redeclared Function: conbocuoi3"
        self.assertTrue(TestChecker.test(input,expect,407))
        
    def test_redeclared_function_4(self):
        input = """
        
var conbocuoi4:integer;

procedure conbocuoi2();
begin
    return;
end

function conbocuoi3():integer;
begin
    return 10;
end

function conbocuoi4():integer;
begin
    return 100;
end

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
    conbocuoi2:string;
begin
    return;
end

procedure conbocuoi4();
begin
    return;
end
"""
        expect = "Redeclared Function: conbocuoi4"
        self.assertTrue(TestChecker.test(input,expect,408))
        
    def test_redeclared_function_5(self):
        input = """
        
var conbocuoi4:integer;

function conbocuoi3():integer;
begin
    return conbocuoi4();
end

function conbocuoi6():integer;
begin
    return 100;
end

procedure conbocuoi5();
begin
    return;
end

function conbocuoi5():integer;
begin
    return 100;
end

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
    conbocuoi2:string;
begin
    return;
end
"""
        expect = "Redeclared Function: conbocuoi5"
        self.assertTrue(TestChecker.test(input,expect,409))
        
# Redeclared Procedure: 5
    def test_redeclared_procedure_1(self):
        input = """
        
var conbocuoi1, conbocuoi2:integer;

procedure conbocuoi1(hihi:integer);
begin
    return;
end

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
begin 
    conbocuoi1();
end
"""
        expect = "Redeclared Procedure: conbocuoi1"
        self.assertTrue(TestChecker.test(input,expect,410))
        
    def test_redeclared_procedure_2(self):
        input = """
        
var conbocuoi1:integer;

procedure conbocuoi2();
begin
    return;
end

procedure conbocuoi2();
begin
    return;
end

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
    conbocuoi3:string;
begin 
    return;
end
"""
        expect = "Redeclared Procedure: conbocuoi2"
        self.assertTrue(TestChecker.test(input,expect,411))

    def test_redeclared_procedure_3(self):
        input = """
        
var conbocuoi1:integer;

procedure conbocuoi2();
begin
    return;
end

function conbocuoi3():integer;
begin
    return 10;
end

procedure conbocuoi3();
begin
    return;
end

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
    conbocuoi3:string;
begin 
    return;
end
"""
        expect = "Redeclared Procedure: conbocuoi3"
        self.assertTrue(TestChecker.test(input,expect,412))
        
    def test_redeclared_procedure_4(self):
        input = """
        
var conbocuoi4:integer;

procedure conbocuoi2();
begin
    return;
end

function conbocuoi3():integer;
begin
    return 10;
end

procedure conbocuoi4();
begin
    return;
end

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
    conbocuoi3:string;
begin
    return;
end

function conbocuoi4():integer;
begin
    return 100;
end
"""
        expect = "Redeclared Procedure: conbocuoi4"
        self.assertTrue(TestChecker.test(input,expect,413))
        
    def test_redeclared_procedure_5(self):
        input = """
        
var conbocuoi4:integer;

function conbocuoi3():integer;
begin
    return conbocuoi4();
end

function conbocuoi6():integer;
begin
    return 100;
end

procedure conbocuoi5();
begin
    return;
end

procedure conbocuoi5();
begin
    return;
end

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
    conbocuoi3:string;
begin
    return;
end
"""
        expect = "Redeclared Procedure: conbocuoi5"
        self.assertTrue(TestChecker.test(input,expect,414))
        

# Redeclared Parameter: 5
    def test_redeclared_parameter_1(self):
        input = """
var conbocuoi4:integer;

function conbocuoi3(conbocuoi1:string; conbocuoi1:integer):integer;
begin
    return conbocuoi4;
end

function conbocuoi6():integer;
begin
    return 100;
end

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
    conbocuoi3:string;
begin
    return;
end
"""
        expect = "Redeclared Parameter: conbocuoi1"
        self.assertTrue(TestChecker.test(input,expect,415))
        
#     def test_redeclared_parameter_2(self):
#         input = """
# var conbocuoi4:integer;

# function conbocuoi3(conbocuoi1:string; conbocuoi2:integer):integer;
# begin
#     return conbocuoi6(1, "conbocuoi");
# end

# function conbocuoi6(conbocuoi2:integer; conbocuoi2:string):integer;
# begin
#     return 100;
# end

# procedure main(); 
# var conbocuoi1:integer;
#     conbocuoi2:real;
#     conbocuoi3:string;
# begin
#     return;
# end
# """
#         expect = "Redeclared Parameter: conbocuoi2"
#         self.assertTrue(TestChecker.test(input,expect,416))
        
    def test_redeclared_parameter_3(self):
        input = """
var conbocuoi4:integer;

function conbocuoi3(conbocuoi1:string; conbocuoi3:integer; conbocuoi3:real):integer;
begin
    return conbocuoi4;
end

function conbocuoi6():integer;
begin
    return 100;
end

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
    conbocuoi3:string;
begin
    return;
end
"""
        expect = "Redeclared Parameter: conbocuoi3"
        self.assertTrue(TestChecker.test(input,expect,417))
        
    def test_redeclared_parameter_4(self):
        input = """
var conbocuoi4:integer;

function conbocuoi3(conbocuoi1:string; conbocuoi4:integer):integer;
begin
    return conbocuoi4;
end

procedure conbocuoi6(conbocuoi4:array [1 .. 100] of real; conbocuoi4:string);
begin
    return;
end

procedure main(); 
var conbocuoi1:integer;
    conbocuoi2:real;
    conbocuoi3:string;
begin
    return;
end
"""
        expect = "Redeclared Parameter: conbocuoi4"
        self.assertTrue(TestChecker.test(input,expect,418))
        
    def test_redeclared_parameter_5(self):
        input = """
var a, b, c:integer;
var d:boolean;
var e:real;
var m: array [1 .. 100] of integer;
function foo():integer; begin  return 0; end
procedure main(); begin 
	b := foo();
	d := true;
	a := m[0] + 1;
	c := m[d] + 1;
	return ;
end
"""
        expect = "Type Mismatch In Expression: ArrayCell(Id(m),Id(d))"
        self.assertTrue(TestChecker.test(input,expect,419))
    
    def test_333(self):
        input = """
        var a:integer;
var b:real;
var m:array[1 .. 10] of integer;
procedure main(); begin 
	b := m[1] + -1;
	b := b * (1.0 + 1);
	b := not (m[1] = 1);
	return ;
end


        """
        expect ="Type Mismatch In Statement: AssignStmt(Id(b),UnaryOp(not,BinaryOp(=,ArrayCell(Id(m),IntLiteral(1)),IntLiteral(1))))"
        self.assertTrue(TestChecker.test(input,expect,420))
    
    def test_444(self):
        input = """function foo():integer;
var a:integer;
begin  
	a := 4;
	if (a = 10) then begin 
		return 1; 
	end
	return 10;
end

procedure main(); 
var a:integer;
begin 
	a := 0;
  
	if (foo() > 1) then begin 
		if(foo2() <= 100) then

			return ; 
		else
			return ;  
	end 
	else begin 
		a := 2;
		return ;
	end
end"""
        expect ="Undeclared Function: foo2"
        self.assertTrue(TestChecker.test(input,expect,421))
        