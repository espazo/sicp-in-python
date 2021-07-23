#
# 1 计算器
#

# 表达式树

class Exp(object):
    """A call expression in Calculator."""
    def __init__(self, operator, operands):
        self.operator = operator
        self.operands = operands

    def __repr__(self):
        return 'Exp({0}, {1})'.format(repr(self.operator), repr(self.operator))

    def __str__(self):
        operand_strs = ', '.join(map(str, self.operands))
        return '{0}({1})'.format(self.operator, operand_strs)


print(repr(Exp('add', [1, 2])))
print(Exp('add', [1, 2]))

print(repr(Exp('add', [1, Exp('mul', [2, 3, 4])])))
print(Exp('add', [1, Exp('mul', [2, 3, 4])]))

# 求值

from operator import mul
from functools import reduce


def calc_apply(operator, args):
    """Apply the named operator to a list of args."""
    if operator in ('add', '+'):
        return sum(args)
    if operator in ('sub', '-'):
        if len(args) == 0:
            raise TypeError(operator + ' requires at least 1 argument')
        if len(args) == 1:
            return -args[0]
        return sum(args[:1] + [-arg for arg in args[1:]])
    if operator in ('mul', '*'):
        return reduce(mul, args, 1)
    if operator in ('div', '/'):
        if len(args) != 2:
            raise TypeError(operator + ' requires exactly 2 arguments')
        numer, denom = args
        return numer / denom


print(calc_apply('+', [1, 2, 3]))
print(calc_apply('-', [10, 1, 2, 3]))
print(calc_apply('*', []))
print(calc_apply('/', [40, 5]))

e = Exp('add', [2, Exp('mul', [4, 6])])
print(e)
# print(calc_eval(e))     # 26


# REPL：（读取、求值、打印）循环


# FIXME：需要实现函数 calc_eval
def old_read_eval_print_loop():
    """Run a read-eval-print loop for calculator."""
    while True:
        expression_tree = calc_parse(input('calc> '))
        print(calc_eval(expression_tree))


def read_eval_print_loop():
    """Run a read-eval-print loop for calculator."""
    while True:
        try:
            expression_tree = calc_parse(input('calc> '))
            print(calc_eval(expression_tree))
        except (SyntaxError, TypeError, ZeroDivisionError) as err:
            print(type(err).__name__ + ':', err)
        except (KeyboardInterrupt, EOFError):
            print('Calculation completed.')
            return


#
# 解析
#

def calc_parse(line):
    """Parse a line of calculator input and return an expression tree."""
    tokens = tokenize(line)
    expression_tree = analyze(tokens)
    if len(tokens) > 0:
        raise SyntaxError('Extra token(s): ' + ' '.join(tokens))
    return expression_tree


# 词法分析
def tokenize(line):
    """Convert a string into a list of tokens."""
    spaced = line.replace('(', ' ( ').replace(')', ' ) ').replace(',', ' , ')
    return spaced.split()


tokenize('add(2, mul(4, 6))')


# 语法分析

# def analyze(tokens):
#     """Create a tree of nested lists from a sequence of token."""
#     token = analyze_token(tokens.pop(0))
#     if type(token) in (int, float):
#         return token
#     else:
#         tokens.pop(0)   # Remove (
#         return Exp(token, analyze_operands(tokens))
#
#
# def analyze_operands(tokens):
#     """Read a list of comma-separated operands."""
#     operands = []
#     while tokens[0] != ')':
#         if operands:
#             tokens.pop(0)   # Remove ,
#         operands.append(analyze(tokens))
#     tokens.pop(0)   # Remove )
#     return operands


def analyze_token(token):
    """Return the value of token if it can be analyzed as a number, or token."""
    try:
        return int(token)
    except (TypeError, ValueError):
        try:
            return float(token)
        except (TypeError, ValueError):
            return token


def assert_non_empty(tokens):
    """Raise an excpetion if tokens is empty."""
    if len(tokens) == 0:
        raise SyntaxError('unexpected end of line')


known_operators = ['add', 'sub', 'mul', 'div', '+', '-', '*', '/']


def analyze(tokens):
    """Create a tree of nested lists from a sequence of tokens."""

    assert_non_empty(tokens)
    token = analyze_token(tokens.pop(0))
    if type(token) in (int, float):
        return token
    if token in known_operators:
        if len(tokens) == 0 or tokens.pop(0) != '(':
            raise SyntaxError('expected ( after ' + token)
        return Exp(token, analyze_operands(tokens))
    else:
        raise SyntaxError('unexpected ' + token)


def analyze_operands(tokens):
    """Analyze a sequence of comma-separated operands."""
    assert_non_empty(tokens)
    operands = []
    while tokens[0] != ')':
        if operands and tokens.pop(0) != ',':
            raise SyntaxError('expected ,')
        operands.append(analyze(tokens))
        assert_non_empty(tokens)
    tokens.pop(0)   # Remove )
    return operands



