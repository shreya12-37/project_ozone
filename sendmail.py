import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
   

def sendMail(reciever_address, contactDetails=None):
	fromaddr = "famegamecorp2020@gmail.com"
	toaddr = reciever_address
	try:   
		msg = MIMEMultipart() 
			  
		msg['From'] = fromaddr 
		msg['To'] = toaddr
		msg['Subject'] = "Successfully registered for contest"
		body = "Query from "+contactDetails["fname"]+"\n "+contactDetails['email'] +"\n"+"You have been successfully registered for the contest."
		msg.attach(MIMEText(body, 'plain')) 
		s = smtplib.SMTP('smtp.gmail.com', 587) 
		s.starttls()
		s.login(fromaddr, "yowxmvaacpolqakj")
		text = msg.as_string() 
		s.sendmail(fromaddr, toaddr, text) 
		s.quit()
		print("mail sent successfully")
	except Exception as e:
		print(e)
		return 400, "mail not send"

	print("mail sent")		
	return 200, "mail sent"

if __name__ == "__main__":
	sendMail('famegamecorp2020@gmail.com')
