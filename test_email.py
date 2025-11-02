import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

sender_email = os.environ.get('EMAIL_USER')
sender_password = os.environ.get('EMAIL_PASSWORD')
receiver_email = os.environ.get('RECEIVER_EMAIL')

print(f"Email do remetente: {sender_email}")
print(f"Email do destinatário: {receiver_email}")

if not all([sender_email, sender_password, receiver_email]):
    print("❌ Erro: Credenciais não configuradas!")
    exit(1)

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "✅ TESTE: Sistema de Email Funcionando"

body = "Este é um email de teste do seu sistema de monitorização do Hotel Lusitania. Se recebeu isto, o sistema está a enviar emails corretamente!"

message.attach(MIMEText(body, "plain"))

try:
    print("A ligar a Gmail...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(message)
        print("✅ Email de teste enviado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao enviar email: {e}")
