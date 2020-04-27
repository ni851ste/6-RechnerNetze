from threading import Thread, Event

n = 0
L = []
global s
sdf = 0
listEv = Event()
sumEv = Event()
addEv = Event()
stopEv = Event()


def copy():
    while True:
        listEv.wait(timeout=1)
        if stopEv.is_set():
            break
        if listEv.is_set():
            L.append(n)
            listEv.clear()
            print('Copy')
            sumEv.set()
    print('Ending Copy')


def summe():
    global sdf
    while True:
        sumEv.wait(timeout=1)
        if stopEv.is_set():
            break
        if sumEv.is_set():
            sdf = sdf + L[-1]
            sumEv.clear()
            print('Sum')
            addEv.set()
    print('Ending Sum')


def add(N):
    global n
    while True:
        addEv.wait(timeout=1)
        if stopEv.is_set():
            break
        if addEv.is_set():
            n = n + 1
            if n > N:
                stopEv.set()
            addEv.clear()
            print('Add %d' % n)
            listEv.set()
    print('Ending Add')


N = 500
a = Thread(target=add, args=(N,))
c = Thread(target=copy)
s = Thread(target=summe)
a.start()
c.start()
s.start()
addEv.set()
