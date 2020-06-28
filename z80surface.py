from tkinter import *
import re

commandMatch = None
ram = [0] * 256 * 256
regExConst8hex = r'[0-9A-Fa-f]{2}(h|H)'    # 00H - FFH
regExConst16hex = r'[0-9A-Fa-f]{4}(h|H)'   # 0000H - FFFFH
regExConst8dec = r'[0-9]{1,3}'             # 0-255
regExConst16dec = r'[0-9]{1,5}'            # 0-65535
regExConst8 = r'((' + regExConst8hex + r')|(' + regExConst8dec + r'))'
regExConst16 = r'((' + regExConst16hex + r')|(' + regExConst16dec + r'))'

"""
Assuming this is file mymodule.py, then this string, being the
first statement in the file, will become the "mymodule" module's
docstring when the file is imported.
"""
def insert_command_value(commandValue):
   commands.insert(END,commandValue)
   commandValue=int(commandValue, 2)
   commands.insert(END,hex(commandValue))

"""
Assuming this is file mymodule.py, then this string, being the
first statement in the file, will become the "mymodule" module's
docstring when the file is imported.
"""
def get_register(register):
   registerValue = ''
   
   if register == 'A':
      registerValue = entryTextRegA.get()
   elif register == 'B':
      registerValue = entryTextRegB.get()
   elif register == 'C':
      registerValue = entryTextRegC.get()
   elif register == 'D':
      registerValue = entryTextRegD.get()
   elif register == 'E':
      registerValue = entryTextRegE.get()
   elif register == 'H':
      registerValue = entryTextRegH.get()
   elif register == 'L':
      registerValue = entryTextRegL.get()

   return registerValue

"""
Convert a hex value into an integer value
"""
def convertHexToInt(hexValue):
   intValue = -1
   
   m = re.match(r'[0-9A-Fa-f]{2,4}H', hexValue)
   if m:
      value = m.group(0)
      value = value[:len(value)-1]    
      intValue = int(value, 16)
   else:
      m = re.match(r'0x[0-9A-Fa-f]{2,4}', hexValue)
      if m:
         value = m.group(0)
         value = value[2:]    
         intValue = int(value, 16)
      else:
         m = re.match(r'[0-9]{1,3}', hexValue)
         if m:
            # 8 bit integer value
            value = m.group(0)
            intValue = int(value, 10)
            if intValue > 255:
               intValue = -1       
         else:
            # 16 bit integer value
            m = re.match(r'[0-9]{4,5}', hexValue)
            if m:
               value = m.group(0)
            intValue = int(value, 10)
            if intValue > 65536:
               intValue = -1       

   return intValue

"""
Assuming this is file mymodule.py, then this string, being the
first statement in the file, will become the "mymodule" module's
docstring when the file is imported.
"""
def get_register16_int(register0, register1):
   registerValue16 = 0
   
   if register0 == 'H' and register1 == 'L':
      registerValue0 = convertHexToInt(entryTextRegH.get())
      registerValue1 = convertHexToInt(entryTextRegL.get())
      
   registerValue0 = convertHexToInt(registerValue0)
   registerValue1 = convertHexToInt(registerValue1)

   registerValue16 = registerValue0 * 256 + registerValue1
      
   return registerValue16

"""
65Assuming this is file mymodule.py, then this string, being the
first statement in the file, will become the "mymodule" module's
docstring when the file is imported.
"""
def set_register(register,registerValue):
   commandValue = ''
   
   if register == 'A':
      entryTextRegA.set(registerValue)
      commandValue = commandValue + '111'
   elif register == 'B':
      entryTextRegB.set(registerValue)
      commandValue = commandValue + '000'
   elif register == 'C':
      entryTextRegC.set(registerValue)
      commandValue = commandValue + '001'
   elif register == 'D':
      entryTextRegD.set(registerValue)
      commandValue = commandValue + '010'
   elif register == 'E':
      entryTextRegE.set(registerValue)
      commandValue = commandValue + '011'
   elif register == 'H':
      entryTextRegH.set(registerValue)
      commandValue = commandValue + '100'
   elif register == 'L':
      entryTextRegL.set(registerValue)
      commandValue = commandValue + '101'

   return commandValue

"""
Assuming this is file mymodule.py, then this string, being the
first statement in the file, will become the "mymodule" module's
docstring when the file is imported.
"""
def parse_input(regexPattern):
   global commandMatch
   commandMatch = re.match(regexPattern, directCommand.get())
   return commandMatch

"""
Peek memory. 
"""
def peek_memory():
   peekAddressString = ''
   peekAddress = entryTextRamPeek.get()
   print(peekAddress)
   peekAddress = convertHexToInt(peekAddress)
   if peekAddress >= 0:
      for loopAddress in range(0, 16):
         if (loopAddress % 16) == 0:
            peekAddressString = hex(peekAddress) + ' :'
         peekValue = ram[peekAddress]
         peekAddressString = peekAddressString + ' ' + hex(peekValue)
         peekAddress = peekAddress + 1
      peekAddressString = peekAddressString + '\n'
      ramText.insert(INSERT, peekAddressString)
      

"""
Assuming this is file mymodule.py, then this string, being the
first statement in the file, will become the "mymodule" module's
docstring when the file is imported.
"""
def show_entry_fields():
   global commandMatch
   print(directCommand.get())
   if parse_input(r'LD [ABCDEHL]\s*,\s*[0-9A-F]{2}H'):
      ldCmd = commandMatch.group(0)
      print(ldCmd)
      ldCmd = ldCmd[3:]             # remove prefix
      print(ldCmd)
      ldCmd = re.split(",", ldCmd)
      register = ldCmd[0]
      registerValue = ldCmd[1]
      commandValue = '0b00' + set_register(register,registerValue) + '110'
      insert_command_value(commandValue)
   elif parse_input(r'LD [ABCDEHL]\s*,\s*[ABCDEHL]'):
      ldCmd = commandMatch.group(0)
      ldCmd = ldCmd[3:]             # remove prefix
      ldCmd = re.split(",", ldCmd)
      registerSrc = ldCmd[0]
      registerDest = ldCmd[1]
      registerValue = get_register(registerSrc)
      commandValue = '0b01' + set_register(registerDest,registerValue)
      insert_command_value(commandValue)  
   elif parse_input(r'LD [ABCDEHL]\s*,\s*[HL]'):
      ldCmd = commandMatch.group(0)
      ldCmd = ldCmd[3:]             # remove prefix
      ldCmd = re.split(",", ldCmd)
      address16 = get_register16_int('H', 'L')
      registerDest = ldCmd[0]
      set_register(registerDest, ram[address16])
   elif parse_input(r'LD ' + regExConst8 + r'\s*,\s*\[IX\s*+' + regExConst8 + r'\s*\]'):
      ldCmd = commandMatch.group(0)
      print(ldCmd)
      ldCmd = ldCmd[3:]             # remove prefix
      print(ldCmd)
      ldCmd = re.split(",", ldCmd)
      constValue = ldCmd[0]
      print(ldCmd)

      #ldCmd
      #parse ?
   else:
      print("Invalid command")

master = Tk()
Label(master, text="Register A").grid(row=0)
Label(master, text="Register B").grid(row=1)
Label(master, text="Register C").grid(row=2)
Label(master, text="Register D").grid(row=3)
Label(master, text="Register E").grid(row=4)
Label(master, text="Register H").grid(row=5)
Label(master, text="Register L").grid(row=6)
Label(master, text="Register IX").grid(row=7)
Label(master, text="Register IY").grid(row=8)
Label(master, text="Direct command").grid(row=9, column=1)

entryTextRegA = StringVar()
regA = Entry(master, textvariable=entryTextRegA)
entryTextRegB = StringVar()
regB = Entry(master, textvariable=entryTextRegB)
entryTextRegC = StringVar()
regC = Entry(master, textvariable=entryTextRegC)
entryTextRegD = StringVar()
regD = Entry(master, textvariable=entryTextRegD)
entryTextRegE = StringVar()
regE = Entry(master, textvariable=entryTextRegE)
entryTextRegH = StringVar()
regH = Entry(master, textvariable=entryTextRegH)
entryTextRegL = StringVar()
regL = Entry(master, textvariable=entryTextRegL)
entryTextRegIX = StringVar()
regIX = Entry(master, textvariable=entryTextRegIX)
entryTextRegIY = StringVar()
regIY = Entry(master, textvariable=entryTextRegIY)
directCommand = Entry(master)

regA.grid(row=0, column=1)
regB.grid(row=1, column=1)
regC.grid(row=2, column=1)
regD.grid(row=3, column=1)
regE.grid(row=4, column=1)
regH.grid(row=5, column=1)
regL.grid(row=6, column=1)
regIX.grid(row=7, column=1)
regIY.grid(row=8, column=1)
directCommand.grid(row=9, column=2)

# Last commands
commands = Listbox(master)
commands.grid(row=1, column = 2, rowspan=6)

# Memory
Label(master, text="Memory").grid(row=0, column = 2)
entryTextRamPeek = StringVar()
ramPeek = Entry(master, textvariable=entryTextRamPeek)
ramPeek.grid(row=0, column=3)
Button(master, text='Peek', command=peek_memory).grid(row=0, column=4, sticky=W, pady=4)

ramScroll = Scrollbar(master)
ramText = Text(master,height=6)
ramScroll.config(command=ramText.yview)
ramText.config(yscrollcommand=ramScroll.set)
ramText.grid(row=1, column=4, rowspan=6)

Button(master, text='Quit', command=master.quit).grid(row=10, column=0, sticky=W, pady=4)
Button(master, text='Show', command=show_entry_fields).grid(row=9, column=3, sticky=W, pady=4)

mainloop( )
