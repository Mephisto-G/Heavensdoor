from tkinter import *
import time
import hashlib
import os
from pyfingerprint.pyfingerprint import PyFingerprint
from login2 import *

def Buscar_Digital():
	try:
		f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
		if( f.verifyPassword() == False ):
			raise ValueError('The given fingerprint sensor password is wrong!')
	except Exception as e:
		user_not_found()
		exit(1)
	try:
		print('Waiting for finger...')

		while ( f.readImage() == False ):
			pass
		f.convertImage(0x01)

		result = f.searchTemplate()

		positionNumber = result[0]
		accuracyScore = result[1]
		if ( positionNumber == -1 ):
			user_not_found()
			exit(0)
		else:
			Finger=positionNumber
			Lista= os.listdir()
		if Finger in Lista:
			Ver=open(Finger+".fin", 'r')
			usr=Ver.read().splitlines()
	except Exception as e:
		exit(1)

def Adicionar_Digital():
	try:
		f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
		if ( f.verifyPassword() == False ):
			raise ValueError('The given fingerprint sensor password is wrong!')
	except Exception as e:
			exit(1)
	try:
		while(f.readImage() == False):
			pass
		f.convertImage(0x01)
		result=f.searchTemplate()
		positionNumber= result[0]
		if (positionNumbe >= 0):
			Usr_ja_cad()
			exit(0)
		#Adicionar algo para fazer o user remover o dedo
			time.sleep(2)
			while(f.readImage() == False):
				pass
		f.convertImage(0x02)
		if (f.compareCharacteristics() == 0 ):
			raise Exception("Fingers not Match")
			Dedos_nao_batem()
		f.createTemplate()
		positionNumber = f.storeTemplate()
		USR=open(positionNumber+".fin")
		USR.write(usr)
		USR.close
		Cadastrado()
		main_screen()
	except Exception as e:
		exit(1)

def Remover_Digital():
	try:
		f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
	
		if ( f.verifyPassword() == False ):
			raise ValueError('The given fingerprint sensor password is wrong!')
	except Exception as e:
		exit(1)
	try:
		positionNumber = input('Please enter the template position you want to delete: ')
		positionNumber = int(positionNumber)
		if ( f.deleteTemplate(positionNumber) == True ):
			print('Template deleted!')
	except Exception as e:
		print('Operation failed!')
		print('Exception message: ' + str(e))
		exit(1)

		
