from threading import Thread

n = 0


def add1(N):
    # Global n and "n=0" above are the same variable
    # global is needed to change n from the global scope
    global n
    while n < N:
        n = n + 1
        print('Add1: %d' % n)


class Adder(Thread):

    def __init__(self, changeN, N):
        Thread.__init__(self)
        self.changeN = changeN
        self.N = N

    def run(self):
        global n
        while n < self.N:
            n = n + self.changeN
            print('Adder Class %d: %d' % (self.changeN, n))


maxCount = 100

# a = Thread(target=add1, args=(maxCount,))
a2 = Adder(1, maxCount)
s2 = Adder(-1, maxCount)

# start calls for the Threads own "run()" method
a2.start()
# a.start()
s2.start()
