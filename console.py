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

    # Default fundamental frequency
    freq = 220.0 # Oh, so western!

    # Default octave multiplier
    octave = 1.0

    # Default drift speed for overtones
    drift_speed = 0.3

    # Default just diatonic scale
    diatonic = [
        (1.0, 1.0),  # 1:1  P1 C
        (9.0, 8.0),  # 9:8  M2 D
        (5.0, 4.0),  # 5:4  M3 E
        (4.0, 3.0),  # 4:3  P4 F
        (3.0, 2.0),  # 3:2  P5 G
        (5.0, 3.0),  # 5:3  M6 A
        (15.0, 8.0), # 15:8 M7 B
        ]

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
        cmds = cmd.split(',')

        for cmd in cmds:
            self.overtones(cmd)

    def overtones(self, cmd):
        """ 
        interact with overtones 

        an overtone in pippi is actually
        a single wavetable osc in pd.
        pippi has 6 overtones in total, each 
        with a set of partials rendered as a wavetable.
        Three groups of overtones, two channels each.

        a 1, a 2
        b 1, b 2
        c 1, c 2

        """

        group = ''
        channel = ''
        operation = ''

        cmd = cmd.split()

        # 0th index tells us which overtone to route to, 
        # or implicitly refers to all overtones in the 
        # absence of a group or channel specification.
        # It also tells us which operation to perform.
        #
        # eg: 
        #   af [ a 1 f, a 2 f]
        #   bv [ b 1 v, b 2 v]
        #   a1f [ a 1 f ]
        #
        # the first character denotes group, the second 
        # is the channel, and the third is the operation

        # strip whitespace from command elements
        for i, s in enumerate(cmd):
            cmd[i].strip()

        if len(cmd[0]) == 3:
            # Operations on a single group channel
            group = cmd[0][0:1]
            channel = cmd[0][1:2]
            operation = cmd[0][2:3]
        elif len(cmd[0]) == 2:
            # Operations on all channels of a group
            group = cmd[0][0:1]
            operation = cmd[0][1:2]
        elif len(cmd[0]) == 1:
            # Operations on all channels of all groups
            operation = cmd[0]

        # Construct a well formed selection message
        selection = 'overtone '

        if group == '' and channel == '':
            selection += 'all'
        elif channel == '':
            selection += group
        else:
            selection += group + channel

        # We're done with the 0th element, next we parse 
        # operation arguments from the remaining list items
        cmd.pop(0)

        # Construct a well formed operation message
        if operation == 'f':
            # Change the fundamental frequency

            # Now the 0th element will be an indication of a few 
            # possible things:
            #       - absolute frequency in hz
            #       - diatonic scale degree
            #       - ratio

            if cmd[0][0:1] == 's':
                # Set freq to diatonic scale degree

                cmd[0] = cmd[0][1:] # strip 's' 

                # self.diatonic counts from 0, as is the convention in python
                # scale degrees are inputted counting from 1, as is the convention 
                # in western musical notation. so subtract 1!
                degree = int(cmd[0]) - 1

                # now we see if a different fundamental frequency has been specified
                # as well as if an octave offset has been specified
                if len(cmd) == 3:
                    octave = float(cmd[1])
                    freq = float(cmd[2])
                elif len(cmd) == 2:
                    octave = float(cmd[1])
                    freq = self.freq
                elif len(cmd) == 1:
                    octave = self.octave
                    freq = self.freq

                ratio = self.diatonic[degree]
                
                freq = (ratio[0] / ratio[1]) * freq * octave

            elif cmd[0][0:1] == 'r':
                # Set freq to ratio
                # !TODO implement this...
                pass
            else:
                # Assume anything else is an absolute frequency
                freq = float(cmd[0])

            operation = 'freq ' + str(freq)

        elif operation == 'v':
            # Change the volume
            operation = 'volume ' + cmd[0]
        elif operation == 'p':
            # Select partials and their maximum amplitudes
            pass
        elif operation == 'n':
            # Adjust noise mix
            operation = 'noise ' + cmd[0]
        elif operation == 'd':
            # Adjust drift
            if len(cmd) == 2:
                drift_width = cmd[0]
                drift_speed = cmd[1]
            elif len(cmd) == 1:
                drift_width = cmd[0]
                drift_speed = str(self.drift_speed)

            operation = 'drift ' + drift_width + ' ' + drift_speed 

        msg = selection + ' ' + operation

        # Okay, now actually send the message along to pd!
        self.pd.send([msg])

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
