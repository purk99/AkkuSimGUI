from tkinter import *
from tkinter import ttk

from time import sleep
#from timer import *

root = Tk()
root.title("Testfenster")

mainframe = ttk.Frame(root)
mainframe.grid()

tL = ttk.Label(mainframe,text="Test")
tL.grid(column=1,row=1)

eb = ttk.Button(mainframe,text="Exit",command=root.destroy)
eb.grid(column=10,row=10)


