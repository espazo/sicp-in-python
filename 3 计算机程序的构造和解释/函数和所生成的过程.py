# 递归函数
def pig_latin(w):
    """Return the Pig Latin equivalent of English word w."""
    if starts_with_a_vowel(w):
        return w + 'ay'
    return pig_latin(w[1:] + w[0])


def starts_with_a_vowel(w):
    """Return whether w begins with a vowel."""
    return w[0].lower() in 'aeiou'


print(pig_latin('pun'))


def fact_iter(n):
    total, k = 1, 1
    while k <= n:
        total, k = total * k, k + 1
    return total


print(fact_iter(4))


def fact(n):
    if n == 1:
        return 1
    return n * fact(n - 1)


print(fact(4))


# 树形递归
def fib(n):
    if n == 1:
        return 0
    if n == 2:
        return 1
    return fib(n - 2) + fib(n - 1)


print(fib(6))


def fib_iter(n):
    prev, curr = 1, 0  # curr is the first Fibonacci number.
    for _ in range(n - 1):
        prev, curr = curr, prev + curr
    return curr


# 记忆函数
def memo(f):
    """Return a memoized version of single-argument function f."""
    cache = {}

    def memoized(n):
        if n not in cache:
            cache[n] = f(n)
        return cache[n]

    return memoized


fib = memo(fib)
print(fib(40))


# 找零
def count_change(a, kinds=(50, 25, 10, 5, 1)):
    """Return the number of way to change amount a using coin kinds."""
    if a == 0:
        return 1
    if a < 0 or len(kinds) == 0:
        return 0
    d = kinds[0]
    return count_change(a, kinds[1:]) + count_change(a - d, kinds)


print(count_change(100))


# 求幂
def exp(b, n):
    if n == 0:
        return 1
    return b * exp(b, n - 1)


# 使用固定的空间
def exp_iter(b, n):
    result = 1
    for _ in range(n):
        result = result * b
    return result


# 下面两个函数 log 的时间求幂
def square(x):
    return x * x


def fast_exp(b, n):
    if n == 0:
        return 1
    if n % 2 == 0:
        return square(fast_exp(b, n // 2))
    else:
        return b * fast_exp(b, n - 1)


print(fast_exp(2, 100))