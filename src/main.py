import sys
from automacoes import leitura_email

def menu():
    print("=== 🤖 BOT DE AUTOMAÇÃO – MENU INICIAL ===")
    print("1. Ler e-mails, aplicar filtro e salvar em planilha")
    print("0. Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        leitura_email.ler_emails_e_salvar()
    elif opcao == "0":
        print("Encerrando...")
        sys.exit()
    else:
        print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    while True:
        menu()
