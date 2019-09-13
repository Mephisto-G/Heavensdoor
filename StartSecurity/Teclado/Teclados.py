import sys
import os
from tkinter import *
import math 
import json
import tecladoqwerty 

class CriarUsuario:
	def __init__(self, master=None):
		#Quadrinho
		
		self.frame_master= Frame(master)
		self.frame_master["pady"] = 5
		self.frame_master.configure(bg='white')
		self.frame_master.pack(fill='both', expand=True)
		
		osk = keyboard_mixin()
		osk.show()
		
		#GetUser
		
		form = Frame(self.frame_master)
		left = Frame(form)
		rite = Frame(form)
		form.pack(fill=X) 
		left.pack(side=LEFT)
		rite.pack(side=RIGHT, expand=YES, fill=X)
		
		lab = Label(left, width=7, text="Usuario:")
		use = Label(left, width=7, text="aaa")
		ent = Entry(rite)
		lab.pack(side=TOP)
		ent.pack(side=TOP, fill=X)
		var = StringVar()
		ent.config(textvariable=var)
		
			

		#GetPass
		
		lab2 = Label(left, width=7, text="Senha:")
		use2 = Label(left, width=7, text="aaa")
		ent2 = Entry(rite)
		lab2.pack(side=TOP)
		ent2.pack(side=TOP, fill=X)
		var2 = StringVar()
		ent2.config(textvariable=var2)
		
		self.frame_1 = Frame(self.frame_master)
		self.frame_1.configure(bg='sky blue')
		self.frame_1.pack(fill='both', expand=True)
		
		#Entradas
		butt_1 = Button(self.frame_1)
		butt_1['text'] = "We're done"
		butt_1['font'] = ('Arial', '16', 'bold')
		butt_1["command"] = self.btao
		butt_1.configure(bg='sky blue',
								activebackground='black')
		butt_1.pack(side='left', fill='both', expand=True)
		
	def btao(self):
		print("We're in the endgame Now")
		with open('teste.json', 'r') as arquivo:
			data= json.loads(arquivo)
		print(data)

#print(var.get())

if __name__ == '__main__':
	teclado = Tk()
	teclado.title('Insira Conta')
	teclado.geometry('1080x720')
	#teclado.overrideredirect(True)
	teclado.resizable(False, False)
	CriarUsuario(teclado)
	teclado.mainloop()

