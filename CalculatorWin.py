import tkinter
import keyboard
import math


global screenWidth, screenHeight

root = tkinter.Tk()
screenWidth = 1680 # root.winfo_screenwidth()
screenHeight = 1050 # root.winfo_screenheight()
root.withdraw()
root.title("Calculator")
root.geometry("%sx67+0+%s" % (screenWidth, screenHeight-140))
root.resizable(False, False)
root.overrideredirect(True)
root.attributes("-topmost", True)


class CalculatorMain:

    def __init__(self, main):

        self.magicFrame = tkinter.Frame(main)  # all the other grid elements (in column 0) are relative to this one so by giving it monitor width, the other frames have it too
        self.magicFrame.config(height=0, width=screenWidth)
        self.magicFrame.grid(row=0, column=0, sticky="WE")

        self.numberLayoutFrame = tkinter.Frame(main)
        self.numberLayoutFrame.config(height=20)
        self.numberLayoutFrame.grid(row=1, column=0, sticky="WE")
        self.numberLayoutFrame.grid_remove()

        self.buttonMenuFrame = tkinter.Frame(main)
        self.buttonMenuFrame.config(height=20)
        self.buttonMenuFrame.grid(row=2, column=0, sticky="WE")

        self.inputFrame = tkinter.Frame(main)
        self.inputFrame.config(height=40)
        self.inputFrame.grid(row=3, column=0, sticky="WE")

    def showANDhide(self, main, event=None):
        if 'normal' == main.state():
            main.withdraw()
            calcInput.userInputEntry.delete(0, tkinter.END)
        else:
            main.deiconify()


class CalculatorInput:

    def __init__(self, frame):
        self.userInputEntry = tkinter.Entry(frame, font=("Helvetica", 20), takefocus=1)
        self.userInputEntry.pack(fill=tkinter.BOTH)

    def calculateUserInput(self, event=None):

        try:
            result = eval(self.userInputEntry.get())
        except:
            result = "error"

        self.userInputEntry.delete(0, tkinter.END)
        self.userInputEntry.insert(0, result)

    def clearUserInput(self):
        self.userInputEntry.delete(0, tkinter.END)

    def clearLastInputedChar(self):
        get = self.userInputEntry.get()[:-1]
        self.userInputEntry.delete(0, tkinter.END)
        self.userInputEntry.insert(0, get)

class CalculatorButtonMenu:

    def __init__(self, frame, main):
        self.exitButton = tkinter.Button(frame, text="x", command=lambda: self.closeWindow(main))
        self.exitButton.grid(row=0, column=0)

        self.btnClear = tkinter.Button(frame, text="C", command=lambda: calcInput.clearUserInput())
        self.btnClear.grid(row=0, column=1)

        self.btnEquals = tkinter.Button(frame, text="=", command=lambda: calcInput.calculateUserInput())
        self.btnEquals.grid(row=0, column=3)

        self.numberLayoutPopUp = tkinter.Button(frame, text="^", command=lambda: self.popUpCommonCharWindow(main))
        self.numberLayoutPopUp.grid(row=0, column=2)

        self.btnPlus = tkinter.Button(frame, text="+", command=lambda: calcNumberLayout.insertInUserInputEntry(self.btnPlus.cget('text')))

        self.btnMinus = tkinter.Button(frame, text="-", command=lambda: calcNumberLayout.insertInUserInputEntry(self.btnMinus.cget('text')))

        self.btnMultiply = tkinter.Button(frame, text="*", command=lambda: calcNumberLayout.insertInUserInputEntry(self.btnMultiply.cget('text')))

        self.btnDivide = tkinter.Button(frame, text="/", command=lambda: calcNumberLayout.insertInUserInputEntry(self.btnDivide.cget('text')))

        self.btnGrade = tkinter.Button(frame, text="**", command=lambda: calcNumberLayout.insertInUserInputEntry("**"))


    def closeWindow(self, main):
        main.destroy()

    def popUpCommonCharWindow(self, main):
        if calc.numberLayoutFrame.winfo_ismapped():
            calc.numberLayoutFrame.grid_remove()
            main.geometry("%sx67+0+%s" % (screenWidth, screenHeight-109))

            calcButtonMenu.btnPlus.grid_forget()
            calcButtonMenu.btnMinus.grid_forget()
            calcButtonMenu.btnMultiply.grid_forget()
            calcButtonMenu.btnDivide.grid_forget()
            calcButtonMenu.btnGrade.grid_forget()

        else:
            main.geometry("%sx98+0+%s" % (screenWidth, screenHeight-140))
            calc.numberLayoutFrame.grid()

            calcButtonMenu.btnPlus.grid(row=0, column=4)
            calcButtonMenu.btnMinus.grid(row=0, column=5)
            calcButtonMenu.btnMultiply.grid(row=0, column=6)
            calcButtonMenu.btnDivide.grid(row=0, column=7)
            calcButtonMenu.btnGrade.grid(row=0, column=8)


class CalculatorNumberLayout:

    def __init__(self, frame):

        self.btn1 = tkinter.Button(frame, text="1", command=lambda: self.insertInUserInputEntry(self.btn1.cget('text')))
        self.btn1.pack(side="left")
        self.btn2 = tkinter.Button(frame, text="2", command=lambda: self.insertInUserInputEntry(self.btn2.cget('text')))
        self.btn2.pack(side="left")
        self.btn3 = tkinter.Button(frame, text="3", command=lambda: self.insertInUserInputEntry(self.btn3.cget('text')))
        self.btn3.pack(side="left")
        self.btn4 = tkinter.Button(frame, text="4", command=lambda: self.insertInUserInputEntry(self.btn4.cget('text')))
        self.btn4.pack(side="left")
        self.btn5 = tkinter.Button(frame, text="5", command=lambda: self.insertInUserInputEntry(self.btn5.cget('text')))
        self.btn5.pack(side="left")
        self.btn6 = tkinter.Button(frame, text="6", command=lambda: self.insertInUserInputEntry(self.btn6.cget('text')))
        self.btn6.pack(side="left")
        self.btn7 = tkinter.Button(frame, text="7", command=lambda: self.insertInUserInputEntry(self.btn7.cget('text')))
        self.btn7.pack(side="left")
        self.btn8 = tkinter.Button(frame, text="8", command=lambda: self.insertInUserInputEntry(self.btn8.cget('text')))
        self.btn8.pack(side="left")
        self.btn9 = tkinter.Button(frame, text="9", command=lambda: self.insertInUserInputEntry(self.btn9.cget('text')))
        self.btn9.pack(side="left")
        self.btn0 = tkinter.Button(frame, text="0", command=lambda: self.insertInUserInputEntry(self.btn0.cget('text')))
        self.btn0.pack(side="left")
        self.btnClearOne = tkinter.Button(frame, text="<-", command=lambda: calcInput.clearLastInputedChar())
        self.btnClearOne.pack(side="left")

    def insertInUserInputEntry(self, char):
        calcInput.userInputEntry.insert(tkinter.END, char)


global calc, calcButtonMenu, calcInput, calcNumberLayout
calc = CalculatorMain(root)
calcInput = CalculatorInput(calc.inputFrame)
calcButtonMenu = CalculatorButtonMenu(calc.buttonMenuFrame, root)
calcNumberLayout = CalculatorNumberLayout(calc.numberLayoutFrame)


keyboard.add_hotkey("ctrl+space", lambda: calc.showANDhide(root))
root.bind('<Return>', lambda event: calcInput.calculateUserInput())

root.mainloop()
