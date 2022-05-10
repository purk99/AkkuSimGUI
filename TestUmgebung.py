from tkinter import *
from tkinter import ttk

from time import sleep
from timer import *

t1 = AsyncTimer()

root = Tk()
root.title("Testfenster")

mainframe = ttk.Frame(root)
mainframe.grid()

val1 = StringVar()
t1.start()

tL = ttk.Label(mainframe,textvariable=val1)
#tL = ttk.Label(mainframe,text="Test")
tL.grid(column=1,row=1)

uB = ttk.Button(mainframe,text="Starte Counter",command=lambda:t1.run(10))

eb = ttk.Button(mainframe,text="Exit",command=root.destroy)
eb.grid(column=10,row=10)

root.mainloop()




