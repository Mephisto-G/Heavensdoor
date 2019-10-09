import time
from pyfingerprint.pyfingerprint import PyFingerprint

from tkinter import *

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
  
class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()
  
        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()
  
        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()
  
        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()
  
        self.titulo = Label(self.primeiroContainer, text="Dados do usuário")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()
  
        self.nomeLabel = Label(self.segundoContainer,text="Nome", font=self.fontePadrao)
        self.nomeLabel.pack(side=LEFT)
  
        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 30
        self.nome["font"] = self.fontePadrao
        self.nome.pack(side=LEFT)
  
        self.senhaLabel = Label(self.terceiroContainer, text="Senha", font=self.fontePadrao)
        self.senhaLabel.pack(side=LEFT)
  
        self.senha = Entry(self.terceiroContainer)
        self.senha["width"] = 30
        self.senha["font"] = self.fontePadrao
        self.senha["show"] = "*"
        self.senha.pack(side=LEFT)
  
        self.autenticar = Button(self.quartoContainer)
        self.autenticar["text"] = "Autenticar"
        self.autenticar["font"] = ("Calibri", "8")
        self.autenticar["width"] = 12
        self.autenticar["command"] = self.verificaSenha
        self.autenticar.pack()
  
        self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()
  
    #Método verificar senha
    def verificaSenha(self):
        usuario = self.nome.get()
        senha = self.senha.get()
        if usuario == "Gabriel" and senha == "123":
            self.mensagem["text"] = "Autenticado"
            try:
                root = Tk()
                root.geometry("400x400")
                print('Waiting for finger...')
                w = Label(root, text="'Waiting for finger...", width=100)
                w.pack()
                root.update()
                ## Wait that finger is read
                while ( f.readImage() == False ):
                    pass

                ## Converts read image to characteristics and stores it in charbuffer 1
                f.convertImage(0x01)

                ## Checks if finger is already enrolled
                result = f.searchTemplate()
                positionNumber = result[0]

                if ( positionNumber >= 0 ):
                    print('Template already exists at position #' + str(positionNumber))
                    exit(0)

                print('Remove finger...')
                w['text'] = 'Remove finger'
                root.update()
                time.sleep(2)

                print('Waiting for same finger again...')
                w['text'] = 'Waiting for same finger again...'
                root.update()
                ## Wait that finger is read again
                while ( f.readImage() == False ):
                    pass

                ## Converts read image to characteristics and stores it in charbuffer 2
                f.convertImage(0x02)

                ## Compares the charbuffers
                if ( f.compareCharacteristics() == 0 ):
                    raise Exception('Fingers do not match')

                ## Creates a template
                f.createTemplate()

                ## Saves template at new position number
                positionNumber = f.storeTemplate()
                print('Finger enrolled successfully!')
                w['text'] = 'Finger enrolled successfully!'
                root.update()
                print('New template position #' + str(positionNumber))

            except Exception as e:
                print('Operation failed!')
                w['text'] = 'Operation Failed!'
                print('Exception message: ' + str(e))
                exit(1)


        else:
            self.mensagem["text"] = "Erro na autenticação"
  
  
root = Tk()
Application(root)
root.mainloop()