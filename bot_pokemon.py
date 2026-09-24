import os
from threading import Thread
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "Bot Pokémon Attivo!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

Thread(target=run).start()

import asyncio
import logging
import random
from bs4 import BeautifulSoup
from curl_cffi import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Abilita i log di controllo
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "8854409724:AAG4EI81Edk5CmAra4shf_D-wDoFmU3atrg"

CARTE = {
    "Pikachu ex Giorno": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Pikachu-ex-V2-30C149?sellerCountry=17&language=5",
    "Pikachu ex Notte": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Pikachu-ex-V2-30C150?sellerCountry=17&language=5",
    "Mewtwo ex": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Mewtwo-ex-V2-30C151?sellerCountry=17&language=5",
    "Mew ex": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Mew-ex-V2-30C152?sellerCountry=17&language=5",
    "Sylveon ex": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Sylveon-ex-V2-30C153?sellerCountry=17&language=5",
    "Gengar ex": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Gengar-ex-V2-30C154?sellerCountry=17&language=5",
    "Jirachi ex": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Jirachi-ex-V2-30C155?sellerCountry=17&language=5",
    "Mewtwo Secret": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Mewtwo-ex-V3-30C157?sellerCountry=17&language=5",
    "Mew Secret": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Mew-ex-V3-30C158?sellerCountry=17&language=5",
    "Charizard Gold": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Charizard-30CBS-4?sellerCountry=17&language=5",
    "Pikachu Gold": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Pikachu-30CBS-58?sellerCountry=17&language=5",
    "Lugia Gold": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Lugia-30CAQ-149?sellerCountry=17&language=5",
    "Gengar Gold": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Gengar-30CTM-94?sellerCountry=17&language=5",
    "Rayquaza Gold": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Rayquaza-EX-30CDRX-85?sellerCountry=17&language=5",
    "Pikachu & Zekrom Gold": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Pikachu-Zekrom-GX-30CTEU-33?sellerCountry=17&language=5",
    "Shining Celebi Gold": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Shining-Celebi-30CNDE-106?sellerCountry=17&language=5",
    "Magikarp Gold": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Magikarp-30CPAL-203?sellerCountry=17&language=5",
    "Mew RGB Blu": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Mew-V3-30CBRGB?sellerCountry=17&language=5",
    "Mew RGB Verde": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Mew-V2-30CGRGB?sellerCountry=17&language=5",
    "Mew RGB Rosso": "https://www.cardmarket.com/it/Pokemon/Products/Singles/30th-Celebration/Mew-V1-30CRRGB?sellerCountry=17&language=5"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
}

def ottieni_minimo_italiano(url: str) -> str:
    try:
        response = requests.get(url, headers=HEADERS, impersonate="chrome124", timeout=15)
        
        if response.status_code == 403:
            return "❌ Bloccato ( status 403 )"
        elif response.status_code != 200:
            return f"❌ Errore HTTP {response.status_code}"
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        prezzo_box = soup.find("dd", class_="col-6 col-xl-7 d-none d-xl-block")
        if prezzo_box:
            return prezzo_box.text.strip()
        
        prezzo_alt = soup.select_one(".price-container .h5")
        if prezzo_alt:
            return prezzo_alt.text.strip()

        return "⚠️ Prezzo non trovato"

    except Exception as e:
        return f"❌ Errore: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bot avviato! Invia **/prezzi** per controllare i minimi attuali.", parse_mode="Markdown")

async def prezzi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    attesa_msg = await update.message.reply_text("🔎 *Controllo su Cardmarket in corso... Attendi circa 30-40 secondi.*", parse_mode="Markdown")
    
    report = "🇮🇹 **Minimi attuali (ITA - Venditori Italia):**\n"
    report += "───────────────────────────\n\n"
    
    for nome, url in CARTE.items():
        prezzo = ottieni_minimo_italiano(url)
        report += f"🃏 **{nome}**\n"
        report += f"💰 Minimo: `{prezzo}`\n"
        report += f"🔗 [Vedi su Cardmarket]({url})\n\n"
        
        # Pausa casuale di circa 2 secondi per bypassare Cloudflare
        await asyncio.sleep(random.uniform(1.5, 2.5))
        
    report += "───────────────────────────"

    if len(report) > 4000:
        meta = len(report) // 2
        await attesa_msg.edit_text(report[:meta], parse_mode="Markdown", disable_web_page_preview=True)
        await update.message.reply_text(report[meta:], parse_mode="Markdown", disable_web_page_preview=True)
    else:
        await attesa_msg.edit_text(report, parse_mode="Markdown", disable_web_page_preview=True)

if __name__ == "__main__":
    # Configurazione con timeout estesi per reti instabili/aziendali
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prezzi", prezzi))
    
    print("🤖 Bot avviato e pronto!")
    app.run_polling()
