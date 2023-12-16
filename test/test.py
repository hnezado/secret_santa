from tkinter import *
import Pmw

root = Tk()

Pmw.initialise(root) #initializing it in the root window

l = Label(root,text='Random Text')
l.pack()

b = Button(root,text='Hover me')
b.pack()

tooltip_1 = Pmw.Balloon(root) #Calling the tooltip
tooltip_1.bind(b,'This is the hover Text\nHope you get an idea of whats going on here.') #binding it and assigning a text to it

root.mainloop()