import cmd
import socket
import subprocess
import threading
from pygame import mixer
import os
import math
import dsp

class Pippi(cmd.Cmd):
    """ Pippi Console 
    """

    prompt = 'pippi: '
    intro = 'Pippi Console'

    voices = [] 
    channels = []
    stopped = []
    renders = []
    cc = {} 

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.condition = threading.Condition()
        self.m = Mixer(mixer, self.renders, self.voices, self.channels, self.condition)
        self.m.start()

    def play(self, cmd):
        orcs = os.listdir('orc/')
        for orc in orcs:
            if cmd[0] == orc[0:2]:
                t = cmd[0]
                cmd.pop(0)
                orc = 'orc.' + orc.split('.')[0]
                p = __import__(orc, globals(), locals(), ['play'])

                for c in self.cc:
                    if c == t or c == 'g':
                        cmd = cmd + self.cc[c]

                Voice(p.play, t, cmd, self.renders, self.voices, self.condition).start()

                return True

        print 'not found'

    def do_s(self, cmd):
        cmds = cmd.split(' ')

        channel = self.channels[int(cmds[0])]
        try:
            channel[0].fadeout(1500 + dsp.randint(0, 500))
            self.voices.append((channel[0].get_sound(), channel[1], channel[2]))
        except AttributeError:
            pass

        self.channels.remove(channel)

    def do_p(self, cmd):
        cmds = cmd.split(' ')

        sound = self.voices[int(cmds[0])]
        self.channels.append((sound[0].play(-1), sound[1], sound[2]))
        self.voices.remove(sound)

        self.do_i()

    def do_c(self, cmd):
        cmd = cmd.split(' ')
        t = cmd[0]
        cmd.pop(0)
        self.cc[t] = cmd

    def do_v(self, cmd):
        cmds = cmd.split(' ')

        channel = self.channels[int(cmds[0])]

        try:
            current = channel[0].get_volume()
            target = float(cmds[1])
            
            if target == current:
                return

            diff = target - current
            diff /= 100.0

            for i in range(100):
                current += diff 
                channel[0].set_volume(current)
                dsp.delay(0.01)
        except AttributeError:
            pass

        self.do_i()
    

    def do_i(self, cmd=[]):
        print
        for i, channel in enumerate(self.channels):
            t = channel[1]
            p = channel[2]
            try:
                print t, 'C:', i, 'V:', channel[0].get_volume(), 'L:', channel[0].get_sound().get_length(), 'P:', p
            except AttributeError:
                pass
        print

        for i, voice in enumerate(self.voices):
            print 'Available:', i, 'Length:', voice[0].get_length()

        print

    def default(self, cmd):
        self.play(cmd.split(' '))

    def do_EOF(self, line):
        return True

    def postloop(self):
        if self.m.mixer.get_init() is not None:
            self.m.mixer.quit()
            print 'Closing ALSA connection'

class Voice(threading.Thread):
    def __init__(self, play, type, args, renders, voices, condition):
        threading.Thread.__init__(self)
        self.play = play
        self.type = type
        self.args = args
        self.voices = voices
        self.renders = renders
        self.condition = condition

    def run(self):
        self.condition.acquire()
        self.renders += [ (self.play(self.args), self.type, self.args) ]
        self.condition.notify()
        self.condition.release()

class Mixer(threading.Thread):
    def __init__(self, mixer, renders, voices, channels, condition):
        threading.Thread.__init__(self)
        self.condition = condition
        self.voices = voices
        self.channels = channels
        self.renders = renders
        self.mixer = mixer

    def run(self):
        while True:
            self.condition.acquire()
            if self.renders == []:
                self.condition.wait()
            else:
                for render in self.renders:
                    if self.mixer.get_init() is None:
                        self.mixer.init(frequency=44100, size=-16, channels=2)

                    s = self.mixer.Sound(render[0])
                    self.channels.append((s.play(-1), render[1], render[2]))

                    self.renders.remove(render)

            self.condition.release()


if __name__ == '__main__':
        # Create console
        console = Pippi()

        # Start looping command prompt
        console.cmdloop()
