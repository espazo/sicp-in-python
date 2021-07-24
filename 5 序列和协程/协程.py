#
# Python 协程
#

# 生成器对象上有两个额外的方法：send() 和 close()
# 创建了一个模型使对象可以消耗或产出值
# 定义了这些对象的生成器函数叫做协程

# 协程可以通过（yield）语句来消耗值


def match(pattern):
    print('Looking for ' + pattern)
    try:
        while True:
            s = (yield)
            if pattern in s:
                print(s)
    except GeneratorExit:
        print("=== Done ===")


m = match("Jabberwock")
m.__next__()
m.send("the Jabberwock with eyes of flame")
m.send("came whiffling through the tulgey wood")
m.send("and burbled as it came")
m.close()


def read(file, next_coroutine):
    for line in file.split():
        next_coroutine.send(line)


text = 'Commending spending is offending to people pending lending!'
matcher = match('ending')
matcher.__next__()
read(text, matcher)

#
# 生产、过滤和消耗
#

# 生产者，创建序列中的物品，并使用 send()，而不是 (yield)
# 过滤器，使用 (yield) 来消耗物品并将结果使用 sned() 发送给下一个步骤
# 消费者，使用 (yield) 来消耗物品，但是从来不发送
print('生产、过滤和消费')


def match_filter(pattern, next_coroutine):
    print('Looking for ' + pattern)
    try:
        while True:
            s = (yield)
            if pattern in s:
                next_coroutine.send(s)
    except GeneratorExit:
        next_coroutine.close()


def print_consumer():
    print('Preparing to print')
    try:
        while True:
            line = (yield)
            print(line)
    except GeneratorExit:
        print("=== Done ===")


printer = print_consumer()
printer.__next__()

matcher = match_filter('pend', printer)
matcher.__next__()

read(text, matcher)


# 过滤器还可以用来转换元素
def count_letters(next_coroutine):
    try:
        while True:
            s = (yield)
            counts = {letter: s.count(letter) for letter in set(s)}
            next_coroutine.send(counts)
    except GeneratorExit as e:
        next_coroutine.close()


# 可以使用它来计算文本中最常出现的字母，并使用一个消费者，
# 将字典合并来找出最常出现的键。
def sum_dictionaries():
    total = {}
    try:
        while True:
            counts = (yield)
            for letter, count in counts.items():
                total[letter] = count + total.get(letter, 0)
    except GeneratorExit:
        max_letter = max(total.items(), key=lambda t: t[1])[0]
        print("Most frequent letter: " + max_letter)


s = sum_dictionaries()
s.__next__()
c = count_letters(s)
c.__next__()
read(text, c)


#
# 多任务
#

# 生产者或过滤器并不受限于唯一的下游。它可以拥有多个小城作为他的下游，
# 并使用 send() 向它们发送数据。
def read_to_many(text, coroutines):
    for word in text.split():
        for coroutine in coroutines:
            coroutine.send(word)
    for coroutine in coroutines:
        coroutine.close()


m = match("mend")
m.__next__()

p = match("pe")
p.__next__()

read_to_many(text, [m, p])
