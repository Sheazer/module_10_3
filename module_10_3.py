# from threading import Thread, Lock
#
# x = 0
#
# lock = Lock()
#
#
# def thread_task1():
#     global x
#
#     for i in range(10_000_000):
#         with lock:
#             x = x + 1
#
#
# def thread_task():
#     global x
#
#     for i in range(1_000_000):
#         try:
#             lock.acquire()
#             x = x + 1
#         finally:
#             lock.release()
#
#
# def main():
#     global x
#     x = 0
#
#     t1 = Thread(target=thread_task)
#     t2 = Thread(target=thread_task)
#
#     t1.start()
#     t2.start()
#
#     t1.join()
#     t2.join()
#
#
# for i in range(10):
#     main()
#     print(x)
#

from threading import Thread, Lock
from random import randint
from time import sleep


class Bank(Thread):

    def __init__(self):
        super().__init__()
        self.lock = Lock()
        self.balance = 0

    def deposit(self):
        n = 100
        for _ in range(n):
            x = randint(100, 200)
            sleep(0.001)
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            self.balance += x
            print(f'Пополнение: {x} Баланс: {self.balance}')

    def take(self):
        n = 100
        for _ in range(n):
            x = randint(200, 300)
            sleep(0.001)
            print(f'Запрос на {x}')
            if self.balance - x >= 0:
                self.balance -= x
                print(f'Снятие: {x}. Баланс: {self.balance}')
            else:
                print('Запрос отклонён, недостаточно средств')
                self.lock.acquire()



bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = Thread(target=Bank.deposit, args=(bk,))
th2 = Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
