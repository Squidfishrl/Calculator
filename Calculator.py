import tkinter
from tkinter import ttk
import keyboard
import math
import datetime


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
global histFilename
histFilename = 'calculatorHistory.txt'


class CalculatorMain:

    def __init__(self, main):

        self.magicFrame = tkinter.Frame(main)  # all the other grid elements (in column 0) are relative to this one so by giving it monitor width, the other frames have it too
        self.magicFrame.config(height=0, width=screenWidth)
        self.magicFrame.grid(row=0, column=0, sticky="WE")

        # self.mathFunctionsFrame = tkinter.Frame(main)
        # self.mathFunctionsFrame.config(height=80, bg="red")
        # self.mathFunctionsFrame.grid(row=1, column=0)
        # self.mathFunctionsFrame.grid_remove()

        self.numberAndFuncLayoutFrame = tkinter.Frame(main)
        self.numberAndFuncLayoutFrame.config(height=20)
        self.numberAndFuncLayoutFrame.grid(row=2, column=0, sticky="WE")
        self.numberAndFuncLayoutFrame.grid_remove()

        self.buttonMenuFrame = tkinter.Frame(main)
        self.buttonMenuFrame.config(height=20)
        self.buttonMenuFrame.grid(row=3, column=0, sticky="WE")

        self.inputFrame = tkinter.Frame(main)
        self.inputFrame.config(height=40)
        self.inputFrame.grid(row=4, column=0, sticky="WE")
        self.inputFrame.focus_set()




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
        self.upAndDownKeyPress = 0

    def calculateUserInput(self, event=None):

        command = self.userInputEntry.get()
        command = command.rstrip('\n')
        try:
            result = eval(command)
        except:
            result = "error"

        self.addToHistory(command, result)

        self.userInputEntry.delete(0, tkinter.END)
        self.userInputEntry.insert(0, result)
        self.upAndDownKeyPress = 0

    def clearUserInput(self):
        self.userInputEntry.delete(0, tkinter.END)

    def clearLastInputedChar(self):
        get = self.userInputEntry.get()[:-1]
        self.userInputEntry.delete(0, tkinter.END)
        self.userInputEntry.insert(0, get)

    def addToHistory(self, command, result):
        try:
            file = open(histFilename, 'x')
        except FileExistsError:
            file = open(histFilename, 'a')

        writeMsg = "DATE: " + str(datetime.datetime.now())+"        "+command + " = " + str(result)
        file.write(writeMsg)
        file.write('\n')
        file.close()

        try:
            if calcHistoryMenu.window.winfo_exists():
                calcHistoryMenu.insertNewLine(writeMsg)

        except AttributeError or tkinter.TclError:
            pass

    def traverseHistoryUpDown(self, event, key):

        if key == 'up':
            self.upAndDownKeyPress += 1
        if key == 'down':
            self.upAndDownKeyPress -= 1

        if self.upAndDownKeyPress <= 0:
            self.userInputEntry.delete(0, tkinter.END)
            self.upAndDownKeyPress = 0
            return

        file = open(histFilename, 'r')
        lines = file.read().splitlines()
        if self.upAndDownKeyPress >= len(lines):
            self.upAndDownKeyPress = len(lines)
        line = lines[-1*self.upAndDownKeyPress]

        line = line[40:]  # remove everything except the initial command
        line = line.split('=', 1)[0]
        line = ''.join(line.split())

        self.userInputEntry.delete(0, tkinter.END)
        self.userInputEntry.insert(0, line)


class CalculatorButtonMenu:

    def __init__(self, frame, main):

        self.btnEquals = tkinter.Button(frame, text="=", command=lambda: calcInput.calculateUserInput())
        self.btnEquals.pack(side="left")

        self.numberLayoutPopUp = tkinter.Button(frame, text="🠕", command=lambda: self.popUpMoreFuncFrame(main))
        self.numberLayoutPopUp.pack(side="left")

        self.btnClear = tkinter.Button(frame, text="C", command=lambda: calcInput.clearUserInput())
        self.btnClear.pack(side="left")

        self.btnDot = tkinter.Button(frame, text=".", command=lambda: calcNumberAndFuncLayout.insertInUserInputEntry(self.btnDot.cget('text')))

        self.btnPlus = tkinter.Button(frame, text="+", command=lambda: calcNumberAndFuncLayout.insertInUserInputEntry(self.btnPlus.cget('text')))

        self.btnMinus = tkinter.Button(frame, text="-", command=lambda: calcNumberAndFuncLayout.insertInUserInputEntry(self.btnMinus.cget('text')))

        self.btnMultiply = tkinter.Button(frame, text="*", command=lambda: calcNumberAndFuncLayout.insertInUserInputEntry(self.btnMultiply.cget('text')))

        self.btnDivide = tkinter.Button(frame, text="/", command=lambda: calcNumberAndFuncLayout.insertInUserInputEntry(self.btnDivide.cget('text')))

        self.btnComma = tkinter.Button(frame, text=",", command=lambda: calcNumberAndFuncLayout.insertInUserInputEntry(self.btnComma.cget('text')))

        self.exitButton = tkinter.Button(frame, text="x", command=lambda: self.closeMainWindow(main))
        self.exitButton.pack(side="right")

        self.histViewButton = tkinter.Button(frame, text="History", command=lambda: self.viewCalcHistory(main))
        self.histViewButton.pack(side="right")

        self.mathLayoutPopUp = tkinter.Button(frame, text="🠕🠕", command=lambda: calcNumberAndFuncLayout.mathFunctionsPopUp(main))
        self.mathLayoutPopUp.pack(side="right")

    def closeMainWindow(self, main):
        main.destroy()

    def viewCalcHistory(self, main):
        try:
            if calcHistoryMenu.window.winfo_exists():
                calcHistoryMenu.destroyWindow()
                self.histViewButton["text"] = "History"
            else:
                calcHistoryMenu.createWindow(main)
                self.histViewButton["text"] = "Close History"

        except AttributeError:
            calcHistoryMenu.createWindow(main)
            self.histViewButton["text"] = "Close History"

    def popUpMoreFuncFrame(self, main):
        if calc.numberAndFuncLayoutFrame.winfo_ismapped():
            calc.numberAndFuncLayoutFrame.grid_remove()
            main.geometry("%sx67+0+%s" % (screenWidth, screenHeight-40))

            self.btnDot.pack_forget()
            self.btnPlus.pack_forget()
            self.btnMinus.pack_forget()
            self.btnMultiply.pack_forget()
            self.btnDivide.pack_forget()
            self.btnComma.pack_forget()

        else:
            main.geometry("%sx98+0+%s" % (screenWidth, screenHeight-40))
            calc.numberAndFuncLayoutFrame.grid()

            self.btnDot.pack(side="left")
            self.btnPlus.pack(side="left")
            self.btnMinus.pack(side="left")
            self.btnMultiply.pack(side="left")
            self.btnDivide.pack(side="left")
            self.btnComma.pack(side="left")
            self.btnClear.pack_forget()
            self.btnClear.pack(side="left")

    # def popUpMathFunctionFrame(self, main):
    #     if calc.mathFunctionsFrame.winfo_ismapped():
    #         calc.mathFunctionsFrame.grid_remove()
    #         if calc.numberAndFuncLayoutFrame.winfo_ismapped():
    #             main.geometry("%sx98+0+%s" % (screenWidth, screenHeight-40))
    #         else:
    #             main.geometry("%sx67+0+%s" % (screenWidth, screenHeight-40))
    #
    #     else:
    #         if calc.numberAndFuncLayoutFrame.winfo_ismapped():
    #             main.geometry("%sx179+0+%s" % (screenWidth, screenHeight-40))
    #         else:
    #             main.geometry("%sx148+0+%s" % (screenWidth, screenHeight-40))
    #
    #         calc.mathFunctionsFrame.grid()


class CalculatorNumberAndFunctionLayout:

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
        self.btnClearOne = tkinter.Button(frame, text="<-", command=lambda: calcInput.clearLastInputedChar())
        self.btnClearOne.pack(side="left")

        self.optFrame = tkinter.Frame(frame)

        self.optPossibilitiesValues = ["combination(n,k)", "permutation(n,k)", "factorial(x)"]
        self.optPossibilities = ttk.Combobox(self.optFrame, values=self.optPossibilitiesValues)
        self.optPossibilities.state = (['disabled'])
        self.optPossibilities.set('possibilities')
        self.optPossibilities.bind("<Key>", lambda e: "break")
        self.optPossibilities.bind("<<ComboboxSelected>>", lambda event: self.detectMathFunction(event, self.optPossibilities.get()))
        self.optPossibilities.pack(side="right")

        self.optTrigonometryValues = ["sin(x)", "cos(x)", "tan(x)", "asin(x)", "acos(x)", "atan(x)"]
        self.optTrigonometry = ttk.Combobox(self.optFrame, values=self.optTrigonometryValues)
        self.optTrigonometry.state = (['disabled'])
        self.optTrigonometry.set('trigonometry')
        self.optTrigonometry.bind("<Key>", lambda e: "break")
        self.optTrigonometry.bind("<<ComboboxSelected>>", lambda event: self.detectMathFunction(event, self.optTrigonometry.get()))
        self.optTrigonometry.pack(side="right")

        self.optAngularConversionValues = ["radians", "degrees"]
        self.optAngularConversion = ttk.Combobox(self.optFrame, values=self.optAngularConversionValues)
        self.optAngularConversion.state = (['disabled'])
        self.optAngularConversion.set('angular conversion')
        self.optAngularConversion.bind("<Key>", lambda e: "break")
        self.optAngularConversion.bind("<<ComboboxSelected>>", lambda event: self.detectMathFunction(event, self.optAngularConversion.get()))
        self.optAngularConversion.pack(side="right")

        self.optHyperbolicValues = ["sinh(x)", "cosh(x)", "tanh(x)", "asinh(x)", "acosh(x)", "atanh(x)"]
        self.optHyperbolic = ttk.Combobox(self.optFrame, values=self.optHyperbolicValues)
        self.optHyperbolic.state = (['disabled'])
        self.optHyperbolic.set('hyperbolic')
        self.optHyperbolic.bind("<Key>", lambda e: "break")
        self.optHyperbolic.bind("<<ComboboxSelected>>", lambda event: self.detectMathFunction(event, self.optHyperbolic.get()))
        self.optHyperbolic.pack(side="right")

        self.optOtherValues = ["pow(x, y)", "sqrt(x)", "log(x, base)"]
        self.optOther = ttk.Combobox(self.optFrame, values=self.optOtherValues)
        self.optOther.state = (['disabled'])
        self.optOther.set('other')
        self.optOther.bind("<Key>", lambda e: "break")
        self.optOther.bind("<<ComboboxSelected>>", lambda event: self.detectMathFunction(event, self.optOther.get()))
        self.optOther.pack(side="right")

    def insertInUserInputEntry(self, char):
        calcInput.userInputEntry.insert(tkinter.END, char)

    def detectMathFunction(self, event, selection):
        if selection in self.optPossibilitiesValues:
            self.optPossibilities.set('possibilities')
            if "comb" in selection:
                # math.comb(n,k)
                self.insertMathFunctionInEntry("math.comb()")
            elif "perm" in selection:
                # math.perm(n,k) k is optional - without k returns n factorial
                self.insertMathFunctionInEntry("math.perm()")
            elif "factorial" in selection:
                # math.factorial(x)
                self.insertMathFunctionInEntry("math.factorial()")

        elif selection in self.optTrigonometryValues:
            self.optTrigonometry.set('trigonometry')
            if selection == "sin(x)":
                # math.sin(x)
                self.insertMathFunctionInEntry("math.radians()")
                self.insertMathFunctionInEntry("math.sin()")
            elif selection == "cos(x)":
                # math.cos(x)
                self.insertMathFunctionInEntry("math.radians()")
                self.insertMathFunctionInEntry("math.cos()")
            elif selection == "tan(x)":
                # math.tan(x)
                self.insertMathFunctionInEntry("math.radians()")
                self.insertMathFunctionInEntry("math.tan()")
            elif selection == "asin(x)":
                # math.asin(x)
                self.insertMathFunctionInEntry("math.radians()")
                self.insertMathFunctionInEntry("math.asin()")
            elif selection == "acos(x)":
                # math.acos(x)
                self.insertMathFunctionInEntry("math.radians()")
                self.insertMathFunctionInEntry("math.acos()")
            elif selection == "atan(x)":
                # math.atan(x)
                self.insertMathFunctionInEntry("math.radians()")
                self.insertMathFunctionInEntry("math.atan()")

        elif selection in self.optAngularConversionValues:
            self.optAngularConversion.set("angular conversion")
            if "degrees" in selection:
                # math.degrees() - converts radians to degrees
                self.insertMathFunctionInEntry("math.degrees()")

            elif "radians" in selection:
                # opposite of math.degrees
                self.insertMathFunctionInEntry("math.radians()")

        elif selection in self.optHyperbolicValues:
            self.optHyperbolic.set('hyperbolic')
            if selection == "sinh(x)":
                # math.sinh(x)
                self.insertMathFunctionInEntry("math.sinh()")
            elif selection == "cosh(x)":
                # math.cosh(x)
                self.insertMathFunctionInEntry("math.cosh()")
            elif selection == "tanh(x)":
                # math.tanh(x)
                self.insertMathFunctionInEntry("math.tanh()")
            elif selection == "asinh(x)":
                # math.asinh(x)
                self.insertMathFunctionInEntry("math.asinh()")
            elif selection == "acosh(x)":
                # math.acosh(x)
                self.insertMathFunctionInEntry("math.acosh()")
            elif selection == "atanh(x)":
                # math.atanh(x)
                self.insertMathFunctionInEntry("math.atanh()")

        elif selection in self.optOtherValues:
            self.optOther.set("other")
            if "pow" in selection:
                # math.pow(x,y)
                self.insertMathFunctionInEntry("math.pow()")
            elif "sqrt" in selection:
                # math.sqrt(x)
                self.insertMathFunctionInEntry("math.sqrt()")
            elif "log" in selection:
                # math.log(x, base)/math.log(x)
                self.insertMathFunctionInEntry("math.log()")

    def insertMathFunctionInEntry(self, command):
        entryMsg = calcInput.userInputEntry.get()
        entryMsg = command[:-1] + entryMsg + ")"
        calcInput.userInputEntry.delete(0, tkinter.END)
        calcInput.userInputEntry.insert(0, entryMsg)

    def mathFunctionsPopUp(self, main):
        if calc.numberAndFuncLayoutFrame.winfo_ismapped():
            pass
        else:
            calc.numberAndFuncLayoutFrame.grid()
            main.geometry("%sx98+0+%s" % (screenWidth, screenHeight-40))

        if self.optFrame.winfo_ismapped():
            self.optFrame.pack_forget()
        else:
            self.optFrame.pack(side="right")




class CalculatorHistoryMenu:

    def createWindow(self, main):
        self.window = tkinter.Toplevel(main)
        self.window.config(bg="grey")
        self.window.geometry("%sx%s+0+0" % (screenWidth, screenHeight))
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)

        self.histText = tkinter.Text(self.window)
        self.histText.config(bg="grey", font=("Helvetica", 15), height=screenHeight-(screenHeight-main.winfo_screenheight()))
        self.histText.pack(side="top", anchor="center", fill=tkinter.BOTH)
        self.histText.bind("<Key>", lambda e: "break")  # so that u cant edit
        self.writeHist()

    def destroyWindow(self):
        self.window.destroy()

    def writeHist(self):
        file = open(histFilename, "r")
        lines = file.readlines()

        for line in lines:
            self.histText.insert(1.0, line)

        file.close()

    def insertNewLine(self, message):
        self.histText.insert(1.0, "%s\n" % (message))

    def onClose(self):
        self.window.destroy()
        calcButtonMenu.histViewButton["text"] = "History"


global calc, calcButtonMenu, calcInput, calcNumberAndFuncLayout, calcHistoryMenu
calc = CalculatorMain(master)
calcInput = CalculatorInput(calc.inputFrame)
calcHistoryMenu = CalculatorHistoryMenu()
calcButtonMenu = CalculatorButtonMenu(calc.buttonMenuFrame, master)
calcNumberAndFuncLayout = CalculatorNumberAndFunctionLayout(calc.numberAndFuncLayoutFrame)


keyboard.add_hotkey("ctrl+space", lambda: calc.showANDhide(master))
master.bind('<Return>', lambda event: calcInput.calculateUserInput())
calcInput.userInputEntry.bind("<Up>", lambda event, key="up": calcInput.traverseHistoryUpDown(event, key))
calcInput.userInputEntry.bind("<Down>", lambda event, key="down": calcInput.traverseHistoryUpDown(event, key))

master.mainloop()
