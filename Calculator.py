import tkinter
import keyboard
import math
import datetime
import subprocess


global screenWidth, screenHeight

master = tkinter.Tk()
screenWidth = 1680 # master.winfo_screenwidth()
screenHeight = 1050 # master.winfo_screenheight()
master.withdraw()
master.title("Calculator")
master.geometry("%sx67+0+%s" % (screenWidth, screenHeight-40))
master.resizable(False, False)
master.wm_attributes('-type', 'splash')
master.attributes("-topmost", True)


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

        command = self.userInputEntry.get()
        try:
            result = eval(command)
        except:
            result = "error"

        self.addToHistory(command, result)

        self.userInputEntry.delete(0, tkinter.END)
        self.userInputEntry.insert(0, result)

    def clearUserInput(self):
        self.userInputEntry.delete(0, tkinter.END)

    def clearLastInputedChar(self):
        get = self.userInputEntry.get()[:-1]
        self.userInputEntry.delete(0, tkinter.END)
        self.userInputEntry.insert(0, get)

    def addToHistory(self, command, result):
        histFilename = 'calculatorHistory.txt'
        try:
            file = open(histFilename, 'x')
        except FileExistsError:
            file = open(histFilename, 'a')

        file.write("\nEXPRESSION: %s=%s   DATE: %s" % (command, result, datetime.datetime.now()))
        file.close()

class CalculatorButtonMenu:

    def __init__(self, frame, main):

        self.btnClear = tkinter.Button(frame, text="C", command=lambda: calcInput.clearUserInput())
        self.btnClear.pack(side="left")

        self.btnEquals = tkinter.Button(frame, text="=", command=lambda: calcInput.calculateUserInput())
        self.btnEquals.pack(side="left")

        self.numberLayoutPopUp = tkinter.Button(frame, text="🠕", command=lambda: self.popUpCommonCharWindow(main))
        self.numberLayoutPopUp.pack(side="left")
        # self.numberLayoutPopUp.grid(row=0, column=2)

        self.btnPlus = tkinter.Button(frame, text="+", command=lambda: calcNumberLayout.insertInUserInputEntry(self.btnPlus.cget('text')))

        self.btnMinus = tkinter.Button(frame, text="-", command=lambda: calcNumberLayout.insertInUserInputEntry(self.btnMinus.cget('text')))

        self.btnMultiply = tkinter.Button(frame, text="*", command=lambda: calcNumberLayout.insertInUserInputEntry(self.btnMultiply.cget('text')))

        self.btnDivide = tkinter.Button(frame, text="/", command=lambda: calcNumberLayout.insertInUserInputEntry(self.btnDivide.cget('text')))

        self.btnGrade = tkinter.Button(frame, text="^", command=lambda: calcNumberLayout.insertInUserInputEntry("**"))

        self.exitButton = tkinter.Button(frame, text="x", command=lambda: self.closeWindow(main))
        self.exitButton.pack(side="right")

        self.histViewButton = tkinter.Button(frame, text="History", command=lambda: self.viewCalcHistory())
        self.histViewButton.pack(side="right")

    def closeWindow(self, main):
        main.destroy()

    def viewCalcHistory(self):
        subprocess.run(["gedit", "calculatorHistory.txt"], check=True)

    def popUpCommonCharWindow(self, main):
        if calc.numberLayoutFrame.winfo_ismapped():
            calc.numberLayoutFrame.grid_remove()
            master.geometry("%sx67+0+%s" % (screenWidth, screenHeight-40))

            calcButtonMenu.btnPlus.pack_forget()
            calcButtonMenu.btnMinus.pack_forget()
            calcButtonMenu.btnMultiply.pack_forget()
            calcButtonMenu.btnDivide.pack_forget()
            calcButtonMenu.btnGrade.pack_forget()

        else:
            main.geometry("%sx98+0+%s" % (screenWidth, screenHeight-40))
            calc.numberLayoutFrame.grid()

            calcButtonMenu.btnPlus.pack(side="left")
            calcButtonMenu.btnMinus.pack(side="left")
            calcButtonMenu.btnMultiply.pack(side="left")
            calcButtonMenu.btnDivide.pack(side="left")
            calcButtonMenu.btnGrade.pack(side="left")


class CalculatorNumberLayout:

    def __init__(self, frame):

        self.btn1 = tkinter.Button(frame, text="1", command=lambda: self.insertInUserInputEntry(self.btn1.cget('text')))
        self.btn1.pack(side="left")
        self.btn2 = tkinter.Button(frame, text="2", command=lambda: self.insertInUserInputEntry(self.btn2.cget('text')))
        self.btn2.pack(side="left")
        self.btne = tkinter.Button(frame, text="e", command=lambda: self.insertInUserInputEntry('math.e'))
        self.btne.pack(side="left")
        self.btn3 = tkinter.Button(frame, text="3", command=lambda: self.insertInUserInputEntry(self.btn3.cget('text')))
        self.btn3.pack(side="left")
        self.btnpi = tkinter.Button(frame, text="π", command=lambda: self.insertInUserInputEntry('math.pi'))
        self.btnpi.pack(side="left")
        self.btn4 = tkinter.Button(frame, text="4", command=lambda: self.insertInUserInputEntry(self.btn4.cget('text')))
        self.btn4.pack(side="left")
        self.btn5 = tkinter.Button(frame, text="5", command=lambda: self.insertInUserInputEntry(self.btn5.cget('text')))
        self.btn5.pack(side="left")
        self.btn6 = tkinter.Button(frame, text="6", command=lambda: self.insertInUserInputEntry(self.btn6.cget('text')))
        self.btn6.pack(side="left")
        self.btne = tkinter.Button(frame, text="𝜏", command=lambda: self.insertInUserInputEntry('math.tau'))
        self.btne.pack(side="left")
        self.btn7 = tkinter.Button(frame, text="7", command=lambda: self.insertInUserInputEntry(self.btn7.cget('text')))
        self.btn7.pack(side="left")
        self.btn8 = tkinter.Button(frame, text="8", command=lambda: self.insertInUserInputEntry(self.btn8.cget('text')))
        self.btn8.pack(side="left")
        self.btn9 = tkinter.Button(frame, text="9", command=lambda: self.insertInUserInputEntry(self.btn9.cget('text')))
        self.btn9.pack(side="left")
        self.btn0 = tkinter.Button(frame, text="0", command=lambda: self.insertInUserInputEntry(self.btn0.cget('text')))
        self.btn0.pack(side="left")
        self.btnClearOne = tkinter.Button(frame, text="⌫", command=lambda: calcInput.clearLastInputedChar())
        self.btnClearOne.pack(side="left")

    def insertInUserInputEntry(self, char):
        calcInput.userInputEntry.insert(tkinter.END, char)


global calc, calcButtonMenu, calcInput, calcNumberLayout
calc = CalculatorMain(master)
calcInput = CalculatorInput(calc.inputFrame)
calcButtonMenu = CalculatorButtonMenu(calc.buttonMenuFrame, master)
calcNumberLayout = CalculatorNumberLayout(calc.numberLayoutFrame)


keyboard.add_hotkey("ctrl+space", lambda: calc.showANDhide(master))
master.bind('<Return>', lambda event: calcInput.calculateUserInput())

master.mainloop()
