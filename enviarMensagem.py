import os
import requests
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# 🔹 Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔹 Configurações da Z-API
ZAPI_INSTANCE = os.getenv("ZAPI_INSTANCE")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE}/token/{ZAPI_TOKEN}/send-messages"

def buscar_contatos():
    """Busca até 3 contatos no Supabase."""
    response = supabase.table("contatos").select("nome, telefone").limit(3).execute()
    return response.data

def enviar_mensagem(nome, telefone):
    """Envia mensagem personalizada via Z-API."""
    mensagem = f"Olá {nome}, tudo bem com você?"
    payload = {
        "phone": telefone,
        "message": mensagem
    }
    r = requests.post(ZAPI_URL, json=payload)
    if r.status_code == 200:
        print(f"✅ Mensagem enviada para {nome} ({telefone})")
    else:
        print(f"❌ Erro ao enviar para {nome} ({telefone}): {r.text}")

if __name__ == "__main__":
    contatos = buscar_contatos()
    if not contatos:
        print("Nenhum contato encontrado no Supabase.")
    else:
        for contato in contatos:
            enviar_mensagem(contato["nome"], contato["telefone"])
