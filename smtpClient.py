
import sys
import socket

class smtpClient:
	def __init__(self):
		self.s = socket.socket()
	
	def smtpClient(self, serverMachine, portNumber):
		
		self.s.connect((serverMachine, int(portNumber)))
		
		recv1 = self.s.recv(1024)
		print(recv1)
		self.s.send('HELO Ben\r\n'.encode())
		recv15 = self.s.recv(1024)
		print(recv15)
		print('Connection successful')
	
	
	def senderAndReceiver(self, sender, receiver):
		mailFrom = "MAIL FROM: " + sender + "\r\n"
		self.s.send(mailFrom.encode())
		recv2 = self.s.recv(1024)
		print("After MAIL FROM command: " + recv2)

		recipient = "RCPT TO: " + receiver + "\r\n"
		self.s.send(recipient.encode())
		recv3 = self.s.recv(1024)
		print("After RCPT TO command: " + recv3)
	
	
	def messageBody(self, message, attachment):
		#print(message)
		data = "DATA\r\n"
		subject = "Subject: trash\r\n"
		version = "MIME-Version: 1.0\r\n"
		contentType = "Content-Type: multipart/mixed; boundary=\"myBoundary\"\r\n"
		boundary = "\r\n--myBoundary\r\n"
		type2 = "Content-Type: text/plain\r\n\r\n"
		type3 = "Content-Type: text/plain\r\n"
		disposition = "Content-Disposition: attachment; filename=\"attachment1.txt\"\r\n\r\n"
		if attachment == "":
			self.s.send("DATA\r\n".encode())
			self.s.send("Subject: Message WITHOUT Attachment: \r\n".encode())
			recvTest = self.s.recv(1024)
			print("Response from the DATA command" + recvTest.decode())
			self.s.send(message.encode())
		else:

			self.s.send(data.encode())
			self.s.send(subject.encode())
			self.s.send(version.encode())
			self.s.send(contentType.encode())
			self.s.send(boundary.encode())
			self.s.send(type2.encode())
			self.s.send((message + "\r\n\r\n").encode())
			self.s.send(boundary.encode())
			self.s.send(type3.encode())
			self.s.send(disposition.encode())
		
			self.s.send((attachment + "\r\n\r\n").encode())
			self.s.send((boundary + "--\r\n").encode())
		self.s.send("\r\n.\r\n".encode())
		recv4 = self.s.recv(1024)
		print("Response after sending the message body: " + recv4.decode())
	
	
	def endTheSession(self):
		self.s.send("QUIT\r\n".encode())
		recv5 = self.s.recv(1024).decode()
		print(recv5)
		self.s.close()




n = len(sys.argv)
print('Total arguments passed:', n)
print('\nName of the python program:', sys.argv[0])
for i in range(1, n):
	print('arguments passed: ', sys.argv[i])



serverName = sys.argv[1]
portNO = sys.argv[2]
senderEmail = sys.argv[3]
rcvEmail = sys.argv[4]
emailText = sys.argv[5]
fileObj = ""
if n == 7:
	fileObj = open(sys.argv[6], "r").read()


c = smtpClient()
c.smtpClient(serverName, portNO)
c.senderAndReceiver(senderEmail, rcvEmail)
c.messageBody(emailText, fileObj)
c.endTheSession()

print('This is a test')










