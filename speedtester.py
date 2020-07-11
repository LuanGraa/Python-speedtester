import json
import sys
import time 
import os
import platform
import socket
import re
import csv
from datetime import datetime

 

# Testa a conversão para Int-------------------------------
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
#----------------------------------------------------------        


#Efetua a conexão com o servidor---------------------------
#OBS: Sockets não funcionam em redes da UA(Timeout Error)
def HostPing(host,port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	command = "PING {}\n".format(int(time.time()))
	s.sendall(command.encode())
	data = s.recv(1024)
	print(str(data).split("'")[1])
	data_clean = int(re.search(r'\d+', str(data)).group()) #Limpa a string data deixando apenas os milisegundos 
	s.close()
	return data_clean
#----------------------------------------------------------
def helloServer(host,port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	s.sendall('HI\n'.encode())
	data = s.recv(1024)
	print(str(data).split("'")[1])
	s.close()
	return time.time()
#----------------------------------------------------------	
def downloadFromHost(host,port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	start = time.time()
	s.connect((host, port))
	print("Downloading 10mb: \n")
	s.sendall("DOWNLOAD {}\n".format(10000000).encode())
	data = s.recv(10000000)
	end = time.time()

	print(data) #String não pode ser limpa devido aos caracteres do download
	s.close()
	return round((1024.0 * 0.001) / (end - start), 3)
#----------------------------------------------------------	
def quitSession(host,port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	print("Terminando sessão de testes...")
	s.sendall("QUIT\n".encode())
	data = s.recv(1024)
	s.close()
#----------------------------------------------------------	
def dumpCsv(lat,idHost,index,date,largBanda):
	
	with open('report.csv', 'a') as csvFile:
		writer = csv.DictWriter(csvFile, fieldnames=['contador','id','data','latência','largBanda','check'])
		writer.writerow({'contador': index, 'id' : idHost,'data': date,'latência': lat,'largBanda': largBanda,'check': 0} )
		csvFile.flush()
	csvFile.close()

#----------------------------------------------------------	


#Validar argumentos ---------------------------------------
if len(sys.argv) < 3:
    print("Correct Syntax: python3 client.py interval num [country or id]")
    sys.exit(1)
assert RepresentsInt(sys.argv[1]), "Intervalo deve ser inteiro!"
assert RepresentsInt(sys.argv[2]), "Num deve ser inteiro!"
assert int(sys.argv[1]) > 0, "Intervalo deve ser positivo!"
assert int(sys.argv[2]) > 0, "Num deve ser positivo!"
#----------------------------------------------------------


#Abrir arquivo JSON ---------------------------------------
with open('servers.json', 'r') as myfile:
    data = myfile.read()
obj = json.loads(data)
#----------------------------------------------------------
index = 1

#Caso Arg3 for um ID---------------------------------------
if(RepresentsInt(sys.argv[3])):
	for i in range(0,int(sys.argv[2])):
		for server in obj['servers']:
			if(server['id'] == int(sys.argv[3])) :
            
				HOST = server['host'].split(":")[0]
				PORT = int(server['host'].split(":")[-1])
				latfinal = 0
				print("Conectado a:",HOST,":",PORT,"\nLocalizado em:",server['country'],"\n")
				print("HI")
				helloServer(HOST,PORT)            	
				for b in range(10):
					start = time.time()
					print ('PING', int(time.time()))
					date_before = datetime.now()
					cleandata = HostPing(HOST,PORT)
					date_after = datetime.fromtimestamp(cleandata / 1e3)
					o = date_after - date_before
					o = int(o.total_seconds()*1000) #Converter microsegundos para milisegundos
					latfinal = latfinal + o
				bandWidth = downloadFromHost(HOST,PORT)
				print("\nLatência(ms): ",(int(latfinal/10)))
				print("Largura de banda: ",bandWidth)
				quitSession(HOST,PORT)
				time.sleep(int(sys.argv[1]))
				dataISO = datetime.now().isoformat()
				dumpCsv(index+1,server['id'],latfinal,dataISO,bandWidth)
				print("------------------------------------------------------------")
				break

	
#---------------------------------------------------------	


#Caso Arg3 for um País------------------------------------
else:
	for i in range(0,int(sys.argv[2])):
		print("Teste ",i+1," de",int(sys.argv[2]),">--------------------------------------------")
		for server in obj['servers']:
			if(server['country'] == sys.argv[3]):
            
				HOST = server['host'].split(":")[0]
				PORT = int(server['host'].split(":")[-1])
				latfinal = 0
				print("Conectado a:",HOST,":",PORT,"\nLocalizado em:",server['country'],"\n")
				print("HI")
				helloServer(HOST,PORT)            	
				for b in range(10):
					start = time.time()
					print ('PING', int(time.time()))
					date_before = datetime.now()
					cleandata = HostPing(HOST,PORT)
					date_after = datetime.fromtimestamp(cleandata / 1e3)
					o = date_after - date_before
					o = int(o.total_seconds()*1000) #Converter microsegundos para milisegundos
					latfinal = latfinal + o
				bandWidth = downloadFromHost(HOST,PORT)
				print("\nLatência(ms): ",(int(latfinal/10)))
				print("Largura de banda: ",bandWidth)
				quitSession(HOST,PORT)
				time.sleep(int(sys.argv[1]))
				dataISO = datetime.now().isoformat()
				dumpCsv(index+1,server['id'],latfinal,dataISO,bandWidth)
				print("------------------------------------------------------------")
				break


				
	
#---------------------------------------------------------				

			


	










