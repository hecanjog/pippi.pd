import cmd
import socket
import subprocess
import threading
from multiprocessing import Process, Queue, current_process, freeze_support 
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
    renders = []

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.condition = threading.Condition()
        self.m = Mixer(mixer, self.renders, self.voices, self.condition)
        self.m.start()

    def play(self, cmd):
        orcs = os.listdir('orc/')
        for orc in orcs:
            if cmd[0] == orc[0:2]:
                cmd.pop(0)
                orc = 'orc.' + orc.split('.')[0]
                p = __import__(orc, globals(), locals(), ['play'])
                
                Voice(p.play, cmd, self.renders, self.voices, self.condition).start()

                return True

        print 'not found'

    def do_v(self, cmd):
        cmds = cmd.split(' ')

        voice = self.voices[int(cmds[0])]

        current = voice.get_volume()
        target = float(cmds[1])
        
        if target == current:
            return

        diff = target - current
        diff /= 100.0

        for i in range(100):
            current += diff 
            voice.set_volume(current)
            dsp.delay(0.01)

    def do_info(self, cmd):
        for i, voice in enumerate(self.voices):
            print 'Voice:', i, 'Volume:', voice.get_volume(), 'Length:', voice.get_length()
        print

    def default(self, cmd):
        self.play(cmd.split(' '))

    def do_EOF(self, line):
        return True

    def postloop(self):
        if self.m.mixer.get_init() is not None:
            self.m.mixer.quit()
            print 'Closing ALSA connection'

        return True

class Voice(threading.Thread):
    def __init__(self, play, args, renders, voices, condition):
        threading.Thread.__init__(self)
        self.play = play
        self.args = args
        self.voices = voices
        self.renders = renders
        self.condition = condition

    def run(self):
        self.condition.acquire()
        self.renders += [ self.play(self.args) ]
        self.condition.notify()
        self.condition.release()

class Mixer(threading.Thread):
    def __init__(self, mixer, renders, voices, condition):
        threading.Thread.__init__(self)
        self.condition = condition
        self.voices = voices
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

                    s = self.mixer.Sound(render)
                    s.play(-1)

                    self.renders.remove(render)
                    self.voices.append(s)

            self.condition.release()


if __name__ == '__main__':
        # Create console
        console = Pippi()

        # Start looping command prompt
        console.cmdloop()
