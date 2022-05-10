from time import sleep
from threading import Thread
from tkinter import StringVar

class AsyncTimer(Thread):
    def __init__(self):
        super().__init__()
        self.time = StringVar()

    def run(self,dur):
        self.time = dur
        while self.time >= 0:
            #print("Thread läuft")
            self.time -= 1
            sleep(1)

        if self.time == 0:
            self.time = dur

    def getTime(self):
        return self.time


    def countdown(self,dur):
        while dur:
            m,s = divmod(dur,60)
            min_sec_format = '{:02d}:{:02d}'.format(m, s)
            print(min_sec_format, end='\r')
            sleep(1)
            dur -= 1

        print("Countdown finished")

    def countdownsecs(self,dur):
        while dur:
            secFormat = '{:02d}'.format(dur)
            print(secFormat, end='\r')
            sleep(1)
            dur -= 1
        print("Countdown 1 finished")
