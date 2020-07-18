import tkinter
import keyboard

master = tkinter.Tk()
master.withdraw()
master.title("Calculator")
master.geometry("%sx40+0+%s" % (master.winfo_screenwidth(), master.winfo_screenheight()-40))
master.resizable(False, False)
master.wm_attributes('-type', 'splash')
master.attributes("-topmost", True)


class Calculator:

    def __init__(self, main):

        self.entryUserInput = tkinter.Entry(main, width=main.winfo_screenwidth(), font=("Helvetica", 20))
        self.entryUserInput.grid(column=1, row=0)
        self.calculateButton = tkinter.Button(main, text="calculate", command=self.calculateUserInput)
        self.calculateButton.grid(column=0, row=0)


    def calculateUserInput(self, event=None):

        try:
            result = eval(self.entryUserInput.get())
        except:
            result = "error"

        self.entryUserInput.delete(0, tkinter.END)
        self.entryUserInput.insert(0, result)

    def showANDhide(self, main, event=None):
        if 'normal' == main.state():
            main.withdraw()
            self.entryUserInput.delete(0, tkinter.END)
        else:
            main.deiconify()


calc = Calculator(master)

keyboard.add_hotkey("ctrl+q", lambda: calc.showANDhide(master))
master.bind('<Return>', lambda event: calc.calculateUserInput())

master.mainloop()
