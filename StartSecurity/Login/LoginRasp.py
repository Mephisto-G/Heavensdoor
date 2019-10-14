from tkinter import *
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import hashlib
import time
import csv
from csv import DictWriter
from pyfingerprint.pyfingerprint import PyFingerprint

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)


def mano():
    CU.destroy()

def delete_bio():
    try:
        global CU
        CU = Toplevel(screen2)
        CU.attributes('-fullscreen',True)

        global entry

        entry = StringVar()

        global entry2


        Label(CU, text="Informe o nome do usuario que deseja deletar", width=100).pack()
        entry2 = Entry(CU, textvariable = entry, font = "Arial 12")
        entry2.pack()
        Button(CU, text = "Confirmar", width = 10, height = 1, command = delete_bio2, font = "Arial 8", bg = "green").pack()
        Button(CU, text = "Voltar", width = 10, height = 1, command = mano, font = "Arial 8", bg = "red").pack()

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

def delete_bio2():
    listinha = os.listdir()
    USUARIO= entry.get()
    USER = open (USUARIO+'.FiPy', 'r')
    verify = int(USER.read())
    positionNumber = verify
    if ( f.deleteTemplate(positionNumber) == True ):
        print('Template deleted!')
        Label(CU, text = 'Biometria Deletada', font = 'Arial 12', fg = 'green').pack()
    else:
        print ("V a t o   M a n o   C u")

def search_bio():
    try:
        global root
        root = Toplevel(screen2)
        root.attributes('-fullscreen',True)
        print('Pressione o dedo no leitor.....')
        w = Label(root, text="Pressione o dedo no leitor...", width=100, font = "Arial 20")
        w.pack()
        root.update()
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Searchs template
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            print('Biometria não cadastrada')
            w['text'] = 'Biometria não cadastrada'
            root.update()
            time.sleep(3)
            root.destroy()

        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))
            w['text']= 'Biometria Autorizada'
            root.update()
            time.sleep(3)
            home()
            root.destroy()
            ##w['text'] = 'Found template at position #' + str(positionNumber), 'The accuracy score is: ' + str(accuracyScore)

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))

def mano2():
    s50.destroy()

def register_bio2():
    global s50
    s50 = Toplevel(screen2)
    s50.attributes('-fullscreen',True)

    global username
    username = StringVar()
    global username_entry1

    Label(s50, text = "Usuario ", font = "Arial 12").pack()
    username_entry1 = Entry(s50, textvariable = username, font = "Arial 12")
    username_entry1.pack()
    Button(s50, text = "Registrar", width = 10, height = 1, command = register_bio, bg = "green", font = "Arial 8").pack()
    Button(s50, text = "Voltar", width = 10, height = 1, command =  mano2, bg = "red", font = "Arial 8").pack()


def register_bio():
    try:
        global toor
        username1 = username.get()
        toor = Toplevel(screen2)
        toor.attributes('-fullscreen',True)
        print('Pressione o dedo no leitor.....')
        w = Label(toor, text="Pressione o dedo no leitor.....", width=100)
        w.pack()
        toor.update()
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Template already exists at position')
            w['text'] = 'Biometria ja cadastrada'
            toor.update()
            time.sleep(3)
            toor.destroy()

        print('Remove finger...')
        w['text'] = 'Remova o dedo'
        toor.update()
        time.sleep(2)

        print('Pressione o dedo novamente')
        w['text'] = 'Pressione o dedo novamente'
        toor.update()
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
        w['text'] = 'Biometria cadastrada com sucesso!'
        toor.update()
        time.sleep(3)
        biometria = open (username.get()+'.FiPy', 'w')
        biometria.write(str(positionNumber))
        biometria.close()
        toor.destroy()


        print('New template position #' + str(positionNumber))

    except Exception as e:
        print('Operation failed!')
        w['text'] = 'Operation Failed!'
        print('Exception message: ' + str(e))
        exit(1)

def send_email3():
    email = 'linkdragonsuporte@gmail.com'
    password = 'XnY<D42s[8~EhS".'
    send_to_email = 'Ikurosaki531@gmail.com'
    subject = 'AVISO!!' # The subject line
    body = 'Veiculo desbloqueado com segurança'

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(body, 'plain'))
    filename = "teste.jpg"
    attachment = open(filename, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
    server.sendmail(email, send_to_email, text)
    server.quit()

def send_email2():
    email = 'linkdragonsuporte@gmail.com'
    password = 'XnY<D42s[8~EhS".'
    send_to_email = 'Ikurosaki531@gmail.com'
    subject = 'RISCO DE VIDA!!!' # The subject line
    body = 'Violação de segurança, botão de panico pressionado, proprietario do veiculo corre risco de vida '

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(body, 'plain'))
    filename = "teste.jpg"
    attachment = open(filename, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
    server.sendmail(email, send_to_email, text)
    server.quit()

def send_email():

    email = 'linkdragonsuporte@gmail.com'
    password = 'XnY<D42s[8~EhS".'
    send_to_email = 'Ikurosaki531@gmail.com' # read contacts
    subject = 'AVISO!!!!!!' # The subject line
    body = 'Erro na autenticação do veiculo'

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(body, 'plain'))
    filename = "teste.jpg"
    attachment = open(filename, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
    server.sendmail(email, send_to_email, text)
    server.quit()

def change_password2():
     username_info = username_verify.get()
     password_info = password_verify.get()
     email_info = email_verify.get()

     file=open(username_info, "w")
     file.write(username_info+"\n")
     file.write(password_info+"\n")
     file.write(email_info)
     file.close()

     username_entry1.delete(0, END)
     password_entry1.delete(0, END)
     email_entry1.delete(0, END)

     Label(screen1, text = "Alteração Concluida", fg = "green" ,font = ("calibri", 11)).pack()

def voltar():
    screen2.destroy()

def voltar_registerhome():
    screen1.destroy()

def seila2():
    screen50.destroy()

def seila():
    screen40.destroy()

def voltar_login():
    screen12.destroy()

def delete3():
  screen4.destroy()

def delete4():
  screen5.destroy()

def seila3():
    screen112.destroy()

def password_not_recognised():
    global screen4
    screen4 = Toplevel(screen2)
    screen4.title("Success")
    screen4.attributes('-fullscreen',True)
    Label(screen4, text = "").pack()
    Label(screen4, text = "").pack()
    Label(screen4, text = "").pack()
    Label(screen4, text = "").pack()
    Label(screen4, text = "Senha Incorreta", font = "Arial 15").pack()
    Label(screen4, text = "").pack()
    Label(screen4, text = "").pack()
    Button(screen4, text = "OK", command =delete3, width = 10, height = 1, font = "Arial 8", bg = "red").pack()

def user_not_found():
    global screen5
    screen5 = Toplevel(screen2)
    screen5.title("Success")
    screen5.attributes('-fullscreen',True)
    Label(screen5, text = "").pack()
    Label(screen5, text = "").pack()
    Label(screen5, text = "").pack()
    Label(screen5, text = "Usuario Inexistente", font = "Arial 15").pack()
    Label(screen5, text = "").pack()
    Button(screen5, text = "OK", command =delete4, bg = "red", font = "Arial 8", width = 10, height = 1).pack()

def login_verify():

  username1 = username_verify.get()
  password1 = password_verify.get()
  username_entry1.delete(0, END)
  password_entry1.delete(0, END)

  list_of_files = os.listdir()
  if username1 in list_of_files:
    file1 = open(username1, "r")
    verify = file1.read().splitlines()
    if password1 in verify:
        home(),
    else:
        password_not_recognised(),send_email()

  else:
        user_not_found(),send_email()

def delete_user():
    username1 = username_verify.get()
    username_entry1.delete(0, END)
    list_of_files = os.listdir()
    if username1 in list_of_files:
        os.remove(username1)
        Label(screen112, text = "Usuario removido com sucesso", fg = "green" ,font = ("calibri", 11)).pack()
    else:
        user_not_found()

def delete_user_home():
    global screen112
    screen112 = Toplevel(screen2)
    screen112.attributes('-fullscreen',True)

    global username_verify
    username_verify = StringVar()
    global username_entry1

    Label(screen112, text = "").pack()
    Label(screen112, text = "").pack()
    Label(screen112, text = "").pack()
    Label(screen112, text = "Usuario ", font = "Arial 12").pack()
    username_entry1 = Entry(screen112, textvariable = username_verify, font = "Arial 12")
    username_entry1.pack()
    Label(screen112, text = "").pack()

    Button(screen112, text = "Concluir", width = 10, height = 1, command = delete_user, bg = "green", font = "Arial 8").pack()
    Button(screen112, text = "Voltar", width = 10, height = 1, command = seila3, bg = "red", font = "Arial 8").pack()

def destroi():
    screen51.destroy()

def Token2():
    senha = password_verify.get()
    password_entry1.delete(0, END)
    if senha == "123":
        home()
        screen51.destroy()
    else:
        Label(screen51, text = "Token Incorreto ", font = "Arial 12", fg = "red").pack()

def Token():
     global screen51
     screen51 = Toplevel(screen2)
     screen51.title("Success")
     screen51.attributes('-fullscreen',True)
     global password_verify
     password_verify = StringVar()
     global password_entry1
     Label(screen51, text = "", font = "Arial 12").pack()
     Label(screen51, text = "", font = "Arial 12").pack()
     Label(screen51, text = "", font = "Arial 12").pack()
     Label(screen51, text = "Senha ", font = "Arial 12").pack()
     password_entry1 = Entry(screen51, textvariable = password_verify, show = "***", font = "Arial 12")
     password_entry1.pack()
     Button(screen51, text = "Confirmar", width = 10, height = 1, command = Token2, bg = "green", font = "Arial 8").pack()
     Button(screen51, text = "Voltar", width = 10, height = 1, command = destroi, bg = "red", font = "Arial 8").pack()

def register_user():
    print("working")

    username_info = username.get()
    password_info = password.get()
    email_info = email.get()

    file=open(username_info, "w")
    file.write(username_info+"\n")
    file.write(password_info+"\n")
    file.write(email_info)
    file.close()
    
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    email_entry.delete(0, END)

    Label(screen1, text = "Registro Concluido", fg = "green" ,font = ("calibri", 11)).pack()

def change_password():
    global screen1
    screen1 = Toplevel(screen2)
    screen1.title("Start Security")
    screen1.attributes('-fullscreen',True)

    global username_verify
    global password_verify
    global email_verify

    username_verify = StringVar()
    password_verify = StringVar()
    email_verify = StringVar()

    global username_entry1
    global password_entry1
    global email_entry1

    Label(screen1, text = "Usuario ", font = "Arial 12").pack()
    username_entry1 = Entry(screen1, textvariable = username_verify, font = "Arial 12")
    username_entry1.pack()
    Label(screen1, text = "").pack()
    Label(screen1, text = "Senha ", font = "Arial 12").pack()
    password_entry1 = Entry(screen1, textvariable = password_verify, font = "Arial 12")
    password_entry1.pack()
    Label(screen1, text = "").pack()
    Label(screen1, text = "Email ", font = "Arial 12").pack()
    email_entry1 = Entry(screen1, textvariable = email_verify, font = "Arial 12")
    email_entry1.pack()
    Label(screen1, text = "").pack()

    Button(screen1, text = "Concluir", width = 10, height = 1, command = change_password2, bg = "green", font = "Arial 8").pack()
    Button(screen1, text = "Voltar", width = 10, height = 1, command = voltar_registerhome, bg = "red", font = "Arial 8").pack()

def register():
    global screen1
    screen1 = Toplevel(screen2)
    screen1.title("Start Security")
    screen1.attributes('-fullscreen',True)

    global username
    global password
    global email
    global username_entry
    global password_entry
    global email_entry

    username = StringVar()
    password = StringVar()
    email = StringVar()

    Label(screen1, text = "Por favor preencha os campos abaixo", font = "Arial 12").pack()
    Label(screen1, text = "").pack()
    Label(screen1, text = "Usuario * ", font = "Arial 12").pack()
    username_entry = Entry(screen1, textvariable = username, font = "Arial 12")
    username_entry.pack()
    Label(screen1, text = "").pack()
    Label(screen1, text = "Senha * ", font = "Arial 12").pack()
    password_entry =  Entry(screen1, textvariable = password, font = "Arial 12")
    password_entry.pack()
    Label(screen1, text = "").pack()
    Label(screen1, text = "Email * ", font = "Arial 12").pack()
    email_entry =  Entry(screen1, textvariable = email, font = "Arial 12")
    email_entry.pack()
    Label(screen1, text = "").pack()
    Button(screen1, text = "Registrar", width = 10, height = 1, command = register_user, bg = "green", font = "Arial 8").pack()
    Button(screen1, text = "Voltar", width = 10, height = 1, command = voltar_registerhome, bg = "red", font = "Arial 8").pack()

def register_home():
    global screen12
    screen12 = Toplevel(screen2)
    screen12.title("Start Security")
    screen12.attributes('-fullscreen',True)
    Label(screen12, text = "").pack()
    Label(screen12, text = "").pack()
    Label(screen12, text = "").pack()
    Button(screen12, text = "Registrar Login", width = 25, height = 3, command = register, font = "Arial 12").pack()
    Label(screen12, text = "").pack()
    Button(screen12, text = "Registrar Biometria", width = 25, height = 3, command = register_bio2, font = "Arial 12").pack()
    Label(screen12, text = "").pack()
    Label(screen12, text = "").pack()
    Button(screen12, text = "Voltar", width = 12, height = 1, command = voltar_login, bg = "red", font = "Arial 8").pack()

def Change_home():
    global screen4
    screen4 = Toplevel(screen2)
    screen4.title("Start Security")
    screen4.attributes('-fullscreen',True)
    Label(screen4, text = "").pack()
    Button(screen4, text = "Remover Biometria", width = 25, height = 3, command = delete_bio, font = "Arial 12").pack()
    Label(screen4, text = "").pack()
    Button(screen4, text = "Alterar Login", width = 25, height = 3, command = change_password, font = "Arial 12").pack()
    Label(screen4, text = "").pack()
    Button(screen4, text = "Remover Usuario", width = 25, height = 3, command = delete_user_home, font = "Arial 12").pack()
    Label(screen4, text = "").pack()
    Button(screen4, text = "Voltar", width = 12, height = 1, command = delete3, bg = "red", font = "Arial 8").pack()

def home():
    global screen40
    screen40 = Toplevel(screen2)
    screen40.title("Start Security")
    Label(screen40,text = "Bem Vindo", bg = "grey", width = 300, height = 2, font = "Arial 12").pack()
    screen40.attributes('-fullscreen',True)
    Label(screen40, text = "").pack()
    Button(screen40, text = "Registrar Usuario", width = 25, height = 3, command = register_home, font = "Arial 12" ).pack()
    Button(screen40, text = "Alterar Dados", width = 25, height = 3, command = Change_home,font = "Arial 12").pack()
    Button(screen40, text = "PANICO", width = 25, height = 3, command = send_email2, font = "Arial 12", bg = "yellow").pack()
    Label(screen40, text = "").pack()
    Button(screen40, text = "Desconectar", width = 12, height = 2, command = seila, bg = "red", font = "Arial 8").pack()

def login():
    global screen50
    screen50 = Toplevel(screen2)
    screen50.title("Start Security")
    screen50.attributes('-fullscreen',True)
    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_entry1
    global password_entry1

    Label(screen50, text = "").pack()
    Label(screen50, text = "").pack()
    Label(screen50, text = "").pack()
    Label(screen50, text = "Usuario ", font = "Arial 12").pack()
    username_entry1 = Entry(screen50, textvariable = username_verify, font = "Arial 12")
    username_entry1.pack()
    Label(screen50, text = "").pack()
    Label(screen50, text = "Senha ", font = "Arial 12").pack()
    password_entry1 = Entry(screen50, textvariable = password_verify, show = "***", font = "Arial 12")
    password_entry1.pack()
    Label(screen50, text = "").pack()
    Button(screen50, text = "Login", width = 10, height = 1, command = login_verify, bg = "green", font = "Arial 8").pack()
    Button(screen50, text = "Voltar", width = 10, height = 1, command = seila2, bg = "red", font = "Arial 8").pack()

def main_screen():
    global screen2
    screen2 = Tk()
    screen2.title("Start Security")
    screen2.attributes('-fullscreen',True)
    Label(screen2, text = "").pack()
    Button(screen2, text = "Biometria", width = 25, height = 2, command = search_bio, font = "Arial 12").pack()
    Button(screen2, text = "Login", width = 25, height = 2, command = login, font = "Arial 12").pack()
    Button(screen2, text = "Token", width = 25, height = 2, command = Token, font = "Arial 12").pack()
    Button(screen2, text = "PANICO", width = 25, height = 2, command = send_email2, font = "Arial 12", bg = "yellow").pack()
    Label(screen2, text = "").pack()
    Button(screen2, text = "Sair", width = 10, height = 1, command = voltar, font = "Arial 8", bg = "red").pack()
    screen2.mainloop()

main_screen()
