import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def check_hotel_availability():
    # URL do Booking.com para o Hotel Lusitania
    # Formato: checkin=2025-12-30, checkout=2026-01-01
    url = "https://www.booking.com/hotel/pt/lusitania.html?checkin=2025-12-30&checkout=2026-01-01&group_adults=2&no_rooms=1"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        page_content = response.text
        
        # Verificar se há quartos disponíveis
        # Booking.com mostra "Não há disponibilidade" quando esgotado
        if "Não há disponibilidade" in page_content or "No availability" in page_content:
            print(f"[{datetime.now()}] Hotel ainda esgotado")
            return False
        else:
            print(f"[{datetime.now()}] DISPONIBILIDADE ENCONTRADA!")
            send_notification()
            return True
            
    except Exception as e:
        print(f"Erro ao verificar: {e}")
        return False

def send_notification():
    sender_email = os.environ.get('EMAIL_USER')
    sender_password = os.environ.get('EMAIL_PASSWORD')
    receiver_email = os.environ.get('RECEIVER_EMAIL')
    
    if not all([sender_email, sender_password, receiver_email]):
        print("Credenciais de email não configuradas")
        return
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "ALERTA: Hotel Lusitania Disponível!"
    
    body = """
    Boa notícia! O Hotel Lusitania tem disponibilidade para 30 Dez - 01 Jan!
    
    Aceda já ao Booking.com para reservar:
    https://www.booking.com/hotel/pt/lusitania.html?checkin=2025-12-30&checkout=2026-01-01&group_adults=2&no_rooms=1
    """
    
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
            print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")

if __name__ == "__main__":
    check_hotel_availability()
