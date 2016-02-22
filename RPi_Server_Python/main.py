#Name: main.py
#Author: John Board
#Date: 11/02/2016
#Description: Main file.

from cvhandler import CVHandler
from config import LOGGING_NAME
import logging, datetime, time
from os import path
from code import InteractiveConsole
import cProfile, pstats, StringIO

class AirHockeyTable():
    def __init__(self):
        self.running = True     #Global running flag. Make false to stop main loop.

    def start(self):
        self.initLogging()

        self.logger.debug("Initializing CV handler...")
        self.cv = CVHandler()
        self.cv.start()


        #self.startInteractiveShell()

        self.running = True
        self.loop()

    """
    Initialize console and file logging. File logging disabled.
    """
    def initLogging(self):
        self.logger = logging.getLogger(LOGGING_NAME)
        self.logger.setLevel(logging.DEBUG)

        try:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')# %H.%M.%S')
            fh = logging.FileHandler(path.join(path.dirname(__file__), "logs/%s.txt"%st))
            fh.setLevel(logging.DEBUG)
        except IOError:
            print("Create 'logs' directory in program's root directory.")

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter("%(created)f %(thread)d %(filename)s,%(lineno)d %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        #self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    """
    Starts interactive python console. Runs on the main thread, while the loop runs in another thread.
    """
    def startInteractiveShell(self):
        vars = globals()
        vars.update(locals())
        shell = InteractiveConsole(vars)
        shell.interact()

    def stop(self):
        if self.running == True:        #If stop hasn't been called before...
            self.running = False
        else:                           #If stop has been called before...
            self.cv.stop()

    def loop(self):
        while self.running:


            self.cv.tick()


            #self.cv.tick()

#Checks to see whether the file was imported or run as standalone
if __name__ == "__main__":
    app = AirHockeyTable()
    app.start()