from telethon import TelegramClient, events
import re
import asyncio
import dns.resolver  # Para verificar se o e-mail tem servidor ativo

# Configurações do bot
api_id = 24010179  
api_hash = "7ddc83d894b896975083f985effffe11"
bot_token = "7498558962:AAF0K2FbG1w8DlAWXvT9sPpPEZWe54LOYQ"

# Inicializando o bot
bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# Expressão regular para validar e-mail
email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

# ID do grupo
group_id = -1002222583428

# Dicionário para rastrear usuários que precisam enviar um e-mail
users_restricted = {}

def save_email(user_name, email):
    """ Salva o e-mail válido em um arquivo txt """
    with open("emails.txt", "a", encoding="utf-8") as file:
        file.write(f"{user_name} - {email}\n")

def check_mx_record(email):
    """ Verifica se o e-mail tem um servidor de e-mail ativo """
    try:
        domain = email.split('@')[1]  # Obtém o domínio (ex: gmail.com)
        mx_records = dns.resolver.resolve(domain, 'MX')  # Verifica os registros MX
        return bool(mx_records)  # Retorna True se encontrar registros
    except:
        return False  # Retorna False se o domínio não tiver e-mail

@bot.on(events.ChatAction(chats=group_id))
async def new_member(event):
    """ Quando um usuário entra, pede o e-mail apenas uma vez """
    if event.user_joined or event.user_added:
        user_id = event.user_id

        if user_id not in users_restricted:
            users_restricted[user_id] = True  # Marca o usuário como restrito
            welcome_message = (
                f"👋 Bem-vindo {event.user.first_name}! Envie um e-mail válido para liberar seu acesso ao grupo.\n\n"
                "🔹 O que você encontra no grupo?\n"
                "✅ Automação para:\n"
                "  - Facebook\n"
                "  - Instagram\n"
                "  - Telegram\n"
                "  - WhatsApp\n\n"
                "✅ Suporte técnico para resolver dúvidas e problemas\n"
                "✅ Novidades e atualizações sobre as ferramentas de automação\n"
                "✅ Dicas de engajamento para aumentar o alcance nas redes sociais\n"
                "✅ Troca de experiências com outros usuários\n\n"
                "🚀 Teste grátis! Acesse o nosso Site: https://bio.site/AutoCommenterPro."
            )
            await bot.send_message(group_id, welcome_message)

@bot.on(events.NewMessage(chats=group_id))
async def check_email(event):
    """ Verifica se o usuário enviou um e-mail válido, faz verificação real e apaga mensagens """
    user_id = event.sender_id
    message_text = event.raw_text

    if user_id in users_restricted:
        match = re.search(email_regex, message_text)
        if match:
            email = match.group()

            # Verifica se o domínio tem servidor de e-mail real
            if check_mx_record(email):
                save_email(event.sender.first_name, email)  # Salva o e-mail

                await asyncio.sleep(2)  # Aguarda 2 segundos antes de apagar
                await event.delete()  # Apaga o e-mail do grupo

                del users_restricted[user_id]  # Libera o usuário
                await bot.send_message(group_id, f"✅ Obrigado, {event.sender.first_name}! Seu acesso ao grupo foi liberado.")
            else:
                await event.delete()  # Apaga a mensagem inválida
                await bot.send_message(user_id, "❌ O e-mail enviado não parece ser real. Envie um e-mail válido para continuar.")
        else:
            await event.delete()  # Apaga a mensagem inválida
            await bot.send_message(user_id, "❌ Sua mensagem foi apagada. Envie um e-mail válido para continuar no grupo.")

print("Bot está rodando...")
bot.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
