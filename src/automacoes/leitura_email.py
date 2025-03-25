import imaplib
import email
from email.header import decode_header
import pandas as pd
from datetime import datetime
import os
import json
from dotenv import load_dotenv

load_dotenv()

def ler_emails_e_salvar():
    usuario = os.getenv("EMAIL_USUARIO")
    senha = os.getenv("EMAIL_SENHA")

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(usuario, senha)
    mail.select("inbox")

    # Carregar filtros
    with open("filtros.json", "r", encoding="utf-8") as f:
        filtros = json.load(f)
    palavras_chave = filtros.get("palavras_chave_para_excluir", [])

    # Buscar todos os e-mails
    status, mensagens = mail.search(None, "ALL")
    mensagens = mensagens[0].split()

    dados = []
    log_exclusao = []

    for num in mensagens[-50:]:
        status, msg_data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        assunto, encoding = decode_header(msg["Subject"])[0]
        remetente = msg.get("From")

        if isinstance(assunto, bytes):
            assunto = assunto.decode(encoding or "utf-8", errors="ignore")

        # Verificar se o assunto contém alguma palavra-chave
        palavra_detectada = next(
            (palavra for palavra in palavras_chave if palavra.lower() in assunto.lower()), None
        )

        if palavra_detectada:
            mail.store(num, '+FLAGS', '\\Deleted')
            log_exclusao.append({
                "DataHora": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Assunto": assunto,
                "Remetente": remetente,
                "PalavraDetectada": palavra_detectada
            })
            print(f"🗑️ Apagado: '{assunto}' | Palavra-chave: {palavra_detectada}")
        else:
            dados.append({
                "Data": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Assunto": assunto,
                "Remetente": remetente
            })

    # Executar a exclusão real
    mail.expunge()

    # ✅ Salvar os e-mails "bons" em planilha (se houver)
    if dados:
        os.makedirs("output", exist_ok=True)
        nome_arquivo = datetime.now().strftime("output/emails_bons_%Y-%m-%d_%H-%M.xlsx")
        df = pd.DataFrame(dados)
        df.to_excel(nome_arquivo, index=False)
        print(f"📁 Planilha gerada com e-mails bons: {nome_arquivo}")
    else:
        print("⚠️ Nenhum e-mail 'bom' para salvar em planilha.")

    # ✅ Salvar o log de e-mails excluídos (se houver)
    if log_exclusao:
        os.makedirs("logs", exist_ok=True)
        log_df = pd.DataFrame(log_exclusao)
        log_path = "logs/emails_excluidos.csv"
        log_df.to_csv(
            log_path,
            index=False,
            mode="a",
            encoding="utf-8-sig",
            header=not os.path.exists(log_path)
        )
        print("📁 Log de exclusão salvo em logs/emails_excluidos.csv")
    else:
        print("✅ Nenhum e-mail foi excluído nesta execução.")

    mail.logout()
    print("✔️ Leitura finalizada e e-mails irrelevantes removidos.")
