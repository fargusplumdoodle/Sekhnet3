import random
import time
from Printer import VerbosityPrinter as vp
import socket
import threading


class Client(threading.Thread):

    def __init__(self, port, name=0, verbose=4):

        super(Client, self).__init__()

        self.verbose = verbose
        self.name = 'Client-%s' % name
        self.vp = vp(self.verbose, name=self.name)

        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.pl = 1024

    def run(self):
        try:
            self.c.connect( ('localhost', self.port) )
            #self.vp.print('Waiting for connection', 4)

            data = self.c.recv(self.pl)
            self.vp.print('Start')
            # connection established
            # waiting for a random amount of time
            prob = random.choice(range(10))
            time.sleep(prob)
            self.c.send(b'DONE')
            self.vp.print('Finished')
        except Exception as e:
            self.vp.pritn('Error: %s' % str(e))
            self.c.close()
            exit(2)

    def get_data(self,  timeout=10):
        data = []
        for x in range(timeout):
            chunk = self.c.recv(self.pl)
            if chunk == b'':
                return b''.join(data)
            else:
                data.append(chunk)
        raise ConnectionError('Error: No data recieved in %s tries' % timeout)

