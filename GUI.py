#!/usr/bin/python2
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import Notebook
from RSA import *

class MainFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.rsa = RSA(128)
                 
        self.createWidgets()
    
    def createWidgets(self):
		self.key_frame = KeyFrame(self)
		self.input_frame = InputFrame(self)
		self.output_frame = OutputFrame(self)
		self.state_frame = StateFrame(self)
		
		self.key_frame.generate_key_button.configure(command=self.generateKey)
		self.input_frame.string_input_frame.encrypt_button.configure(command=self.encryptString)
		self.input_frame.string_input_frame.decrypt_button.configure(command=self.decryptString)
				
		self.key_frame.pack(fill=X)
		self.input_frame.pack(fill=X)
		self.output_frame.pack(fill=X)
		self.state_frame.pack(fill=X)

    def generateKey(self):
		n, e = self.rsa.generatePublicKey()
		d = self.rsa.generatePrivateKey()
		
		self.key_frame.string_varible_n.set('%d' % n)
		self.key_frame.string_varible_e.set('%d' % e)
		self.key_frame.string_varible_d.set('%d' % d)

    def encryptString(self):
        m = self.input_frame.string_input_frame.message.get()
        
        c = self.rsa.encrypt(m)
        
        self.output_frame.displayOutput(c)
        
	def decryptString(self):
		c = self.output_frame.getOutput()
		
		print self.rsa.decrypt(c)

class KeyFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.createWidgets()

    def createWidgets(self):
		self.string_varible_n = StringVar()
		self.string_varible_e = StringVar()
		self.string_varible_d = StringVar()
		
		self.label_frame = LabelFrame(self, text='Key', padx=5, pady=5)
		self.label_frame_public_key = LabelFrame(self.label_frame, text='Public Key', padx=5, pady=5, borderwidth=0)
		self.label_frame_private_key = LabelFrame(self.label_frame, text='Private Key', padx=5, pady=5, borderwidth=0)
        
		self.generate_key_button = Button(self.label_frame, text='Generate Key')
        
		self.entry_public_key_n = Entry(self.label_frame_public_key, textvariable=self.string_varible_n)
		self.entry_public_key_e = Entry(self.label_frame_public_key, textvariable=self.string_varible_e)
		self.entry_private_key_d = Entry(self.label_frame_private_key, textvariable=self.string_varible_d);
		
		self.entry_public_key_n.pack(side=LEFT)
		self.entry_public_key_e.pack(side=LEFT)
		self.entry_private_key_d.pack(fill=X)
		
		self.label_frame_public_key.pack(fill=X)
		self.label_frame_private_key.pack(fill=X)
		self.generate_key_button.pack(side=RIGHT)
		
		self.label_frame.pack(fill=X)


class InputFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		
		self.createWidgets()
	
	def createWidgets(self):
		self.label_frame = LabelFrame(self, text="Input", padx=5, pady=5)
		
		self.notebook = Notebook(self.label_frame)
		
		self.string_input_frame = StringInputFrame(self.notebook)
		self.file_input_frame = FileInputFrame(self.notebook)
		
		self.notebook.add(self.string_input_frame, text="String")
		self.notebook.add(self.file_input_frame, text="File")

		self.label_frame.pack(fill=BOTH)
		self.notebook.pack(fill=BOTH)

class StringInputFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent, padx=5, pady=5)
		
		self.createWidgets()
	
	def createWidgets(self):
		self.message = StringVar()
		self.label_frame = LabelFrame(self, padx=5, pady=5, text="Please Input Plaintext", borderwidth=0)
		self.entry = Entry(self.label_frame, textvariable=self.message)
			
		self.encrypt_button = Button(self, text="Encrypt")
		self.decrypt_button = Button(self, text="Decrypt")

		self.label_frame.pack(fill=BOTH)
		self.entry.pack(fill=X)
		self.decrypt_button.pack(side=RIGHT)
		self.encrypt_button.pack(side=RIGHT)

class FileInputFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		
		self.createWidgets()
	
	def createWidgets(self):
		self.label_frame = LabelFrame(self, padx=5, pady=5, text="Please Input File Path", borderwidth=0)
		
		self.label_frame.pack(fill=BOTH)

class OutputFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		
		self.createWidgets()
	
	def createWidgets(self):
		self.label_frame = LabelFrame(self, padx=5, pady=5, text="Output")
		
		self.output_text = Text(self.label_frame, width=46, height=15)
		
		self.scroll = Scrollbar(self.label_frame)
		
		self.label_frame.pack(fill=BOTH)
		self.scroll.pack(side=RIGHT)
		self.output_text.pack(side=RIGHT)
	
	def displayOutput(self, output_message):
		self.output_text.delete(1.0, END)								#clear screen
		self.output_text.insert(END, output_message)
	
	def getOutput(self):
		self.output_text.get(1.0, END)
		
class StateFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		
		self.createWidgets()
	
	def createWidgets(self):
		self.frame = Frame(self, padx=5, pady=5, relief=RIDGE)
		self.state_label = Label(self, text="")
		
		self.state_label.pack(fill=X)
		self.frame.pack(fill=BOTH)
	
	def changeState(state):
		self.state_label.configure(text=state)

def main():
    root = Tk()
    root.title('RSA');                              					#set window title as "RSA"
    root.resizable(width=False, height=False);      					#do not allow resize window
    main = MainFrame(root)
    main.pack(fill=BOTH, expand=1)
    root.mainloop()

if __name__ == '__main__':
	main()
