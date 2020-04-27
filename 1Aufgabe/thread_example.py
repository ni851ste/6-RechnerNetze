from threading import Thread

n = 0


def add1(N):
    global n
    while n < N:
        n = n + 1
        print('Add1: %d' % n)


class Adder(Thread):
    def __init__(self, n, N):
        Thread.__init__(self)
        self.n = n
        self.N = N

    def run(self):
        global n
        while n < self.N:
            n = n + self.n
            print('Adder Class %d: %d' % (self.n, n))


N = 500
a = Thread(target=add1, args=(N,))
a2 = Adder(2, N)
s2 = Adder(-2, N)
a2.start()
a.start()
s2.start()
