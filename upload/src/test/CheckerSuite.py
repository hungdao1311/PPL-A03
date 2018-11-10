import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):

# Redeclared Variable: 5
    def test_global_var(self):
        input = Program(
            [
                VarDecl(Id("a"), FloatType()),
                VarDecl(Id("b"), IntType()),
                VarDecl(Id("z"), StringType()),
                FuncDecl(Id("main"), [VarDecl(Id("m"), StringType()),VarDecl(Id("h"), IntType())], [], [])# procedure
             ])
        expect = 'No entry point'
        self.assertTrue(TestChecker.test(input, expect, 300))
    def test_redecl_vardecl1(self):
        input = Program(
            [
                VarDecl(Id("a"), FloatType()),
                FuncDecl(Id("main"), [], [], []),# procedure
                VarDecl(Id("a"), IntType()),
            ])
        expect = 'Redeclared Variable: a'
        self.assertTrue(TestChecker.test(input, expect, 301))
    def test_redecl_func2(self):
        input = Program(
            [
                VarDecl(Id("a"), FloatType()),
                FuncDecl(Id("main"), [VarDecl(Id("m"), StringType()),VarDecl(Id("h"), IntType())], [], [],IntType()),
                FuncDecl(Id("main"), [VarDecl(Id("m"), StringType()),VarDecl(Id("h"), IntType())], [], [],IntType()),
                FuncDecl(Id("main"), [VarDecl(Id("m"), StringType()),VarDecl(Id("h"), IntType())], [], [])
             ])
        expect = 'Redeclared Function: main'
        self.assertTrue(TestChecker.test(input, expect, 302))
    def test_redecl_proce3(self):
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
    def test_q3_float4(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[IntLiteral(1)]),
                    CallStmt(Id("putIntLn"),[FloatLiteral(2.3)])
                ])
        ])
        expect = 'Type Mismatch In Statement: CallStmt(Id(putIntLn),[FloatLiteral(2.3)])'
        self.assertTrue(TestChecker.test(input,expect,304))
    def test_BinOp5(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp("+",StringLiteral("2.3"),IntLiteral(2))])
                ])
        ])
        expect = 'Type Mismatch In Expression: BinaryOp(+,StringLiteral(2.3),IntLiteral(2))'
        self.assertTrue(TestChecker.test(input,expect,305))
    
    def test_BinOp6(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp("div",FloatLiteral(2.3),IntLiteral(2))])
                ])
        ])
        expect = 'Type Mismatch In Expression: BinaryOp(div,FloatLiteral(2.3),IntLiteral(2))'
        self.assertTrue(TestChecker.test(input,expect,306))
    def test_BinOp7(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp("andthen",BooleanLiteral(True),IntLiteral(2))])
                ])
        ])
        expect = 'Type Mismatch In Expression: BinaryOp(andthen,BooleanLiteral(True),IntLiteral(2))'
        self.assertTrue(TestChecker.test(input,expect,307))
    def test_BinOp8(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp("div",IntLiteral(2),FloatLiteral(2.3))])
                ])
        ])
        expect = 'Type Mismatch In Expression: BinaryOp(div,IntLiteral(2),FloatLiteral(2.3))'
        self.assertTrue(TestChecker.test(input,expect,308))
    
    def test_BinOp9(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putFloatLn"),[BinaryOp("+",IntLiteral(2),IntLiteral(2))]),
                    CallStmt(Id("putFloatLn"),[BinaryOp("div",FloatLiteral(2),IntLiteral(2))])
                ])
        ])
        expect = 'Type Mismatch In Expression: BinaryOp(div,FloatLiteral(2),IntLiteral(2))'
        self.assertTrue(TestChecker.test(input,expect,309))
    def test_UnOp10(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[UnaryOp("not",FloatLiteral(2.3))])
                ])
        ])
        expect = 'Type Mismatch In Expression: UnaryOp(not,FloatLiteral(2.3))'
        self.assertTrue(TestChecker.test(input,expect,310))
    def test_arrayCell11(self):
        input = Program([
                FuncDecl(Id("main"),[],[VarDecl(Id("a"),ArrayType(2,5,FloatType()))],[
                    CallStmt(Id("putIntLn"),[ArrayCell(Id("a"),IntLiteral(4))])
                ])
        ])
        expect = 'Type Mismatch In Statement: CallStmt(Id(putIntLn),[ArrayCell(Id(a),IntLiteral(4))])'
        self.assertTrue(TestChecker.test(input,expect,311))
    def test_FunCall12(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putFloatLn"),[StringLiteral("4")])
                ])
        ])
        expect = 'Type Mismatch In Statement: CallStmt(Id(putFloatLn),[StringLiteral(4)])'
        self.assertTrue(TestChecker.test(input,expect,312))
    
    def test_FunCall13(self):
        input = Program([
                FuncDecl(Id("main"),[],[VarDecl(Id("a"),ArrayType(3,5,FloatType()))],[
                    CallStmt(Id("testPrintArr"),[Id("a")])
                ])
        ])
        expect = 'Undeclared Procedure: testPrintArr'
        self.assertTrue(TestChecker.test(input,expect,313))

    def test_UnOp14(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putboolLn"),[UnaryOp("not",IntLiteral(2))])
                ])
        ])
        expect = 'Type Mismatch In Expression: UnaryOp(not,IntLiteral(2))'
        self.assertTrue(TestChecker.test(input,expect,314))

    def test_UnOp15(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putboolLn"),[UnaryOp("-",IntLiteral(2))])
                ])
        ])
        expect = 'Type Mismatch In Statement: CallStmt(Id(putboolLn),[UnaryOp(-,IntLiteral(2))])'
        self.assertTrue(TestChecker.test(input,expect,315))
    
    def test_BinOp16(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putFloatLn"),[BinaryOp("+",IntLiteral(2),IntLiteral(2))]),
                    CallStmt(Id("putFloatLn"),[BinaryOp("/",IntLiteral(2),IntLiteral(2))]),
                    CallStmt(Id("putIntLn"),[BinaryOp("/",IntLiteral(2),IntLiteral(2))])
                ])
        ])
        expect = 'Type Mismatch In Statement: CallStmt(Id(putIntLn),[BinaryOp(/,IntLiteral(2),IntLiteral(2))])'
        self.assertTrue(TestChecker.test(input,expect,316))
    
    def test_BinOp17(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putBoolLn"),[UnaryOp("not",BinaryOp(">",IntLiteral(2),IntLiteral(2)))]),
                    CallStmt(Id("putIntLn"),[BinaryOp("-",StringLiteral("2"),IntLiteral(2))])
                ])
        ])
        expect = 'Type Mismatch In Expression: BinaryOp(-,StringLiteral(2),IntLiteral(2))'
        self.assertTrue(TestChecker.test(input,expect,317))
    
    def test_redeclared_par18(self):
        input = """
var c4:integer;

function c3(c1:string; c1:integer):integer;
begin
    return c4;
end



procedure main(); 
var c1:integer;
    c2:real;
    c3:string;
begin
 
end
"""
        expect = "Redeclared Parameter: c1"
        self.assertTrue(TestChecker.test(input,expect,318))

    def test_redecl_var19(self):
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
        self.assertTrue(TestChecker.test(input,expect,319))

    def test_redecl_var20(self):
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
        self.assertTrue(TestChecker.test(input,expect,320))
    
    def test_built_in21(self):
        input = Program([
                FuncDecl(Id("main"),[],[VarDecl(Id("a"),IntType())],[
                    Assign(Id("a"),CallExpr(Id("getint"),[])),
                    CallStmt(Id("putFloatLna"),[BinaryOp("/",IntLiteral(2),IntLiteral(2))]),
                ])
        ])
        expect = 'Undeclared Procedure: putFloatLna'
        self.assertTrue(TestChecker.test(input,expect,321))
    
    def test_built_in22(self):
        input = Program([
                FuncDecl(Id("main"),[],[VarDecl(Id("a"),FloatType())],[
                    Assign(Id("a"),CallExpr(Id("getint"),[])),
                    CallStmt(Id("putLna"),[]),
                ])
        ])
        expect = 'Undeclared Procedure: putLna'
        self.assertTrue(TestChecker.test(input,expect,322))

    def test_built_in23(self):
        input = Program([
                FuncDecl(Id("main"),[],[VarDecl(Id("a"),FloatType()),VarDecl(Id("b"),StringType())],[
                    Assign(Id("a"),CallExpr(Id("getint"),[])),
                    CallStmt(Id("putstring"),[Id("b")]),
                    CallStmt(Id("putstr"),[])
                ])
        ])
        expect = 'Undeclared Procedure: putstr'
        self.assertTrue(TestChecker.test(input,expect,323))

    def test_built_in24(self):
        input = Program([
                FuncDecl(Id("main"),[],[VarDecl(Id("a"),FloatType()),VarDecl(Id("b"),StringType())],[
                    Assign(Id("a"),CallExpr(Id("getint"),[])),
                    CallStmt(Id("putstring"),[Id("b")]),
                    CallStmt(Id("putln"),[]),
                    CallStmt(Id("d"),[])
                ])
        ])
        expect = 'Undeclared Procedure: d'
        self.assertTrue(TestChecker.test(input,expect,324))
    
    def test_global25(self):
        input = Program([VarDecl(Id("a"),FloatType()),
                FuncDecl(Id("main"),[],[],[
                    Assign(Id("a"),CallExpr(Id("getint"),[])),
                    CallStmt(Id("putstring"),[Id("b")]),
                    CallStmt(Id("putln"),[]),
                    CallStmt(Id("d"),[])
                ]),
                VarDecl(Id("b"),StringType())
        ])
        expect = 'Undeclared Procedure: d'
        self.assertTrue(TestChecker.test(input,expect,325))
    
    def test_noentry26(self):
        input = Program([VarDecl(Id("a"),FloatType()),
                FuncDecl(Id("maine"),[],[],[
                    Assign(Id("a"),CallExpr(Id("getint"),[])),
                    CallStmt(Id("putstring"),[Id("b")]),
                    CallStmt(Id("putln"),[]),
                    CallStmt(Id("d"),[])
                ]),
                VarDecl(Id("b"),StringType())
        ])
        expect = 'No entry point'
        self.assertTrue(TestChecker.test(input,expect,326))
    
    def test_noentry27(self):
        input = Program([VarDecl(Id("a"),FloatType()),
                FuncDecl(Id("main"),[VarDecl(Id("d"),FloatType())],[],[
                    Assign(Id("a"),CallExpr(Id("getint"),[])),
                    CallStmt(Id("putstring"),[Id("b")]),
                    CallStmt(Id("putln"),[]),
                    CallStmt(Id("d"),[])
                ]),
                VarDecl(Id("b"),StringType())
        ])
        expect = 'No entry point'
        self.assertTrue(TestChecker.test(input,expect,327))
    
    def test_undecl28(self):
        input = Program([
                FuncDecl(Id("main"),[],[VarDecl(Id("a"),FloatType()),VarDecl(Id("b"),StringType())],[
                    Assign(Id("a"),CallExpr(Id("getintel"),[])),
                    CallStmt(Id("putstring"),[Id("b")]),
                ])
        ])
        expect = 'Undeclared Function: getintel'
        self.assertTrue(TestChecker.test(input,expect,328))
    
    def test_undecl29(self):
        input = Program([
                FuncDecl(Id("main"),[],[VarDecl(Id("a"),FloatType()),VarDecl(Id("b"),StringType())],[
                    Assign(Id("a"),CallExpr(Id("getnt"),[])),
                    CallStmt(Id("putstring"),[Id("b")]),
                ])
        ])
        expect = 'Undeclared Function: getnt'
        self.assertTrue(TestChecker.test(input,expect,329))
    
    def test_BinOp30(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putBoolLn"),[UnaryOp("not",BinaryOp("andthen",IntLiteral(2),IntLiteral(2)))]),
                    CallStmt(Id("putIntLn"),[])
                ])
        ])
        expect = 'Type Mismatch In Expression: BinaryOp(andthen,IntLiteral(2),IntLiteral(2))'
        self.assertTrue(TestChecker.test(input,expect,330))
    
    def test_BinOp31(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putBoolLn"),[UnaryOp("not",BinaryOp("orelse",IntLiteral(2),IntLiteral(2)))]),
                    CallStmt(Id("putIntLn"),[])
                ])
        ])
        expect = 'Type Mismatch In Expression: BinaryOp(orelse,IntLiteral(2),IntLiteral(2))'
        self.assertTrue(TestChecker.test(input,expect,331))
    
    def test_BinOp32(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putBoolLn"),[UnaryOp("not",BinaryOp("orelse",IntLiteral(2),IntLiteral(2)))]),
                    CallStmt(Id("putIntLn"),[])
                ])
        ])
        expect = 'Type Mismatch In Expression: BinaryOp(orelse,IntLiteral(2),IntLiteral(2))'
        self.assertTrue(TestChecker.test(input,expect,332))
    
    def test_BinOp33(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putBoolLn"),[UnaryOp("not",BinaryOp("and",IntLiteral(2),IntLiteral(2)))]),
                    CallStmt(Id("putIntLn"),[])
                ])
        ])
        expect = 'Type Mismatch In Expression: BinaryOp(and,IntLiteral(2),IntLiteral(2))'
        self.assertTrue(TestChecker.test(input,expect,333))
    
    def test_BinOp34(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putBoolLn"),[UnaryOp("not",BinaryOp("or",IntLiteral(2),IntLiteral(2)))]),
                    CallStmt(Id("putIntLn"),[])
                ])
        ])
        expect = 'Type Mismatch In Expression: BinaryOp(or,IntLiteral(2),IntLiteral(2))'
        self.assertTrue(TestChecker.test(input,expect,334))
    
    def test_BinOp35(self):
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putBoolLn"),[UnaryOp("not",BinaryOp("or",BooleanLiteral(True),BooleanLiteral(False)))]),
                    CallStmt(Id("putInLn"),[])
                ])
        ])
        expect = 'Undeclared Procedure: putInLn'
        self.assertTrue(TestChecker.test(input,expect,335))
    def test_for36(self):
        input = """
                var a: real;
                procedure main();
                var i,j:integer;
                begin
                    for a := 1 to 10 do begin
                        for j := i downto 1 do
                            if (i + j) mod 1 = 1 then break;
                    end
                end
            """
        expect = "Type Mismatch In Statement: For(Id(a)IntLiteral(1),IntLiteral(10),True,[For(Id(j)Id(i),IntLiteral(1),False,[If(BinaryOp(=,BinaryOp(mod,BinaryOp(+,Id(i),Id(j)),IntLiteral(1)),IntLiteral(1)),[Break],[])])])"
        self.assertTrue(TestChecker.test(input, expect, 336))
    
    def test_while37(self):
        input = """
                var a: real;
                procedure main();
                var i,j:integer;
                begin
                    while i do j := i;
                end
            """
        expect = "Type Mismatch In Statement: While(Id(i),[AssignStmt(Id(j),Id(i))])"
        self.assertTrue(TestChecker.test(input, expect, 337))
    
    def test_return38(self):
        input = """
                var a: real;
                procedure main();
                var i,j:integer;
                k:boolean;
                begin
                    return 3;
                end
            """
        expect = "Type Mismatch In Statement: Return(Some(IntLiteral(3)))"
        self.assertTrue(TestChecker.test(input, expect, 338))
    
    def test_return39(self):
        input = """
                var a: real;
                procedure main();
                var i,j:integer;
                k:boolean;
                begin
                end
                function foo():array [1 .. 5] of real;
                var a:array[1 .. 5] of integer;
                begin
                return a ;
                end
            """
        expect = "Type Mismatch In Statement: Return(Some(Id(a)))"
        self.assertTrue(TestChecker.test(input, expect, 339))
    
    def test_funcall40(self):
        input = """
Var name, surname: String;
Procedure main();
Begin
	write("Enter your name:");
	readln(name);
	writeln("Your name is: ",name);
	readln();
End
        """
        expect ="Undeclared Procedure: write"
        self.assertTrue(TestChecker.test(input, expect, 340))
    
    def test_global41(self):
        input = """
procedure main();
                
                begin
                    while true do putstring(a);
                    b:=2;
    
                end
                var a:String;
        """
        expect ="Undeclared Identifier: b"
        self.assertTrue(TestChecker.test(input, expect, 341))

    def test_with42(self):
        input ="""var i : integer;
        function f(): integer;
        begin
        return 200;
        end
        procedure main();
        var
            main: integer;
        begin
            main := f();
            putintln(main);
            with 
                i: integer;
                main: integer;
                f: integer;
            do  begin 
                main := f := i := 100;
                putIntLn();
                putIntLn(f);
                putIntLn(i);
                end
                putintlN(main);
        end
            var g: real;

        """
        expect ="Type Mismatch In Statement: CallStmt(Id(putIntLn),[])"
        self.assertTrue(TestChecker.test(input, expect, 342))

    def test_func43(self):
        input = """
        fUnCTiOn foo(): integer;
        var a,b: integer;
        begin
            a := a+b;
            bar(a);
        end"""
        expect = 'No entry point'
        self.assertTrue(TestChecker.test(input, expect, 343))

    def test_func44(self):
        input = """
var check : Boolean;
    abc   : String;
Procedure main();
Begin
    While (True) Do
    Begin
        reAdLn(abc);
    End
End
        """
        expect = 'Undeclared Procedure: reAdLn'
        self.assertTrue(TestChecker.test(input, expect, 344))
    def test_func45(self):
        input = """
Var 
	bool : Boolean;
	A, B : Integer;
Procedure main();
Begin
	A := 10;
	B := 30;
	bool := False;
	bool := (A = 10) OR (B = 10);
	bool := (A = 10) AND (B = 10);
    return true;
End
        """
        expect = 'Type Mismatch In Statement: Return(Some(BooleanLiteral(True)))'
        self.assertTrue(TestChecker.test(input, expect, 345))

    def test_array46(self):
        input = """
Var
    i : Integer;
    myIntArray : Array[1 .. 20] of Integer;
    myBoolArray : Array[1 .. 20] of Boolean;

Procedure Main();
Begin
    For i := 1 to 5 do
    Begin
        myIntArray[i] := 1;
        myBoolArray[i] := True;
        myBoolArray[i+2] := 3;
    End
End
        """
        expect = 'Type Mismatch In Statement: AssignStmt(ArrayCell(Id(myBoolArray),BinaryOp(+,Id(i),IntLiteral(2))),IntLiteral(3))'
        self.assertTrue(TestChecker.test(input, expect, 346))

    def test_assign_string47(self):
        input = """
Var 
    S : String;

Procedure main();
Begin
    S := "Hey there! How are you?";
    putstring(S);
    return s;
End
        """
        expect = 'Type Mismatch In Statement: AssignStmt(Id(S),StringLiteral(Hey there! How are you?))'
        self.assertTrue(TestChecker.test(input, expect, 347))
    
    def test_array48(self):
        input = """
Var
	myVar : Integer;
	myArray : Array[1 .. 5] of Integer;

Procedure Main();
Begin
	myArray[2] := 25;
	myVar := myArray[2];
    myVar := myArray;
End"""
        expect = 'Type Mismatch In Statement: AssignStmt(Id(myVar),Id(myArray))'
        self.assertTrue(TestChecker.test(input, expect, 348))
    
    def test_funcall49(self):
        input = """procedure main();
                    var
                    radius, area : real;
                    begin
                    radius := 3333;
                    putstring("The area is ");
                    area := PI * radius * radius;
                    
                    end
                """
        expect = 'Undeclared Identifier: PI'
        self.assertTrue(TestChecker.test(input, expect, 349))

    def test_return50(self):
        input = """
                function fibo(x: integer): integer;
                begin
                    if x<=2 then return 1;
                    else return fibo(x-2)+ fibo(x-1);
                end
                procedure main();
                var b:real;
                a:integer;
                begin
                   b:=fibo(a);
                   return b; 
                end
                """
        expect = 'Type Mismatch In Statement: Return(Some(Id(b)))'
        self.assertTrue(TestChecker.test(input, expect, 350))
    
    def test_undeclared_procedure51(self):
        input = """
var conbocuoi4:integer;

function conbocuoi3(conbocuoi1:string; conbocuoi2:integer):integer;
begin
    conbocuoi2 := 123;
    return conbocuoi4;
end

procedure conbocuoi6(conbocuoi5:integer; conbocuoi6:boolean);
begin
    return;
end

procedure main(); 
var conbocuoi3:integer;
    conbocuoi2:real;
begin
    conbocuoi2 := 10;
    conbocuoi2("hehe");
    return;
end
"""
        expect = "Undeclared Procedure: conbocuoi2"
        self.assertTrue(TestChecker.test(input,expect,351))

    def test_undeclared_procedure52(self):
        input = """
var conbocuoi4:integer;

function conbocuoi3(conbocuoi1:string; conbocuoi2:integer):integer;
begin
    conbocuoi2 := 123;
    return conbocuoi4;
end

procedure conbocuoi7(conbocuoi5:integer; conbocuoi6:boolean);
begin
    while conbocuoi6 do
    begin
        conbocuoi5 := conbocuoi5 + 10;
        conbocuoi7(123, True);
    end
    return;
end

procedure main(); 
var conbocuoi3:integer;
    conbocuoi2:real;
begin
    conbocuoi2 := 10;
    if conbocuoi2 = 10 then
    begin
        conbocuoi3 := 10;
    end
    else conbocuoi4();
    return;
end
"""
        expect = "Undeclared Procedure: conbocuoi4"
        self.assertTrue(TestChecker.test(input,expect,352))
    
    def test_if53(self):
        input = """
var conbocuoi4:integer;

function conbocuoi3(conbocuoi1:string; conbocuoi2:integer):integer;
begin
    conbocuoi2 := 123;
    return conbocuoi4;
end

procedure conbocuoi6(conbocuoi5:integer; conbocuoi6:boolean);
begin
    while conbocuoi6 do
    begin
        conbocuoi5 := conbocuoi5 + 10;
        continue;
    end
    return;
end

procedure main(); 
var conbocuoi3:integer;
    conbocuoi2:real;
begin
    if (1) then
    begin
        conbocuoi2 := 1;
        conbocuoi3 := 2;
    end
    return;
end
"""
        expect = "Type Mismatch In Statement: If(IntLiteral(1),[AssignStmt(Id(conbocuoi2),IntLiteral(1)),AssignStmt(Id(conbocuoi3),IntLiteral(2))],[])"
        self.assertTrue(TestChecker.test(input,expect,353))
    
    def test_if54(self):
        input = """
var conbocuoi4:integer;

function conbocuoi3(conbocuoi1:string; conbocuoi2:integer):integer;
begin
    conbocuoi2 := 123;
    return conbocuoi4;
end

procedure conbocuoi6(conbocuoi5:integer; conbocuoi6:boolean);
begin
    while conbocuoi6 do
    begin
        conbocuoi5 := conbocuoi5 + 10;
        continue;
    end
    return;
end

procedure main(); 
var conbocuoi3:integer;
    conbocuoi2:real;
begin
    if (1.5) then
    begin
        conbocuoi2 := 1;
        conbocuoi3 := 2;
    end
    return;
end
"""
        expect = "Type Mismatch In Statement: If(FloatLiteral(1.5),[AssignStmt(Id(conbocuoi2),IntLiteral(1)),AssignStmt(Id(conbocuoi3),IntLiteral(2))],[])"
        self.assertTrue(TestChecker.test(input,expect,354))
    
    def test_var55(self):
        """ Test Precedence """
        input = """
                var a,b: integer;
                procedure main();
                var
                    a: integer;
                begin
                    a := abc();
                end
                
                procedure abc();
                var
                    a: integer;
                begin
                    a := a+c;
                end
                var c : integer;
                """
        expect = "Undeclared Function: abc"
        self.assertTrue(TestChecker.test(input, expect, 355))
    
    def test_if56(self):
        """ Test If Statement """
        input = """
                procedure main();
                var a: real;
                b:real;
                c: integer;
                e,g,h: real;
                begin
                    if a = 1 then begin
                        if b > 3 then c := 5;
                        else d := 1;

                        if e < 4 then ok();
                    end else begin
                        if h > 5 then ok(); else lyo();
                        g := 5;
                    end 
                    return ;
                end
                
                procedure ok();
                begin 
                end 
                
                procedure lyo();
                begin
                end
                """
        expect = "Undeclared Identifier: d"
        self.assertTrue(TestChecker.test(input, expect, 356))
    
    def test_continue57(self):
        """ Test For Statment """
        input = """
                procedure main();
                var a: real;
                i,j:integer;
                begin
                    for i := 1 to 10 do begin
                        for j := i downto 1 do
                            if (i + j) mod 2 = 1 then break;
                    continue;
                    end
                    continue;
                end
                """
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input, expect, 357))
    
    def test_multi58(self):
        input = """
                var a: real;

                procedure main();
                var a: real;
                b:real;
                i,j:integer;
                begin
                    for i := 1 to 10 do begin
                        for j := i downto 1 do
                            if (i + j) mod 2 = 1 then break;
                    continue;
                    end
                end

                procedure b();
                var a: real;
                begin 
                    with wi,wi:integer; do 
                    begin
                    end
                end
                """
        expect = "Redeclared Variable: wi"
        self.assertTrue(TestChecker.test(input, expect, 358))
    
    def test_for59(self):
        input = """
                var a: real;
                procedure main();
                var i,j:integer;
                begin
                    for a := 1 to 10 do begin
                        for j := i downto 1 do
                            if (i + j) mod 1 = 1 then break;
                    end
                end
            """
        expect = "Type Mismatch In Statement: For(Id(a)IntLiteral(1),IntLiteral(10),True,[For(Id(j)Id(i),IntLiteral(1),False,[If(BinaryOp(=,BinaryOp(mod,BinaryOp(+,Id(i),Id(j)),IntLiteral(1)),IntLiteral(1)),[Break],[])])])"
        self.assertTrue(TestChecker.test(input, expect, 359))
    
    def test_if60(self):
        input = """
                var a: real;
                procedure main();
                var i,j:integer;
                begin
                    if i then j := i;
                end
            """
        expect = "Type Mismatch In Statement: If(Id(i),[AssignStmt(Id(j),Id(i))],[])"
        self.assertTrue(TestChecker.test(input, expect, 360))
    
    def test_for61(self):
        input = """
                var a: real;
                procedure main();
                var i,j:integer;
                begin
                    for i := 1 to a do begin
                        for j := i downto 1 do
                            if (i + j) mod 1 = 1 then break;
                    end
                end
            """
        expect = "Type Mismatch In Statement: For(Id(i)IntLiteral(1),Id(a),True,[For(Id(j)Id(i),IntLiteral(1),False,[If(BinaryOp(=,BinaryOp(mod,BinaryOp(+,Id(i),Id(j)),IntLiteral(1)),IntLiteral(1)),[Break],[])])])"
        self.assertTrue(TestChecker.test(input, expect, 361))
    
    def test_proc62(self):
        input = """
        var d: integer;
        f: string;
        procedure Hn(n,a,b: integer);
            begin
            if n = 0 then exit();
            Hn(n-1,a,6-a-b);
            inc(d);
            writeln(f,d,". ",a," -> ",b);
            Hn(n-1,6-a-b,b);
            end
        procedure runHn(n: integer);
            begin
            d :=  0;
            assign(f,"hanoi.out");
            rewrite(f);
            writeln("-----------------");
            Hn(n,1,2);
            writeln(f,"Total: ",d," step(s)");
            close(f);
            readln();
            end
        procedure main();
        BEGIN
        runHn(3);
        END
        """
        expect = "Undeclared Procedure: exit"
        self.assertTrue(TestChecker.test(input, expect, 362))
    
    def test_if63(self):
        input = """
var conbocuoi4:integer;
    conbocuoi5:boolean;

function conbocuoi3(conbocuoi1:string; conbocuoi2:integer):integer;
begin
    conbocuoi2 := 123;
    return conbocuoi4;
end

procedure conbocuoi6(conbocuoi5:integer; conbocuoi6:boolean);
begin
    while conbocuoi6 do
    begin
        conbocuoi5 := conbocuoi5 + 10;
        continue;
    end
    return;
end

procedure main(); 
var conbocuoi3:integer;
    conbocuoi2:real;
begin
    if (True and True or not conbocuoi5 and then False) then
    begin
        conbocuoi2 := 1;
        conbocuoi3 := 2;
    end
    
    if (5 + 5) then
    begin
        conbocuoi2 := conbocuoi3;
    end
    return;
end
"""
        expect = "Type Mismatch In Statement: If(BinaryOp(+,IntLiteral(5),IntLiteral(5)),[AssignStmt(Id(conbocuoi2),Id(conbocuoi3))],[])"
        self.assertTrue(TestChecker.test(input,expect,363))
    
    def test_if64(self):
        input = """
var conbocuoi4:integer;
    conbocuoi5:boolean;

function conbocuoi3(conbocuoi1:string; conbocuoi2:integer):integer;
var conbocuoi4:boolean;
    conbocuoi5:integer;
begin
    if conbocuoi4 then
        conbocuoi2 := 1;
    if not conbocuoi4 then
        return conbocuoi2;
    if conbocuoi4 or not conbocuoi4 and conbocuoi4 or conbocuoi4 then
        return conbocuoi5;
    conbocuoi2 := 123;
    return conbocuoi2;
end

procedure conbocuoi6(conbocuoi5:integer; conbocuoi6:boolean);
begin
    while conbocuoi6 do
    begin
        conbocuoi5 := conbocuoi5 + 10;
        if conbocuoi6 or else not conbocuoi6 then
            return;
        continue;
    end
    return;
end

procedure main(); 
var conbocuoi3:integer;
    conbocuoi2:real;
begin
    
    if (5 + 5) then
    begin
        conbocuoi2 := conbocuoi3;
    end
    return;
end
"""
        expect = "Type Mismatch In Statement: If(BinaryOp(+,IntLiteral(5),IntLiteral(5)),[AssignStmt(Id(conbocuoi2),Id(conbocuoi3))],[])"
        self.assertTrue(TestChecker.test(input,expect,364))
    
    def test_for65(self):
        input = """
var conbocuoi4:integer;
    conbocuoi5:boolean;

function conbocuoi3(conbocuoi1:string; conbocuoi2:integer):integer;
var conbocuoi4:boolean;
    conbocuoi5, conbocuoi:integer;
begin
    for conbocuoi := conbocuoi5 downto conbocuoi5 - 100 do
    begin
        conbocuoi6(conbocuoi5, True);
        break;
    end
    conbocuoi2 := 123;
    
    return conbocuoi2;
end

procedure conbocuoi6(conbocuoi5:integer; conbocuoi6:boolean);
var conbocuoi, conbocuoi7:integer;
begin
    while conbocuoi6 do
    begin
        conbocuoi5 := conbocuoi5 + 10;
        if conbocuoi6 or else not conbocuoi6 then
            return;
        continue;
    end
    for conbocuoi := 1 to conbocuoi5 do
        for conbocuoi7 := conbocuoi + 1 to conbocuoi5 + 100 do
            continue;
    return;
end

procedure main(); 
var conbocuoi3:integer;
    conbocuoi2:real;
begin
    for conbocuoi3 := "conbocuoi1" to conbocuoi2 do
    begin
        conbocuoi2 := conbocuoi2 + 1.0;
    end
    return;
end
"""
        expect = "Type Mismatch In Statement: For(Id(conbocuoi3)StringLiteral(conbocuoi1),Id(conbocuoi2),True,[AssignStmt(Id(conbocuoi2),BinaryOp(+,Id(conbocuoi2),FloatLiteral(1.0)))])"
        self.assertTrue(TestChecker.test(input,expect,365))
    
    def test_for66(self):
        input = """
var conbocuoi4:integer;
    conbocuoi5:boolean;

function conbocuoi3(conbocuoi1:string; conbocuoi2:integer):integer;
var conbocuoi4:boolean;
    conbocuoi5, conbocuoi:integer;
begin
    for conbocuoi := conbocuoi5 downto conbocuoi5 - 100 do
    begin
        conbocuoi6(conbocuoi5, True);
        break;
    end
    conbocuoi2 := 123;
    
    return conbocuoi2;
end

procedure conbocuoi6(conbocuoi5:integer; conbocuoi6:boolean);
var conbocuoi, conbocuoi7:integer;
begin
    while conbocuoi6 do
    begin
        conbocuoi5 := conbocuoi5 + 10;
        if conbocuoi6 or else not conbocuoi6 then
            return;
        continue;
    end
    for conbocuoi := 1 to conbocuoi5 do
        for conbocuoi7 := conbocuoi + 1 to conbocuoi5 + 100 do
            continue;
    return;
end

procedure main(); 
var conbocuoi3:integer;
    conbocuoi2:real;
begin

    for conbocuoi3 := 10 downto -10 do
        for conbocuoi3 := 1 to 1000 do
            for conbocuoi2 := 1 to 10 do
                break;
    return;
end
"""
        expect = "Type Mismatch In Statement: For(Id(conbocuoi2)IntLiteral(1),IntLiteral(10),True,[Break])"
        self.assertTrue(TestChecker.test(input,expect,366))

    def test_for67(self):
        input = """
var conbocuoi4:integer;
    conbocuoi5:boolean;

function conbocuoi3(conbocuoi1:string; conbocuoi2:integer):integer;
var conbocuoi4:boolean;
    conbocuoi5, conbocuoi:integer;
begin
    for conbocuoi := conbocuoi5 downto conbocuoi5 - 100 do
    begin
        conbocuoi6(conbocuoi5, True);
        break;
    end
    conbocuoi2 := 123;
    
    return conbocuoi2;
end

procedure conbocuoi6(conbocuoi5:integer; conbocuoi6:boolean);
var conbocuoi, conbocuoi7:integer;
begin
    while conbocuoi6 do
    begin
        conbocuoi5 := conbocuoi5 + 10;
        if conbocuoi6 or else not conbocuoi6 then
            return;
        continue;
    end
    for conbocuoi := 1 to conbocuoi5 do
        for conbocuoi7 := conbocuoi + 1 to conbocuoi5 + 100 do
            continue;
    for conbocuoi5 := 1 to conbocuoi6 do
        break;
    return;
end

procedure main(); 
var conbocuoi3:integer;
    conbocuoi2:real;
begin
    for conbocuoi3 := "conbocuoi1" to conbocuoi2 do
    begin
        conbocuoi2 := conbocuoi2 + 1.0;
    end
    return;
end
"""
        expect = "Type Mismatch In Statement: For(Id(conbocuoi5)IntLiteral(1),Id(conbocuoi6),True,[Break])"
        self.assertTrue(TestChecker.test(input,expect,367))
    
    def test_param68(self):
        input = """
var conbocuoi4:integer;

function conbocuoi3(conbocuoi1:string; conbocuoi2:integer):integer;
begin
    return conbocuoi4;
end

procedure conbocuoi6(conbocuoi5:integer; conbocuoi5:boolean);
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
        expect = "Redeclared Parameter: conbocuoi5"
        self.assertTrue(TestChecker.test(input,expect,368))
    
    def test_return69(self):
        input = """
                var a: real;
                procedure main();
                var i,j:integer;
                k:boolean;
                begin
                    return 3;
                end
            """
        expect = "Type Mismatch In Statement: Return(Some(IntLiteral(3)))"
        self.assertTrue(TestChecker.test(input, expect, 369))

    def test_return70(self):
        input = """
                var a: real;
                procedure main();
                var i,j:integer;
                k:boolean;
                begin
                end
                function foo():real;
                var a:boolean;
                begin
                return a;
                end
            """
        expect = "Type Mismatch In Statement: Return(Some(Id(a)))"
        self.assertTrue(TestChecker.test(input, expect, 370))

    def test_return71(self):
        input = """
                var a: real;
                procedure main();
                var i,j:integer;
                k:boolean;
                begin
                a:= foo();
                end
                function foo():real;
                var a:boolean;
                begin
                if a then return 1;
                else return a;
                end
            """
        expect = "Type Mismatch In Statement: Return(Some(Id(a)))"
        self.assertTrue(TestChecker.test(input, expect, 371))
    
    def test_return72(self):
        input = """
                var a: real;
                procedure main();
                var i,j:integer;
                k:boolean;
                begin
                a:= foo();
                end
                function foo():integer;
                var a:boolean;
                begin
                
                if a then 
                    begin
                        if a then  
                        begin
                            return 3;
                        end
                        return 3.5;
                    end
                else return 4;
                end
            """
        expect = "Type Mismatch In Statement: Return(Some(FloatLiteral(3.5)))"
        self.assertTrue(TestChecker.test(input, expect, 372))
    
    def test_return73(self):
        input = """
                var a: real;
                procedure main();
                var i,j:integer;
                k:boolean;
                begin
                end
                function foo():array [1 .. 5] of integer;
                var a:array[1 .. 6] of integer;
                begin
                return a ;
                end
            """
        expect = "Type Mismatch In Statement: Return(Some(Id(a)))"
        self.assertTrue(TestChecker.test(input, expect, 373))
    
    def test_funcall74(self):
        input = """
                var a: real;
                procedure main();
                var i,j:real;
                k:boolean;
                a:string;
                b:array[1 .. 5] of integer;
                d:string;
                begin
                foo(a,b,b);
                end
                procedure FOO(a:string;b,c:array[1 .. 5] of real);
                var a:array[1 .. 5] of integer;
                begin
                end
            """
        expect = "Type Mismatch In Statement: CallStmt(Id(foo),[Id(a),Id(b),Id(b)])"
        self.assertTrue(TestChecker.test(input, expect, 374))
    
    def test_arraycell75(self):
        input = """
                var a: real;
                procedure main();
                var i,j:real;
                k:boolean;
                a:string;
                b:array[1 .. 5] of integer;
                d:integer;
                begin
                i := j := b[2*i];
                end
                
            """
        expect = "Type Mismatch In Expression: ArrayCell(Id(b),BinaryOp(*,IntLiteral(2),Id(i)))"
        self.assertTrue(TestChecker.test(input, expect, 375))
    
    def test_arraycell76(self):
        input = """
                var a: real;
                procedure main();
                var i,j:real;
                k:boolean;
                a:string;
                b:array[1 .. 5] of integer;
                d:integer;
                begin
                i := j := b[2*d/4];
                end
                
            """
        expect = "Type Mismatch In Expression: ArrayCell(Id(b),BinaryOp(/,BinaryOp(*,IntLiteral(2),Id(d)),IntLiteral(4)))"
        self.assertTrue(TestChecker.test(input, expect, 376))
    
    def test_array77(self):
        input = """
                var a: real;
                procedure main();
                var i,j:real;
                k:boolean;
                a:string;
                b:array[1 .. 5] of integer;
                d:string;
                begin
                i := foo(b[3],b,b);
                i := foo(b[3],b,b)*3+4-5 div 6;

                end
                function foo(a:integer;b,c:array[1 .. 5] of integer):integer;
                var a:array[1 .. 5] of integer;
                begin
                return a[3];
                end
            """
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input, expect, 377))
    
    def test_var78(self):
        input = """
                var a: real;
                procedure main();
                var i,j:real;
                k:boolean;
                a:string;
                b:array[1 .. 5] of integer;
                d:string;
                begin
                i := foo(b[6],b,b);
                i := foo(b[3],b,b)*3+4-5 div 6;

                end
                function foo(a:real;b,c:array[1 .. 5] of integer):integer;
                var b:array[1 .. 5] of integer;
                begin
                return a[3];
                end
            """
        expect = "Redeclared Variable: b"
        self.assertTrue(TestChecker.test(input, expect, 378))
    
    def test_noentry79(self):
        input = """
                var a: real;

                function main():integer;
                var j:real;
                i:integer;
                k:boolean;
                a:string;
                b:array[1 .. 5] of integer;
                d:string;
                begin
                for i := 4 to 5 do
                begin
                    for i:= 3 to 4 do
                    begin 
                        if i < 3 then continue;
                        else
                        begin
                            for i := 4 to 5 do break;
                        end
                    end
                    if i < 3 then break;
                end
                while true do
                begin 
                    while false do break;
                    if i > 5 then continue;
                    else while false do continue;
                end
                end
            """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input, expect, 379))
    
    def test_noentry80(self):
        input = """
                var a: real;

                function bar():integer;
                var j:real;
                i:integer;
                k:boolean;
                a:string;
                b:array[1 .. 5] of integer;
                d:string;
                begin
                for i := 4 to 5 do
                begin
                    for i:= 3 to 4 do
                    begin 
                        if i < 3 then continue;
                        else
                        begin
                            for i := 4 to 5 do break;
                        end
                    end
                    if i < 3 then break;
                end
                while true do
                begin 
                    while false do break;
                    if i > 5 then continue;
                    else while false do continue;
                end
                end
            """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input, expect, 380))
    
    def test_return81(self):
        input = """
                var a: real;

                procedure main();
                var j:real;
                i:integer;
                k:boolean;
                a:string;
                b:array[1 .. 5] of integer;
                d:string;
                begin
                i := foo(4);
                if false then i:=1;
                while false do i:=1;
                while true do i:= 1;
                i:=1;
                end
                function foo(a:integer):integer;
                begin 
                if false then return 4;
                end
            """
        expect = "Function foo Not Return "
        self.assertTrue(TestChecker.test(input, expect, 381))

    def test_return82(self):
        input = """
                var a: real;

                procedure main();
                var j:real;
                i:integer;
                k:boolean;
                a:string;
                b:array[1 .. 5] of integer;
                d:string;
                begin
                if false then i:=1;
                while false do if true then return; else bar(3);
                while true do 
                begin 
                    for I:= 4 to i+1 do
                    begin
                        with a:integer; do
                            a:= Foo1(a);
                    end
                end
                wITH A:integer; do
                    a:= foo(a);
                end

                procedure bar(a:integer);
                begin 
                if False then return ;
                end

                function foO(a:integer):integer;
                begin 
                if false then return 4;
                end

                function foo(a:integer):integer;
                begin 
                if false then return 4;
                end

                
            """
        expect = "Redeclared Function: foo"
        self.assertTrue(TestChecker.test(input, expect, 382))
    
    def test_global83(self):
        input = """
                var a: string;
                var k:string;
                var b:real;
                procedure main();
                var i,j:real;
                K:boolean;
                A:string;
                B:array[1 .. 5] of integer;
                d:integer;
                begin
                i := j := b[1];
                end
                procedure foo(a:integer);
                var A:string;
                begin
                end
            """
        expect = "Redeclared Variable: A"
        self.assertTrue(TestChecker.test(input, expect, 383))
    
    def test_return84(self):
        input = """
function conbocuoi1(conbocuoi:integer):integer;
begin
    return 1;
end

function conbocuoi2(conbocuoi:real):real;
begin
    if True then return 1.0;
    
end

function conbocuoi3(conbocuoi:string):string;
begin
    return "conbocuoi";
end

function conbocuoi4(conbocuoi:array[1 .. 100] of integer):array[1 .. 100] of integer;
begin
    return conbocuoi;
end

function conbocuoi5(conbocuoi:boolean):boolean;
begin
    return True;
end

procedure main(); 
var c1:integer;
    c2:real;
    c5:boolean;
    c3:string;
    c4:array[1 .. 100] of integer;
begin
    c1 := conbocuoi1(c1);
    c2 := conbocuoi2(c2);
    c5 := conbocuoi5(c5);
    c1 := conbocuoi4(c4)[10];
    return;
end
"""
        expect = "Function conbocuoi2 Not Return "
        self.assertTrue(TestChecker.test(input,expect,384))
    
    def test_return85(self):
        input = """
                var a: string;
                var k:string;
                var b:real;
                procedure main();
                var i,j:real;
                K:boolean;
                A:string;
                B:array[1 .. 5] of integer;
                d:integer;
                begin
                    i := j := b[1];
                end
                function foo(a:integer):integer;
                var B:string;
                begin
                    if true then
                    begin
                        if false then return 0.5;
                        else return 3;
                    end
                    else return 1;
                end
                
            """
        expect = "Type Mismatch In Statement: Return(Some(FloatLiteral(0.5)))"
        self.assertTrue(TestChecker.test(input, expect, 385))
    
    def test_return86(self):
        input = """
                var a: string;
                var k:string;
                var b:real;
                procedure main();
                var i,j:real;
                K:boolean;
                A:string;
                B:array[1 .. 5] of integer;
                d:integer;
                begin
                i := j := b[1] := foo(b[2]);
                end
                function foo(a:integer):integer;
                var B:string;
                begin
                    if true then
                    begin
                        if false then 
                            return 1 ;
                        for a:= 1 to 10 do
                            begin 
                                if false then return 5;
                                if true then return 6;
                            end
                    end
                    else return 1;
                end
                
            """
        expect = "Function foo Not Return "
        self.assertTrue(TestChecker.test(input, expect, 386))
    
    def test_return87(self):
        input = """
                var a: real;

                procedure main();
                var i,j:real;
                k:boolean;
                a:string;
                b:array[1 .. 5] of integer;
                d:string;
                begin
                i := foo(b[10]);
                end

                function foo(b:integer):integer;
                var a:array[1 .. 5] of integer;
                begin
                    if b>3 then 
                    begin
                        with a,b:integer;do 
                        begin
                            if b < 4 then return foo(3);
                            else 
                            begin
                                if b > 5 then return 3;
                            end
                        end
                    end
                    else return 1;
                end
            """
        expect = "Function foo Not Return "
        self.assertTrue(TestChecker.test(input, expect, 387))
    
    def test_return88(self):
        input = """
                var a: real;

                procedure main();
                var i,j:real;
                k:boolean;
                a:string;
                b:array[1 .. 5] of integer;
                d:string;
                begin
                foo(b[10]);
                end

                procedure foo(b:integer);
                var a:array[1 .. 5] of integer;
                begin
                    
                end
                procedure foo(b:integer);
                var a:array[1 .. 5] of integer;
                begin
                    
                end
            """
        expect = "Redeclared Procedure: foo"
        self.assertTrue(TestChecker.test(input, expect, 388))
    
    def test_while89(self):
        input = """
var conbocuoi4:integer;
    conbocuoi5:boolean;

function conbocuoi3(conbocuoi1:string; conbocuoi2:integer):integer;
var conbocuoi4:boolean;
    conbocuoi5, conbocuoi:integer;
begin
    
    return conbocuoi2;
end

procedure conbocuoi6(conbocuoi5:integer; conbocuoi6:boolean);
var conbocuoi, conbocuoi7:integer;
    conbocuoi3:boolean;
begin

    return;
end

procedure main(); 
var conbocuoi3:integer;
    conbocuoi2:real;
    conbocuoi1:boolean;
begin
    while (conbocuoi1) do
        break;
        
    while conbocuoi2 + conbocuoi3 do
        conbocuoi1 := False;
        
    return;
end
"""
        expect = "Type Mismatch In Statement: While(BinaryOp(+,Id(conbocuoi2),Id(conbocuoi3)),[AssignStmt(Id(conbocuoi1),BooleanLiteral(False))])"
        self.assertTrue(TestChecker.test(input,expect,389))
    
    def test_while90(self):
        input = """
var conbocuoi4:integer;
    conbocuoi5:boolean;

function conbocuoi3(conbocuoi1:string; conbocuoi2:integer):integer;
var conbocuoi4:boolean;
    conbocuoi5, conbocuoi:integer;
begin
    while (conbocuoi4 and True) do
        break;
    while (conbocuoi4 and not conbocuoi4 or conbocuoi4) do
        continue;
    return conbocuoi2;
end

procedure conbocuoi6(conbocuoi5:integer; conbocuoi6:boolean);
var conbocuoi, conbocuoi7:integer;
    conbocuoi3:boolean;
begin
    
    return;
end

procedure main(); 
var conbocuoi3:integer;
    conbocuoi2:real;
    conbocuoi1:boolean;
begin
    while (conbocuoi1) do
        break;
        
    while conbocuoi2 + conbocuoi3 do
        conbocuoi1 := False;
        
    return;
end
"""
        expect = "Type Mismatch In Statement: While(BinaryOp(+,Id(conbocuoi2),Id(conbocuoi3)),[AssignStmt(Id(conbocuoi1),BooleanLiteral(False))])"
        self.assertTrue(TestChecker.test(input,expect,390))
    
    def test_whil91(self):
        input = """
var conbocuoi4:integer;
    conbocuoi5:boolean;

function conbocuoi3(conbocuoi1:string; conbocuoi2:integer):integer;
var conbocuoi4:boolean;
    conbocuoi5, conbocuoi:integer;
begin
    while (conbocuoi4 and True) do
        break;
    while (conbocuoi4 and not conbocuoi4 or conbocuoi4) do
        continue;
    return conbocuoi2;
end

procedure conbocuoi6(conbocuoi5:integer; conbocuoi6:boolean);
var conbocuoi, conbocuoi7:integer;
    conbocuoi3:boolean;
begin
    while (conbocuoi3) do
        break;
    while (True) do
        break;
    while (False) do
        break;
    return;
end

procedure main(); 
var conbocuoi3:integer;
    conbocuoi2:real;
    conbocuoi1:boolean;
begin
    while (conbocuoi1) do
        break;
        
    while conbocuoi2 + conbocuoi3 do
        conbocuoi1 := False;
        
    return;
end
"""
        expect = "Type Mismatch In Statement: While(BinaryOp(+,Id(conbocuoi2),Id(conbocuoi3)),[AssignStmt(Id(conbocuoi1),BooleanLiteral(False))])"
        self.assertTrue(TestChecker.test(input,expect,391))
    
    def test_assign92(self):
        input = """
var conbocuoi4:integer;
    conbocuoi5:boolean;

function conbocuoi3(conbocuoi1:string; conbocuoi2:integer):integer;
var conbocuoi4:boolean;
    conbocuoi5, conbocuoi:integer;
begin

    return conbocuoi2;
end

procedure conbocuoi6(conbocuoi5:integer; conbocuoi6:boolean);
var conbocuoi, conbocuoi7:integer;
    conbocuoi3:boolean;
begin
    
    return;
end

procedure main(); 
var conbocuoi3:integer;
    conbocuoi2:real;
    conbocuoi1:boolean;
begin
    conbocuoi2 := conbocuoi3;
    conbocuoi3 := conbocuoi2;
    return;
end
"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(conbocuoi3),Id(conbocuoi2))"
        self.assertTrue(TestChecker.test(input,expect,392))
    
    def test_call93(self):
        input = """
var conbocuoi4:integer;
    conbocuoi5:boolean;

procedure conbocuoi6(conbocuoi5:integer; conbocuoi6:real; conbocuoi8:boolean);
var conbocuoi, conbocuoi7:integer;
    conbocuoi3:boolean;
begin

    return;
end

procedure main(); 
var conbocuoi:integer;
    conbocuoi2:real;
    conbocuoi1:boolean;
begin
    conbocuoi6(conbocuoi, conbocuoi2, conbocuoi1);
    conbocuoi6(conbocuoi, conbocuoi, conbocuoi1);
    conbocuoi6(conbocuoi1, conbocuoi2, conbocuoi2);
    return;
end
"""
        expect = "Type Mismatch In Statement: CallStmt(Id(conbocuoi6),[Id(conbocuoi1),Id(conbocuoi2),Id(conbocuoi2)])"
        self.assertTrue(TestChecker.test(input,expect,393))
    
    def test_array94(self):
        input = """
procedure main(); 
var conbocuoi1:array [1 .. 100] of integer;
    conbocuoi2:array [1 .. 100] of real;
    conbocuoi3:array [1 .. 100] of boolean;
    conbocuoi4:array [1 .. 100] of string;
    c1:integer;
    c2:real;
    c3:boolean;
    c4:string;
begin
    c1 := conbocuoi1[1];
    c2 := conbocuoi1[2];
    c3 := conbocuoi1[3];
    return;
end
"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(c3),ArrayCell(Id(conbocuoi1),IntLiteral(3)))"
        self.assertTrue(TestChecker.test(input,expect,394))
    
    def test_array95(self):
        input = """
procedure main(); 
var conbocuoi1:array [1 .. 100] of integer;
    conbocuoi2:array [1 .. 100] of real;
    conbocuoi3:array [1 .. 100] of boolean;
    c1:integer;
    c2:real;
    c3:boolean;
    c4:string;
begin
    c1 := conbocuoi1[1 + 1];
    c2 := conbocuoi2[2 + 2];
    c3 := conbocuoi3[3 + 3];
    c3 := conbocuoi3["1"];
    return;
end
"""
        expect = "Type Mismatch In Expression: ArrayCell(Id(conbocuoi3),StringLiteral(1))"
        self.assertTrue(TestChecker.test(input,expect,395))
    
    def test_array96(self):
        input = """
procedure main(); 
var conbocuoi1:array [1 .. 100] of integer;
    conbocuoi2:array [1 .. 100] of real;
    conbocuoi3:array [1 .. 100] of boolean;
    c1:integer;
    c2:real;
    c3:boolean;
    c4:string;
begin
    c1 := conbocuoi1[1];
    c2 := conbocuoi2[2];
    c3 := conbocuoi3[3/3];
    return;
end
"""
        expect = "Type Mismatch In Expression: ArrayCell(Id(conbocuoi3),BinaryOp(/,IntLiteral(3),IntLiteral(3)))"
        self.assertTrue(TestChecker.test(input,expect,396))
    
    def test_array97(self):
        input = """
procedure main(); 
var conbocuoi1:array [1 .. 100] of integer;
    conbocuoi2:array [1 .. 100] of real;
    conbocuoi3:array [1 .. 100] of boolean;
    c1:integer;
    c2:real;
    c3:boolean;
    c4:string;
begin
    c1 := conbocuoi1[1];
    c2 := conbocuoi2[2];
    c3 := c1[3];
    return;
end
"""
        expect = "Type Mismatch In Expression: ArrayCell(Id(c1),IntLiteral(3))"
        self.assertTrue(TestChecker.test(input,expect,397))
    
    def test_return98(self):
        input = """
function conbocuoi1(conbocuoi:integer):integer;
begin
    
end

function conbocuoi2(conbocuoi:real):real;
begin
    return 1.0;
end

function conbocuoi3(conbocuoi:string):string;
begin
    return "conbocuoi";
end

function conbocuoi4(conbocuoi:array[1 .. 100] of integer):array[1 .. 100] of integer;
begin
    return conbocuoi;
end

function conbocuoi5(conbocuoi:boolean):boolean;
begin
    return True;
end

procedure main(); 
var c1:integer;
    c2:real;
    c5:boolean;
    c3:string;
    c4:array[1 .. 100] of integer;
begin
    c1 := conbocuoi1(c1);
    c2 := conbocuoi2(c2);
    c5 := conbocuoi5(c5);
    c1 := conbocuoi4(c4)[10];
    return;
end
"""
        expect = "Function conbocuoi1 Not Return "
        self.assertTrue(TestChecker.test(input,expect,398))
    
    def test_UnOp99(self):
        input = """
procedure main(); 
var c1:integer;
    c2:real;
    c3:boolean;
    c4:string;
begin
    c1 := -c1;
    c2 := -c2;
    c3 := not c3;
    c1 := not - not False;
    return;
end
"""
        expect = "Type Mismatch In Expression: UnaryOp(-,UnaryOp(not,BooleanLiteral(False)))"
        self.assertTrue(TestChecker.test(input,expect,399))