from parser import expr

class AstPrinter(expr.Visitor):
    def visit_binary_expr(self, expr: expr.Binary):
        return self.eval(expr.op.lexeme, expr.left, expr.right)

    def visit_unary_expr(self, expr: expr.Unary):
        return self.eval(expr.op.lexeme, expr.right)

    def visit_literal_expr(self, expr: expr.Literal):
        return str(expr.value)

    def visit_grouping_expr(self, expr: expr.Grouping):
        return self.eval("grouped", expr.expr)
    
    def eval(self, label, *exprs: expr.Expr):
        out = "("
        out += str(label)
        
        for expr in exprs:
            out += f" {expr.accept(self)}"
        
        out += ")"
        return out
    
    def print(self, expr: expr.Expr):
        print(expr.accept(self))
