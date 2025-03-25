import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import random

load_dotenv()

EMAIL = os.getenv("EMAIL_USUARIO")
SENHA = os.getenv("EMAIL_SENHA")  # Senha de app

# Assuntos que DEVEM ser apagados (filtros ativam)
assuntos_filtrados = [
    "Promoção imperdível de tecnologia",
    "Oferta exclusiva para você",
    "Sua newsletter semanal",
    "Marketing Digital - Novidades",
    "Última chance: promoção só hoje",
    "Assine nossa newsletter agora",
    "Ganhe descontos incríveis agora",
    "Você foi selecionado para uma oferta",
    "Assinatura quase vencendo – Renove",
    "Convite especial para evento promocional"
]

# Assuntos que NÃO devem ser apagados (bons)
assuntos_limpinhos = [
    "Comprovante de pagamento da faculdade",
    "Projeto Portfólio - Bot funcionando",
    "Consulta médica confirmada",
    "Reunião de equipe marcada",
    "Atualização de sistema",
    "Código de verificação do GitHub",
    "Confirmação de matrícula",
    "Solicitação de documento recebida",
    "Horário da reunião modificado",
    "Dados do projeto atualizados"
]

def enviar_emails_teste():
    print("📤 Iniciando envio de e-mails de teste...\n")

    # Mistura os assuntos filtrados e bons
    todos_os_assuntos = assuntos_filtrados + assuntos_limpinhos
    random.shuffle(todos_os_assuntos)

    for assunto in todos_os_assuntos:
        msg = MIMEText(f"Este é um e-mail automático de teste.\nAssunto: {assunto}")
        msg["Subject"] = assunto
        msg["From"] = EMAIL
        msg["To"] = EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, SENHA)
            server.sendmail(EMAIL, EMAIL, msg.as_string())
            print(f"📩 Enviado: {assunto}")

    print("\n✅ Todos os 20 e-mails de teste foram enviados com sucesso.")

if __name__ == "__main__":
    enviar_emails_teste()
