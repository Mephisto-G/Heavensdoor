import sys
import os
from tkinter import *
us3r=[]
class CriarUsuario:
	def __init__(self, master=None):
		#Quadrinho
		self.frame_master= Frame(master)
		self.frame_master["pady"] = 10
		self.frame_master.configure(bg='white')
		self.frame_master.pack(fill='both', expand=True)
		
		self.frame_1 = Frame(self.frame_master)
		self.frame_1.configure(bg='sky blue')
		self.frame_1.pack(fill='both', expand=True)
		
		#Entradas
		butt_1 = Button(self.frame_1)
		butt_1['text'] = 'nome'
		butt_1['font'] = ('Arial', '16', 'bold')
		butt_1["command"] = self.btao
		butt_1.configure(bg='sky blue',
								activebackground='sky blue')
		butt_1.pack(side='left', fill='both', expand=True)
   
		
		self.Usuario= Entry(self.frame_master)
		self.Usuario.config(relief=RIDGE)
		self.Usuario.pack()
		self.Usuario['text'] = "Nome de Usuário"
		self.Usuario['font'] = ('Arial', '12', 'bold')
		
		
		
		self.Senha= Entry(self.frame_master)
		self.Senha.config(relief=RIDGE)
		self.Senha.pack()
		self.Senha['text'] = "Senha"
		self.Senha['font'] = ('Arial', '12', 'bold')
	def btao(self):
		us3r.append(self.Usuario)
		print (us3r)
		
		
if __name__ == '__main__':
	teclado = Tk()
	teclado.title('Configurações')
	teclado.geometry('720x480')
	#teclado.overrideredirect(True)
	teclado.resizable(False, False)
	CriarUsuario(teclado)
	teclado.mainloop()
