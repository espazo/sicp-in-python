class Account(object):
    interest = 0.02  # A class attribute

    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder

    def deposit(self, amount):
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return 'Insufficient funds'
        self.balance = self.balance - amount
        return self.balance


a = Account('Jim')
print(a.balance)
print(a.holder)

b = Account('Jack')
b.balance = 200
print([acc.balance for acc in (a, b)])

print(a is a)
print(a is b)

c = a
print(c is a)

tom_account = Account('Tom')
print(tom_account.deposit(100))
print(tom_account.withdraw(90))
print(tom_account.withdraw(90))
print(tom_account.holder)

print(type(Account.deposit))
print(type(tom_account.deposit))

print(Account.deposit(tom_account, 1001))
print(tom_account.deposit(1000))

# A class attribute

tom_account = Account('Tom')
jim_account = Account('Jim')

print(tom_account.interest)
print(tom_account.interest)

Account.interest = 0.04

print(tom_account.interest)
print(jim_account.interest)

# 赋值

jim_account.interest = 0.08

print(jim_account.interest)
print(tom_account.interest)

Account.interest = 0.05  # changing the class attribute
print(tom_account.interest)  # changes instances without like-named instance attributes
print(jim_account.interest)  # but the existing instance attribute is unaffected


# 2.5.5 继承

class Account(object):
    """A bank account that has a non-negative balance."""
    interest = 0.02

    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder

    def deposit(self, amount):
        """Increase the account balance by amount and return the new balance."""
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount):
        """Decrease the account balance by amount and return the new balance."""
        if amount > self.balance:
            return 'Insufficient funds'
        self.balance = self.balance - amount
        return self.balance


class CheckingAccount(Account):
    """A bank account that charges for withdrawals."""
    withdraw_charge = 1
    interest = 0.01

    def withdraw(self, amount):
        return Account.withdraw(self, amount + self.withdraw_charge)


checking = CheckingAccount('Sam')

print(checking.deposit(10))
print(checking.withdraw(5))
print(checking.interest)


# 多重继承

class SavingAccount(Account):
    deposit_charge = 2

    def deposit(self, amount):
        return Account.deposit(self, amount - self.deposit_charge)


class AsSeenOnTVAccount(CheckingAccount, SavingAccount):
    def __init__(self, account_holder):
        self.holder = account_holder
        self.balance = 1  # A free dollar!


such_a_deal = AsSeenOnTVAccount("john")

print(such_a_deal.balance)
print(such_a_deal.deposit(20))
print(such_a_deal.withdraw(5))

# Python 使用一种叫做 C3 Method Resolution Ordering 的递归算法来解析名称
print([c.__name__ for c in AsSeenOnTVAccount.mro()])