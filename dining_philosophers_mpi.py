__author__ = 'nidzo17'

# The Dining Philosophers Problem using MPI

from mpi4py import MPI
from time import sleep
from random import randint

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

class philosopher:
    def __init__(self):
        self.left_neighbor = size - 1 if rank == 0 else rank - 1
        self.right_neighbor = 0 if rank == size - 1 else rank + 1
        self.left_fork = '0'
        self.right_fork = 'dirty'
        if (rank == size - 1):
            self.right_fork = '0'
        if rank == 0:
            self.left_fork = 'dirty'
            self.right_fork = 'dirty'
        self.requests = []

    def think(self):
        self.print_msg("thinking...")
        rand = randint(5,8)
        while rand > 0:
            rand -= 1
            self.check()
            sleep(0.8)
        return

    def check(self):
        for request in self.requests:
            if request == self.left_neighbor:
                self.requests.remove(self.left_neighbor)
                if self.left_fork == 'dirty':
                    #self.print_msg("Sending left fork")
                    comm.send('clean', dest=request)
                    self.left_fork = '0'
            if request == self.right_neighbor:
                self.requests.remove(self.right_neighbor)
                if self.right_fork == 'dirty':
                    #self.print_msg("Sending right fork")
                    comm.send('clean', dest=request)
                    self.right_fork = '0'

        self.requests=[]
        if comm.Iprobe(self.left_neighbor):
            self.handle(self.left_neighbor)

        elif comm.Iprobe(self.right_neighbor):
            self.handle(self.right_neighbor)

    def handle(self, neighbor):
        if neighbor == self.left_neighbor:
            msg = comm.recv(source=self.left_neighbor)
            if msg == 'clean':
                self.left_fork = msg
                #self.print_msg("Left fork received")
            elif msg == 'Requesting ':
                if self.left_fork == 'dirty':
                    #self.print_msg("Sending left fork ")
                    comm.send('clean', dest=neighbor)
                    self.left_fork = '0'
                else:
                    if neighbor not in self.requests:
                        self.requests.append(neighbor)

        if neighbor == self.right_neighbor:
            msg2 = comm.recv(source=self.right_neighbor)
            if msg2 == 'clean':
                self.right_fork = msg2
                #self.print_msg("Right fork received")
            elif msg2 =='Requesting ':
                if self.right_fork == 'dirty':
                    #self.print_msg("Sending right fork")
                    comm.send('clean', dest=neighbor)
                    self.right_fork = '0'
                else:
                    if neighbor not in self.requests:
                        self.requests.append(neighbor)

    def fork_request(self):
        self.print_msg("Starving...")
        var = 6
        while self.left_fork == '0' or self.right_fork == '0':
            if self.left_fork == '0' and var > 3:
                self.print_msg("Requesting left fork")
                comm.send('Request', dest=self.left_neighbor)
                var=0
            if self.right_fork == '0' and var > 3:
                self.print_msg("Requesting right fork")
                comm.send('Request', dest=self.right_neighbor)
                var=0
            self.check()
            sleep(0.5)
            var+=1

    def eat(self):
        self.print_msg("Eating...")
        sleep(randint(2,5))
        self.left_fork='dirty'
        self.right_fork='dirty'
        self.print_msg("Eating finished...")

    def print_msg(self, msg):
        print('\t\t '*rank + msg)

if __name__ == "__main__":
    phil = philosopher()
    while(1):
        phil.think()
        phil.fork_request()
        phil.eat()
