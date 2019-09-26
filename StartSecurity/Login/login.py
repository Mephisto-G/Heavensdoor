from tkinter import *
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib
import time

def search_bio():
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

    ## Tries to search the finger and calculate hash
    try:
        print('Waiting for finger...')

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
            print('No match found!')
            exit(0)
        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))

        ## OPTIONAL stuff
        ##

        ## Loads the found template to charbuffer 1
        f.loadTemplate(positionNumber, 0x01)

        ## Downloads the characteristics of template loaded in charbuffer 1
        characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

        ## Hashes characteristics of template
        print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

def delete_bio():
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

    ## Tries to delete the template of the finger
    try:
        positionNumber = input('Please enter the template position you want to delete: ')
        positionNumber = int(positionNumber)

        if ( f.deleteTemplate(positionNumber) == True ):
            print('Template deleted!')

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

def register_bio():
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

    ## Tries to enroll new finger
    try:
        print('Waiting for finger...')

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
        time.sleep(2)

        print('Waiting for same finger again...')

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
        print('New template position #' + str(positionNumber))

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)
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

    ## Tries to enroll new finger
    try:
        print('Waiting for finger...')

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
        time.sleep(2)

        print('Waiting for same finger again...')

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
        print('New template position #' + str(positionNumber))

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

def send_email():
    email = 'linkdragonsuporte@gmail.com'
    password = 'XnY<D42s[8~EhS".'
    send_to_email = 'Ikurosaki531@gmail.com'
    subject = 'AVISO!!!!!!' # The subject line
    message = 'Erro na autenticação do veiculo'

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))

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

def voltar_registerhome():
    screen1.destroy()

def voltar_login():
    screen12.destroy()

def delete3():
  screen4.destroy()

def delete4():
  screen5.destroy()

def password_not_recognised():
  global screen4
  screen4 = Toplevel(screen2)
  screen4.title("Success")
  screen4.geometry("150x100")
  Label(screen4, text = "Senha Incorreta").pack()
  Button(screen4, text = "OK", command =delete3).pack()

def user_not_found():
  global screen5
  screen5 = Toplevel(screen2)
  screen5.title("Success")
  screen5.geometry("150x100")
  Label(screen5, text = "Usuario Inexistente").pack()
  Button(screen5, text = "OK", command =delete4).pack()

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
        home()
    else:
        password_not_recognised(),send_email()

  else:
        user_not_found(),send_email()

def change_password():
    global screen1
    screen1 = Toplevel(screen2)
    screen1.title("Start Security")
    screen1.geometry("300x250")

    global username_verify
    global password_verify
    global email_verify

    username_verify = StringVar()
    password_verify = StringVar()
    email_verify = StringVar()

    global username_entry1
    global password_entry1
    global email_entry1

    Label(screen1, text = "Usuario ").pack()
    username_entry1 = Entry(screen1, textvariable = username_verify)
    username_entry1.pack()
    Label(screen1, text = "").pack()
    Label(screen1, text = "Senha ").pack()
    password_entry1 = Entry(screen1, textvariable = password_verify)
    password_entry1.pack()
    Label(screen1, text = "").pack()
    Label(screen1, text = "Email ").pack()
    email_entry1 = Entry(screen1, textvariable = email_verify)
    email_entry1.pack()
    Label(screen1, text = "").pack()

    Button(screen1, text = "Concluir", width = 10, height = 1, command = change_password2).pack()
    Button(screen1, text = "Voltar", width = 10, height = 1, command = voltar_registerhome).pack()

def register():
  global screen1
  screen1 = Toplevel(screen2)
  screen1.title("Start Security")
  screen1.geometry("300x250")

  global username
  global password
  global email
  global username_entry
  global password_entry
  global email_entry

  username = StringVar()
  password = StringVar()
  email = StringVar()

  Label(screen1, text = "Por favor preencha os campos abaixo").pack()
  Label(screen1, text = "").pack()
  Label(screen1, text = "Usuario * ").pack()
  username_entry = Entry(screen1, textvariable = username)
  username_entry.pack()
  Label(screen1, text = "Senha * ").pack()
  password_entry =  Entry(screen1, textvariable = password)
  password_entry.pack()
  Label(screen1, text = "").pack()
  Label(screen1, text = "Email * ").pack()
  email_entry =  Entry(screen1, textvariable = email)
  email_entry.pack()
  Label(screen1, text = "").pack()

  Button(screen1, text = "Registrar", width = 10, height = 1, command = register_user).pack()
  Button(screen1, text = "Voltar", width = 10, height = 1, command = voltar_registerhome).pack()

def register_home():
    global screen1
    screen1 = Toplevel(screen2)
    screen1.title("Start Security")
    screen1.geometry("300x200")
    Label(screen1, text = "").pack()
    Button(screen1, text = "Registrar Login", width = 15, height = 3, command = register).pack()
    Button(screen1, text = "Registrar Biometria", width = 15, height = 3, command = register_bio).pack()
    Button(screen1, text = "Voltar", width = 15, height = 3, command = voltar_registerhome).pack()

def Change_home():
    global screen4
    screen4 = Toplevel(screen2)
    screen4.title("Start Security")
    screen4.geometry("300x150")
    Label(screen4, text = "").pack()
    Button(screen4, text = "Remover Biometria", width = 15, height = 3, command = delete_bio).pack()
    Button(screen4, text = "Alterar Login", width = 15, height = 3, command = change_password).pack()
    Button(screen4, text = "Voltar", width = 15, height = 3, command = delete3).pack()

def home():
  global screen1
  screen1 = Toplevel(screen2)
  screen1.title("Start Security")
  Label(screen1,text = "Bem Vindo", bg = "grey", width = 300, height = 2, font = ("Calibri", 13)).pack()
  screen1.geometry("300x250")
  Label(screen1, text = "").pack()
  Button(screen1, text = "Registrar Usuario", width = 15, height = 3, command = register_home).pack()
  Button(screen1, text = "Alterar Dados", width = 15, height = 3, command = Change_home).pack()
  Button(screen1, text = "Desconectar", width = 15, height = 3, command = voltar_registerhome).pack()

def login():
    global screen12
    screen12 = Toplevel(screen2)
    screen12.title("Start Security")
    screen12.geometry("250x200")

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_entry1
    global password_entry1

    Label(screen12, text = "Usuario ").pack()
    username_entry1 = Entry(screen12, textvariable = username_verify)
    username_entry1.pack()
    Label(screen12, text = "").pack()
    Label(screen12, text = "Senha ").pack()
    password_entry1 = Entry(screen12, textvariable = password_verify, show = "***")
    password_entry1.pack()
    Label(screen12, text = "").pack()
    Button(screen12, text = "Login", width = 10, height = 1, command = login_verify).pack()
    Button(screen12, text = "Voltar", width = 10, height = 1, command = voltar_login).pack()

def main_screen():
  global screen2
  screen2 = Tk()
  screen2.title("Start Security")
  screen2.geometry("300x150")
  Label(screen2, text = "").pack()
  Button(screen2, text = "Biometria", width = 15, height = 3, command = search_bio).pack()
  Button(screen2, text = "Login", width = 15, height = 3, command = login).pack()

  screen2.mainloop()

main_screen()
