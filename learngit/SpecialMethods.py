from functools import total_ordering


@total_ordering
class Account:#帐号的类
    def __init__(self, owner, amount=0):
        self.owner = owner
        self.amount = amount
        self._transactions = []  #原来狗子真的会条件反射

    def __len__(self):  #获取交易次数
        return len(self._transactions)

    def __repr__(self):
        return 'Account({!r},{!r})'.format(self.owner,self.amount)

    def __str__(self):
        return 'Account {} with starting amount: {}'.format(self.owner,self.amount)

    def __getitem__(self, position):#获取元素
        return self._transactions[position]

    def __reversed__(self):#反向列表利用切片
        return self[::-1]

    def __eq__(self, other):#如果相等返回布尔值TRUE
        return self.balance == other.balance

    def __lt__(self, other):
        return self.balance < other.balance

    def __add__(self, other):#合并
        owner='{}&{}'.format(self.owner,other.owner)
        start_amount=self.amount+other.amount
        acc = Account(owner,start_amount)
        for t in  list(self)+ list(other):
            acc.add_transcation(t)
        return acc

    def __call__(self):#将类转换为方法 例如acc()
        print('Start amount:{}'.format(self.amount))
        print('Transactions:')
        for transaction in self:#输出每一个元素
            print(transaction)
        print('\nBalance: {}'.format(self.balance))

    def __enter__(self):
        print('ENTER WITH:Making backup of transactions for rollback')
        self._copy_transactions=list(self._transactions)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('EXIT WTIH',end=' ')
        if exc_tb:
            self._transactions=self._copy_transactions
            print('Rolling back to previous transactions')
            print('Transaction resulted in {} ({})'.format(exc_type.__name__,exc_val))
        else:
            print('Transaction OK')

    def add_transcation(self, amount):#存或者取钱,判断是否是INT类型的量
        if not isinstance(amount,int):
            raise ValueError('please use int for amount')
        self._transactions.append(amount)

    @property#把方法变成属性调用
    def balance(self):
        return self.amount+sum(self._transactions)


def validate_transaction(acc, amount_to_add):  #__enter__返回值给a
    with acc as a:
        print('Add {} to account'.format(amount_to_add))
        a.add_transcation(amount_to_add)
        print('New balance would be :{}'.format(a.balance))
        if a.balance < 0:
            raise ValueError('sorry cannot go in debt!')






if "__main__"==__name__:
    acc=Account('bob',10)
    acc.add_transcation(20)
    acc.add_transcation(-10)
    acc2=Account('tim',100)
    acc2.add_transcation(20)
    acc2.add_transcation(40)
    acc3=acc+acc2
    acc4=Account('sue', 10)
    print('\nBalance start:{}'.format(acc4.balance))
    try:
        validate_transaction(acc4,-50)
    except ValueError as exc:
        print(exc)
    print('\nBalance end :{}'.format(acc4.balance))
    # Account.print_statement()