import os
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env (en local)
load_dotenv()

def enviar_correo_con_adjunto():
    # 1. Configuración del servidor y credenciales
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    remitente = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")  # Contraseña de aplicación
    
    # LISTA DE DESTINATARIOS
    destinatarios = [
        "clozanoguadarrama@gmail.com",
        "juantobiasdl7@gmail.com"
        #"otro_correo2@ejemplo.com"
    ]
    
    # 2. Crear el mensaje estructurado
    msg = MIMEMultipart()
    msg['From'] = remitente
    # Para el encabezado del correo se unen con coma
    msg['To'] = ", ".join(destinatarios)
    msg['Subject'] = "Asunto del correo con adjunto"
    
    # Cuerpo del correo
    cuerpo = "Hola,\n\nTe adjunto el archivo solicitado en este correo enviado desde Python.\n\nSaludos."
    msg.attach(MIMEText(cuerpo, 'plain'))
    
    # 3. Ruta de los archivos que quieres adjuntar
    archivos_adjuntos = [
        "pdf-files/top-50-mexico-daily-by-deezer(2026-07-03-00-03+0000).pdf",
        "csv-files/top-50-mexico-daily-by-deezer(2026-07-03-00-03+0000).csv"
    ]
    
    # CICLO FOR: Procesa y añade cada archivo de la lista
    for ruta_adjunto in archivos_adjuntos:
        if os.path.exists(ruta_adjunto):
            nombre_archivo = os.path.basename(ruta_adjunto)
            print(f"Preparando adjunto: {nombre_archivo}...")
            
            # Abrir el archivo en modo binario
            with open(ruta_adjunto, "rb") as adjunto:
                parte = MIMEBase("application", "octet-stream")
                parte.set_payload(adjunto.read())
                
            # Codificar en base64 para envío seguro
            encoders.encode_base64(parte)
            
            # Añadir las cabeceras del adjunto
            parte.add_header(
                "Content-Disposition",
                f"attachment; filename= {nombre_archivo}",
            )
            
            # Acoplar el archivo al mensaje principal
            msg.attach(parte)
        else:
            print(f"Advertencia: El archivo en '{ruta_adjunto}' no existe. Se omitirá este adjunto.")

    # 4. Conexión al servidor y envío
    try:
        print("Conectando al servidor SMTP...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() 
        
        # Iniciar sesión
        server.login(remitente, password)
        
        # Enviar (pasamos la lista 'destinatarios' directamente)
        print("Enviando correo a la lista de destinatarios...")
        server.sendmail(remitente, destinatarios, msg.as_string())
        
        print("¡Correo enviado con éxito a todos los destinatarios!")
        
    except Exception as e:
        print(f"Hubo un error al enviar el correo: {e}")
        
    finally:
        # Cerrar la conexión de forma segura
        server.quit()

# Ejecutar la función
if __name__ == "__main__":
    enviar_correo_con_adjunto()