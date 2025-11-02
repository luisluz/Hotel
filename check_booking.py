from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time

def check_hotel_availability():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        url = "https://www.booking.com/hotel/pt/lusitania.html?checkin=2025-12-30&checkout=2026-01-01&group_adults=2&no_rooms=1"
        print(f"[{datetime.now()}] A aceder ao Booking.com...")
        driver.get(url)
        
        # Espera até 30 segundos pelo conteúdo carregar
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "hprt-card"))
        )
        
        time.sleep(2)
        page_source = driver.page_source
        
        # Verificações de disponibilidade
        if "Não há disponibilidade" in page_source or "No availability" in page_source or "Sem disponibilidade" in page_source:
            print(f"[{datetime.now()}] Hotel ainda esgotado")
            return False
        
        # Verifica se encontrou quartos
        if "hprt-card" in page_source and "sold out" not in page_source.lower():
            print(f"[{datetime.now()}] DISPONIBILIDADE ENCONTRADA!")
            send_notification()
            return True
        else:
            print(f"[{datetime.now()}] Hotel esgotado ou não conseguiu carregar")
            return False
            
    except Exception as e:
        print(f"Erro ao verificar: {e}")
        return False
    finally:
        driver.quit()

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
    message["Subject"] = "🚨 ALERTA: Hotel Lusitania Disponível!"
    
    body = """
    🎉 Boa notícia! O Hotel Lusitania tem disponibilidade para 30 Dez - 01 Jan!
    
    Aceda JÁ ao Booking.com para reservar:
    https://www.booking.com/hotel/pt/lusitania.html?checkin=2025-12-30&checkout=2026-01-01&group_adults=2&no_rooms=1
    
    Atenção: esta é uma oportunidade rara, reserve rapidamente antes que se esgote novamente!
    """
    
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
            print("Email de alerta enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")

if __name__ == "__main__":
    check_hotel_availability()
