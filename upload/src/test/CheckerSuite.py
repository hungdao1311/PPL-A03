import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    def test_multi60(self):
        """ Test If Statement """
        input = """
                procedure main();
                var a: real;
                b:real;
                c: integer;
                d: real;
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
                
                function test():boolean;
                var a:integer;
                begin 
                    if a = 1 then return 3;
                    else return true;
                end

                procedure lyo();
                begin
                end
                """
        expect = "Type Mismatch In Statement: Return(Some(IntLiteral(3)))"
        self.assertTrue(TestChecker.test(input, expect, 414))