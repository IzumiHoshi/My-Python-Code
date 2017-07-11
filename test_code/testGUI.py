from tkinter import *


# class App(Frame):
#     def __init__(self, master=None):
#         Frame.__init__(self, master)
#         self.pack()
#         self.createWidgets()
#
#     def createWidgets(self):
#         self.helloLabel = Label(self, text='Hello, world!')
#         self.helloLabel.pack()
#         self.quitButton = Button(self, text='quit!', command=self.quit)
#         self.quitButton.pack()

import tkinter.messagebox as messagebox

class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertButton = Button(self, text='Fuck', command=self.hello)
        self.alertButton.pack()

        self.helloLabel = Label(self, text='Hello, world!')
        self.helloLabel.pack()
        self.quitButton = Button(self, text='quit!', command=self.quit)
        self.quitButton.pack()

    def hello(self):
        name = self.nameInput.get() or 'shit'
        messagebox.showinfo('Message','Shit, %s' % name)



app = App()
app.master.title('Fuck you world')
app.mainloop()