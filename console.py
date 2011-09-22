"""

Pippi Console

I'm grateful to Doug Hellmann for his excellent 
introduction to Python's cmd module.
doughellmann.com/PyMOTW/cmd/

This script also makes use (of course) of the 
excellent dos.python.org documentation on sockets:
docs.python.org/library/socket.html

And PD's documentation of the FUDI protocal:
wiki.puredata.info/en/FUDI

This script just acts as a console interface to PD, 
and doesn't do any dynamic patching. 

If you're interested in that, check out purity, 
pyata, or pypd, which are all robust packages for 
dynamically creating puredata patches within python.
wiki.dataflow.ws/Purity
code.google.com/p/pyata
mccormick.cx/projects/PyPd/

"""

import cmd
import socket

class Pippi(cmd.Cmd):
    """ Pippi Console """

    prompt = 'pippi: '
    intro = 'Pippi Console'
    pd = '' # PdSend class instance lives here

    def do_pd(self, cmd):
        """ connect / disconnect from pd, 
        send pd messages directly """

        cmd = cmd.split()

        if cmd[0] == 'msg':
            cmd.pop(0)
            cmd = ' '.join(cmd)
            self.pd.send(['pd ' + cmd])
        elif cmd[0] == 'c':
            self.pd = PdSend()
        elif cmd[0] == 'd':
            self.pd.close()

    def do_o(self, cmd):
        """ interact with overtone group """

        cmd = cmd.split()

        if cmd[0] == 'v' or cmd[0] == 'f':
            cmd = ' '.join(cmd)
            self.pd.send(['overtone all ' + cmd])

    def do_EOF(self, line):
        return True

    def postloop(self):
        if self.pd.connected == True:
            print 'Disconnecting from PD'
            self.pd.close()
        print

class PdSend():
    """ Simple socket wrapper to talk FUDI with PD """
    pdhost = 'localhost'
    sport = 3000
    rport = 3001
    pd = '' # the socket object will live here
    connected = False # Totally bulletproof way to keep track of connection. Um.

    def __init__(self):
        self.connect()

    def connect(self):
        """ make a connection to pd """
        print 'Connecting to PD'
        try:
            self.pd = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create ipv4 socket
            self.pd.connect((self.pdhost, self.sport)) # make the connection
            self.connected = True
            print 'Sending to PD on port ' + str(self.sport)
        except:
            print 'Connection failed - open PD with [netreceive ' + str(self.sport) + '] at least!'

    def send(self, msgs):
        """ send a list of message strings to pd """
        try:
            for msg in msgs:
                msg = str(msg) + ';'
                self.pd.send(msg)
        except:
            print 'Could not send. Did you open a connection?'

    def close(self):
        """ close the socket connection """
        print 'Closing connection to PD'
        self.pd.close()
        self.connected = False

    def format(self, target, msgs):
        """ format a list of messages into message strings """
        for msg, index in enumerate(msgs):
            msgs[index] = target + ' ' + msg

        return msgs


if __name__ == '__main__':
        # Create console
        console = Pippi()

        # Start looping command prompt
        console.cmdloop()
