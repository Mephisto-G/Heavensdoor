import json
import requests
#abrir arquivo
with open('Arquivo.json') as f:    
    data = json.load(f)


Senha= input("Bem vindo " + (data.get('User'))+" Alterar a senha\n >>> ") 
if Senha == (data.get('Secret')):
	#(data.get("secret")) <-- isso chama a senha, é uma referência pro local q ela fica armazenada no arquivo 
	#é o dado que precisamos alterar.
	X= input ("Nova Senha >>> ")
	print (data.get('Secret'))



