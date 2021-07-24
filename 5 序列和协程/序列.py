#
# 隐式序列
#

"""计算机科学将惰性作为一种重要的计算工具加以赞扬"""
r = range(10000, 1000000000)
print(r[45006230])


# Python 迭代器

class Letters(object):
    def __init__(self):
        self.current = 'a'

    def __next__(self):
        if self.current > 'd':
            raise StopIteration
        result = self.current
        self.current = chr(ord(result) + 1)
        return result

    def __iter__(self):
        return self


letters = Letters()
letters.__next__()
letters.__next__()
letters.__next__()
letters.__next__()
# letters.__next__()  # 报错


class Positives(object):
    def __init__(self):
        self.current = 0

    def __next__(self):
        result = self.current
        self.current += 1
        return result

    def __iter__(self):
        return self


# for 语句
counts = [1, 2, 3]
for item in counts:
    print(item)


i = counts.__iter__()
try:
    while True:
        item = i.__next__()
        print(item)
except StopIteration:
    pass


# 生成器和 yield 语句

def letters_generator():
    current = 'a'
    while current <= 'd':
        yield current
        current = chr(ord(current) + 1)


for letter in letters_generator():
    print(letter)

letters = letters_generator()

print(type(letters))
print(letters.__next__())
print(letters.__next__())
print(letters.__next__())
print(letters.__next__())
# print(letters.__next__())   # 抛出 StopIteration 异常


# 可迭代对象

def all_pairs(s):
    for item1 in s:
        for item2 in s:
            yield (item1, item2)


print(list(all_pairs([1, 2, 3])))


class LetterIterable(object):
    def __iter__(self):
        current = 'a'
        while current <= 'd':
            yield current
            current = chr(ord(current) + 1)


letters = LetterIterable()
print(all_pairs(letters).__next__())


# 流

class Stream(object):
    """A lazily computed recursive list."""

    def __init__(self, first, compute_rest, empty=False):
        self.first = first
        self._compute_rest = compute_rest
        self.empty = empty
        self._rest = None
        self._computed = False

    @property
    def rest(self):
        """Return the rest of the stream, computing it if necessary."""
        assert not self.empty, 'Empty streams have no rest.'
        if not self._computed:
            self._rest = self._compute_rest()
            self._computed = True
        return self._rest

    def __repr__(self):
        if self.empty:
            return '<empty stream>'
        return 'Stream({0}, <compute_rest>)'.format(repr(self.first))


Stream.empty = Stream(None, None, True)

s = Stream(1, lambda: Stream(2 + 3, lambda: Stream.empty))

print(s.first)
print(s.rest.first)
print(s.rest)


def map_stream(fn, s):
    if s.empty:
        return s

    def compute_rest():
        return map_stream(fn, s.rest)
    return Stream(fn(s.first), compute_rest)


def filter_stream(fn, s):
    if s.empty:
        return s

    def compute_rest():
        return filter_stream(fn, s.rest)

    if fn(s.first):
        return Stream(s.first, compute_rest)

    return compute_rest()


# 为了观察流的内容，我们需要将其截断为有限长度，并转换为 Python list
def truncate_stream(s, k):
    if s.empty or k == 0:
        return Stream.empty

    def compute_rest():
        return truncate_stream(s.rest, k - 1)

    return Stream(s.first, compute_rest)


def stream_to_list(s):
    r = []
    while not s.empty:
        r.append(s.first)
        s = s.rest
    return r


def primes(pos_stream):
    def not_divible(x):
        return x % pos_stream.first != 0

    def compute_rest():
        return primes(filter_stream(not_divible, pos_stream.rest))

    return Stream(pos_stream.first, compute_rest)


# p1 = primes(make_integer_stream(2))
# stream_to_list(truncate_stream(p1, 7))
