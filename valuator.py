#!/usr/bin/env python3

import tkinter, re
from valuations import Valuation
from tkinter.constants import *

VERSION = '1.0'

# a class of object that will set itself up on the GUI and add itself to the DEALS dicitonary
class GuiDeal(object):

    def __init__(self, Val, DealFrame):
        global DealCount
        self.BasicName = 'Deal' + str(DealCount+1)
        self.SpacedName = re.sub('([A-Za-z]+)([0-9]+)', '\\1 \\2', self.BasicName)
        self.listbox = tkinter.Listbox(DealFrame, height=1, width=45)
        self.listbox.grid(row=DealCount, column=0, sticky=W)
        if Val.date:
            self.comma = ', '
        else: self.comma = ''
        self.listbox.insert(END, 'Deal ' + str(DealCount+1) + ': ' + str(Val.shares) + ' of ' + str(Val.total_shares) + ' shares @ ' + Val.d_price_per_share + self.comma + Val.date)
        self.checkvar = tkinter.IntVar()
        self.checkbox = tkinter.Checkbutton(DealFrame, variable=self.checkvar)
        self.checkbox.grid(row=DealCount, column=1)
        self.checkbox.select()
        self.include = tkinter.Label(DealFrame, text='include?')
        self.include.grid(row=DealCount, column=2, sticky=W)
        self.valuation = Val # the valuation is stored here
        self.AddToDEALS() # add the object to global dictionary DEALS
        DealCount += 1

    def AddToDEALS(self): # add the object to global dictionary DEALS
        global DEALS
        DEALS[self.BasicName] = self


# Looks through the dictionary DEALS and returns a string with the
# highest number on it, i.e. 'Deal16'.
def GetLastDealName():
    keys = list(DEALS.keys())
    for i in range(len(keys)):
        keys[i] = int(re.findall('[0-9]+', keys[i])[0])
    LastDealNumber = max(keys)
    return 'Deal' + str(LastDealNumber)

# returns the key for the currently selected deal in the DEALS dicitonary
def GetTheSelectedDealName():
    for key, value in DEALS.items():
        if value.listbox.selection_includes(0):
                return key

# check:
# if both pps and amount raised are filled in in the valuation
# check to make sure that the numbers make sense
def CheckPPSAR(shares, price_per_share, amount_raised):
    return shares*price_per_share == amount_raised

def CreateTheGUI():
    global DEALS, DealCount

    # The main tkinter object, not sure quite what it is
    tk = tkinter.Tk()
    tk.title('The Valuator ' + VERSION)
    #top = tkinter.Toplevel()
    #img = tkinter.PhotoImage(file='128x128.png')
    #tkinter.Label(top, image=img).pack()
    #tk.iconwindow(top)

    # something I copied off the internet in order to have a scrolling canvas/frame thing
    def DealFrameConfigure(event):
        DealCanvas.configure(scrollregion=DealCanvas.bbox("all"), width=450, height=100)

    # this runs when you press the Add button
    def AddDeal():
        shares = SharesEntry.get()
        total_shares = TotalSharesEntry.get()
        price_per_share = PriceEntry.get()
        amount_raised = AmountEntry.get()
        date = str(DateEntry.get())
        try: shares = int(shares)
        except:
            NotANumberMessage('Shares')
            return
        try: total_shares = int(total_shares)
        except:
            NotANumberMessage('Total shares')
            return
        if price_per_share:
            try: price_per_share = float(price_per_share)
            except:
                NotANumberMessage('Price per share')
                return
        if amount_raised:
            try: amount_raised = float(amount_raised)
            except:
                NotANumberMessage('Amount raised')
                return
        if shares and total_shares and (price_per_share or amount_raised):
            if price_per_share and amount_raised and not CheckPPSAR(shares, price_per_share, amount_raised):
                RedMessage("'Price per share' and 'Amount raised' don't make sense as entered.")
                return # both pps and ar were entered but the numbers don't make sense
            else:
                if price_per_share:
                    NewVal = Valuation(shares, total_shares, date, price_per_share)
                elif amount_raised:
                    NewVal = Valuation(shares, total_shares, date, amount_raised=amount_raised)
                #print(NewVal)
                AddDealToGui(NewVal)
        elif not shares:
            NeedsEnteringMessage('Shares')
        elif not total_shares:
            NeedsEnteringMessage('Total shares')
        else:
            RedMessage("Please enter a number into either the 'Price per share' or 'Amount raised' field.")

    # this was a test funciton that added a generic deal to the list
    def OldAddDeal():
        global DealCount
        DEALS['Deal' + str(DealCount+1)] = tkinter.Listbox(DealFrame, height=1, width=45)
        DEALS['Deal' + str(DealCount+1)].grid(row=DealCount, column=0, sticky=W)
        DEALS['Deal' + str(DealCount+1)].insert(END, 'Deal ' + str(DealCount+1) + ': 123 of 123 shares @ 123')
        DEALS['Deal' + str(DealCount+1) + 'Check'] = tkinter.Checkbutton(DealFrame)
        DEALS['Deal' + str(DealCount+1) + 'Check'].grid(row=DealCount, column=1)
        DEALS['Deal' + str(DealCount+1) + 'Check'].select()
        DEALS['Deal' + str(DealCount+1) + 'Include'] = tkinter.Label(DealFrame, text='include?')
        DEALS['Deal' + str(DealCount+1) + 'Include'].grid(row=DealCount, column=2, sticky=W)
        #print('Dict len', len(DEALS), 'Added deal', 'Deal' + str(DealCount+1))
        DealCount += 1

    # this adds the valuation from AddDeal() to the gui as a deal in the list
    def AddDealToGui(NewVal):
        NewGuiDeal = GuiDeal(NewVal, DealFrame)
        BlackMessage(NewGuiDeal.SpacedName + ' added to list.')

    # this was a test function that automatically deleted that last deal in the list
    def DeleteLastDeal():
        global DEALS, DealCount
        if len(DEALS)//3:
            NameOfLastDeal = GetLastDealName()
            print('Dict len', len(DEALS), 'Deal to be removed', NameOfLastDeal)
            DEALS[NameOfLastDeal].grid_remove()
            DEALS[NameOfLastDeal + 'Check'].grid_remove()
            DEALS[NameOfLastDeal + 'Include'].grid_remove()
            del DEALS[NameOfLastDeal]
            del DEALS[NameOfLastDeal + 'Check']
            del DEALS[NameOfLastDeal + 'Include']
            DealCount -= 1
        else: print('Dict len', len(DEALS), 'No deals left')

    # this runs when you press the Delete button
    def DeleteDeal():
        DealName = GetTheSelectedDealName()
        if DealName:
            DEALS[DealName].listbox.grid_remove()
            DEALS[DealName].checkbox.grid_remove()
            DEALS[DealName].include.grid_remove()
            BlackMessage(DEALS[DealName].SpacedName + ' deleted.')
            del DEALS[DealName]

    # this runs when you press the Clear button
    def ClearDeals():
        global DealCount
        for key, value in DEALS.items():
            value.listbox.grid_remove()
            value.checkbox.grid_remove()
            value.include.grid_remove()
        DEALS.clear()
        DealCount = 0
        BlackMessage('All deals cleared.')
        #print('All deals cleared')

    # this runs when you press the Valuate button
    def ValuateDeals():
        to_valuate = []
        for key, value in DEALS.items():
            if value.checkvar.get():
                to_valuate.append(value.valuation)
        if len(to_valuate) > 1:
            merged = Valuation(deals=to_valuate)
            OutputSomething(merged)
        elif len(to_valuate) == 1:
            OutputSomething(to_valuate[0])
        else:
            RedMessage('No deals to valuate!')
            return
        #SliderToBottom(scrollbar)
        output.yview_moveto(1.0)
        BlackMessage('Valuation complete!')

    # this function adds a string to the output area
    def OutputSomething(valuation):
        output.insert(END, valuation.get_message())

    # clears the message bar across the middle of the window
    def BlankMessage():
        BlackMessage('')

    # sets the message bar to say the data in a certain field is not a number when it should be
    def NotANumberMessage(fieldname):
        RedMessage("Data in '" + fieldname + "' field not a number!")

    # sets the message bar to say that a field needs entering
    def NeedsEnteringMessage(fieldname):
        RedMessage("Please enter a number into the '" + fieldname + "' field.")

    # writes a black coloured message with a given text
    def BlackMessage(text):
        MessageText.set(text)
        MessageLabel.config(fg='black')

    def RedMessage(text):
        MessageText.set(text)
        MessageLabel.config(fg='red')

    # how many rows and columns in 'frame', the main frame of the gui
    rows = list(range(10))
    columns = list(range(10))

    # the main frame of the gui
    frame = tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
    frame.pack(fill=BOTH,expand=1)

    ####################################
    # TOP HALF WHERE DEALS ARE ENTERED #
    ####################################

    EntryFrame = tkinter.Frame(frame)
    EntryFrame.grid(row=0, column=0, columnspan=len(rows))

    # how wide the entry fields should be at the very top
    ENTRY_WIDTH = 13

    # labels and entry fields at the very top for entering a new deal
    SharesLabel = tkinter.Label(EntryFrame, text="Shares")
    SharesLabel.grid(row=0, column=0)
    SharesEntry = tkinter.Entry(EntryFrame, width=ENTRY_WIDTH)
    SharesEntry.grid(row=1, column=0)

    TotalSharesLabel = tkinter.Label(EntryFrame, text="Total shares")
    TotalSharesLabel.grid(row=0, column=1)
    TotalSharesEntry = tkinter.Entry(EntryFrame, width=ENTRY_WIDTH)
    TotalSharesEntry.grid(row=1, column=1)

    PriceLabel = tkinter.Label(EntryFrame, text="Price per share")
    PriceLabel.grid(row=0, column=2)
    PriceEntry = tkinter.Entry(EntryFrame, width=ENTRY_WIDTH)
    PriceEntry.grid(row=1, column=2)

    AmountLabel = tkinter.Label(EntryFrame, text="Amount raised")
    AmountLabel.grid(row=0, column=3)
    AmountEntry = tkinter.Entry(EntryFrame, width=ENTRY_WIDTH)
    AmountEntry.grid(row=1, column=3)

    #PercentLabel = tkinter.Label(EntryFrame, text="% taken")
    #PercentLabel.grid(row=0, column=4)
    #PercentEntry = tkinter.Entry(EntryFrame, width=ENTRY_WIDTH)
    #PercentEntry.grid(row=1, column=4)

    DateLabel = tkinter.Label(EntryFrame, text="Date")
    DateLabel.grid(row=0, column=5)
    DateEntry = tkinter.Entry(EntryFrame, width=ENTRY_WIDTH)
    DateEntry.grid(row=1, column=5)

    # Deal scrollbar
    DealScrollbar = tkinter.Scrollbar(frame)
    DealScrollbar.grid(row=rows[-7], rowspan=5, column=columns[-3], sticky=W+N+S)

    # frames can't scroll in tkinter, canvas is the only scrolling container
    DealCanvas = tkinter.Canvas(frame, relief=RIDGE, borderwidth=2)
    DealFrame = tkinter.Frame(DealCanvas)
    DealCanvas.configure(yscrollcommand=DealScrollbar.set)
    DealCanvas.grid(row=rows[-7], rowspan=5, column=0, columnspan=len(columns)-3, sticky=N+S+W+E)
    #DealCanvas.configure(scrollregion=DealCanvas.bbox("all")), width=500, height=50)
    DealCanvas.create_window((0,0), window=DealFrame, anchor='nw')
    DealFrame.bind("<Configure>", DealFrameConfigure)
    DealFrameConfigure('<Configure>')

    # All the deals get a separate listbox of height 1 and a checkbutton
    DEALS = {}
    StartWith = 0 # you can initialise a certain number of dummy deals
    DealCount = 0
    for i in range(StartWith):
        DEALS['Deal' + str(i+1)] = tkinter.Listbox(DealFrame, height=1, width=45)
        DEALS['Deal' + str(i+1)].grid(row=i, column=0, sticky=W)
        DEALS['Deal' + str(i+1)].insert(END, 'Deal ' + str(i+1) + ': 123 of 123 shares @ 123')
        DEALS['Deal' + str(i+1) + 'Check'] = tkinter.Checkbutton(DealFrame)
        DEALS['Deal' + str(i+1) + 'Check'].grid(row=i, column=1)
        DEALS['Deal' + str(i+1) + 'Check'].select()
        DEALS['Deal' + str(i+1) + 'Include'] = tkinter.Label(DealFrame, text='include?')
        DEALS['Deal' + str(i+1) + 'Include'].grid(row=i, column=2, sticky=W)
        DealCount += 1

    # Message to report any errors
    MessageText = tkinter.StringVar()
    MessageLabel = tkinter.Label(frame, textvariable=MessageText)
    MessageLabel.grid(row=rows[-2], column=0, columnspan=len(columns), sticky=W)
    BlankMessage()

    # Buttons on the right hand side
    AddButton = tkinter.Button(frame, text="Add deal", command=AddDeal)
    AddButton.grid(row=columns[-7], column=columns[-2], columnspan=2, sticky=E+W)

    DelButton = tkinter.Button(frame, text="Delete deal", command=DeleteDeal)
    DelButton.grid(row=columns[-6], column=columns[-2], columnspan=2, sticky=E+W)

    ClsButton = tkinter.Button(frame, text="Clear deals", command=ClearDeals)
    ClsButton.grid(row=columns[-5], column=columns[-2], columnspan=2, sticky=E+W)

    ValButton = tkinter.Button(frame, text="Valuate", command=ValuateDeals)
    ValButton.grid(row=columns[-4], column=columns[-2], columnspan=2, sticky=E+W)

    ExitButton = tkinter.Button(frame,text="Exit",command=tk.destroy)
    ExitButton.grid(row=columns[-3], column=columns[-2], columnspan=2, sticky=E+W)

    ####################################
    # BOTTOM HALF WHERE OUTPUT APPEARS #
    ####################################

    scrollbar = tkinter.Scrollbar(frame)
    scrollbar.grid(row=rows[-1], column=columns[-1], sticky=W+N+S)

    output = tkinter.Text(frame, wrap=WORD, height=12, yscrollcommand=scrollbar.set)
    output.grid(row=rows[-1], column=0, columnspan=len(columns)-1)

    #Old stuff I got to appear initially in the output:
    #output.insert(END, '123 shares @ 123 per share\n')
    #output.insert(END, '123 shares @ 123 per share\n')
    #output.insert(END, 'Total shares bought: 123\n')
    #output.insert(END, '123% of 123 total shares: 123\n')
    #output.insert(END, 'Amount raised: 123\n')
    #output.insert(END, 'Pre-money: 123\n')
    #output.insert(END, 'Post-money: 123\n')
    #output.insert(END, 'Introibo ad altare Dei.\n')
    #output.insert(END, 'Ad Deum qui laetificavit juventutem meam.\n')
    #for i in range(30):
    #    output.insert(END, str(i) + '\n')

    scrollbar.config(command=output.yview)
    DealScrollbar.config(command=DealCanvas.yview)

    tk.mainloop()

if __name__ == '__main__':
    CreateTheGUI()


