import os
import time
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

CARDS = {
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

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def scrape_card(name, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return f"🔹 *{name}*: N/D"
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Individua il primo prezzo nella tabella delle offerte
        price_div = soup.select_one("div.table-body div.row div.col-price")
        if price_div:
            price = price_div.get_text(strip=True)
        else:
            price = "N/D"
            
        return f"🔹 *{name}*: {price}"
    except Exception:
        return f"🔹 *{name}*: N/D"

def main():
    send_telegram("🔍 *Avvio scansione rapida Cardmarket (Italia)...*")
    
    results = []
    for name, url in CARDS.items():
        res = scrape_card(name, url)
        results.append(res)
        time.sleep(1)  # Piccola pausa rispettosa tra una richiesta e l'altra
        
    report = "📊 *REPORT PREZZI MINIMI ITALIA*\n\n" + "\n".join(results)
    send_telegram(report)

if __name__ == "__main__":
    main()
