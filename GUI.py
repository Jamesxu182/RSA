#!/usr/bin/python2
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import Notebook
from RSA import *
from tkFileDialog import askopenfilename
import os.path

class MainFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		
		self.rsa = RSA(128)
		
		self.createWidgets()

	def createWidgets(self):
		self.key_frame = KeyFrame(self)
		self.input_frame = InputFrame(self)
		self.output_frame = OutputFrame(self)
		self.state_frame = StateFrame(self)
		
		self.key_frame.pack(fill=X)
		self.input_frame.pack(fill=X)
		self.output_frame.pack(fill=X)
		self.state_frame.pack(fill=X)

class KeyFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		
		self.parent = parent
		
		self.createWidgets()

	def createWidgets(self):
		self.string_varible_n = StringVar()
		self.string_varible_e = StringVar()
		self.string_varible_d = StringVar()
		
		self.label_frame = LabelFrame(self, text='Key', padx=5, pady=5)
		self.label_frame_public_key = LabelFrame(self.label_frame, text='Public Key', padx=5, pady=5, borderwidth=0)
		self.label_frame_private_key = LabelFrame(self.label_frame, text='Private Key', padx=5, pady=5, borderwidth=0)
		
		self.generate_key_button = Button(self.label_frame, text='Generate Key', command=self.generateKey)
		
		
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
	def generateKey(self):
		n, e = self.parent.rsa.generatePublicKey()
		d = self.parent.rsa.generatePrivateKey()
		
		self.string_varible_n.set('%d' % n)
		self.string_varible_e.set('%d' % e)
		self.string_varible_d.set('%d' % d)

class InputFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		
		self.createWidgets()
		
	def createWidgets(self):
		self.label_frame = LabelFrame(self, text="Input", padx=5, pady=5)
		
		self.notebook = Notebook(self.label_frame)
		
		self.string_input_frame = StringInputFrame(self)
		self.file_input_frame = FileInputFrame(self)
		
		self.notebook.add(self.string_input_frame, text="String")
		self.notebook.add(self.file_input_frame, text="File")
		
		self.label_frame.pack(fill=BOTH)
		self.notebook.pack(fill=BOTH)

class StringInputFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent, padx=5, pady=5)
		self.parent = parent
		
		self.createWidgets()
	
	def createWidgets(self):
		self.message = StringVar()
		self.label_frame = LabelFrame(self, padx=5, pady=5, text="Please Input Plaintext", borderwidth=0)
		self.entry = Entry(self.label_frame, textvariable=self.message)
		
		self.encrypt_button = Button(self, text="Encrypt", command=self.encryptString)
		self.decrypt_button = Button(self, text="Decrypt", command=self.decryptString)
		
		self.label_frame.pack(fill=BOTH)
		self.entry.pack(fill=X)
		self.decrypt_button.pack(side=RIGHT)
		self.encrypt_button.pack(side=RIGHT)


	def encryptString(self):
		m = self.message.get()
		
		c = self.parent.parent.rsa.encrypt(m)
		
		self.parent.parent.output_frame.displayOutput(c)
		
	def decryptString(self):
		c = self.parent.parent.output_frame.getOutput()
		
		m = self.parent.parent.rsa.decrypt(c)
		
		self.message.set(m);
		
class FileInputFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		
		self.createWidgets()
	
	def createWidgets(self):
		self.file_path = StringVar()
		
		self.label_frame = LabelFrame(self, padx=5, pady=5, text="Please Input File Path", borderwidth=0)
		
		self.entry_file_path = Entry(self.label_frame, textvariable=self.file_path)
		
		self.button_browse = Button(self.label_frame, text="Browse", command=self.openFileChooser)
		self.button_encrypt = Button(self, text='Encrypt', command=self.encryptFile)
		self.button_decrypt = Button(self, text='Decrypt', command=self.decryptFile)
		
		self.label_frame.pack(fill=BOTH)
		
		self.button_browse.pack(side=RIGHT)
		self.entry_file_path.pack(side=LEFT, expand=1)
		self.button_decrypt.pack(side=RIGHT)
		self.button_encrypt.pack(side=RIGHT)
	
	def openFileChooser(self):
		self.file_opt = options = {}
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
		options['initialdir'] = '~/'
		options['title'] = 'Choose file'
		
		filename = askopenfilename(**self.file_opt)
		
		self.file_path.set(filename)
	
	def encryptFile(self):
		path_name = self.file_path.get()
		
		if os.path.isfile(path_name):
			
			f = open(path_name, 'r')
			
			new_f = open(path_name + '.encrypted', 'w')
			
			content = f.read()
			
			cipher = self.parent.parent.rsa.encrypt(content)
			
			self.parent.parent.output_frame.displayOutput(cipher)
			
			new_f.write(cipher)
			
			f.close()
			new_f.close()
			
	def decryptFile(self):
		path_name = self.file_path.get()
		
		if os.path.isfile(path_name):
		
			f = open(path_name, 'r')
			
			cipher = f.read()
			
			content = self.parent.parent.rsa.decrypt(cipher)
			
			self.parent.parent.output_frame.displayOutput(content)
			
			f.close()

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
		return self.output_text.get(1.0, END)
		
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
