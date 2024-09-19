import asyncio
import requests
from telegram import Bot
from datetime import datetime

api_key = "YOUR API-KEY"
TOKEN = "YOUR TOKEN"
CHAT_ID = "YOUR CHAT-ID"
sehir = "ŞEHİR"
bot = Bot(token=TOKEN)

semsiye_mesaj = "Bugün hava yağmurlu, yanına şemsiye almayı unutma. ☔️"
clear_mesaj = "Bugün hava açık ☀️"
clods_mesaj = "Bugün hava kapalı ve bulutlu, hava serin olabilir ☁️"
snow_mesaj = "Bugün hava karlı, kalın giyin ❄️"
drizle_mesaj = "Bugün hafif çiseliyor, şemsiyeni yanına alabilirsin 🌧️"
thunderstorm_mesaj = "Bugün hava fırtınalı dışarı çıkma ⛈️"
sicaklik_mesaj = ""

async def main():
    while True:
        simdi = datetime.now()
        saat = simdi.strftime("%H:%M:%S")
        
        if "08:00:00" <= saat <= "22:00:00":
            url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                weather = data["weather"][0]["main"]
                temperature = data["main"]["temp"]
                ruzgar_hiz = data["wind"]["speed"]
                nem_oran = data["main"]["humidity"]

                if temperature < 10.0:
                    sicaklik_mesaj = f"bugün hava {temperature} derece, mont giymeyi unutma"
                elif 10.0 <= temperature < 20.0:
                    sicaklik_mesaj = f"bugün hava {temperature} derece, uzun kollu giymeyi unutma"
                elif 20.0 <= temperature <= 30.0:
                    sicaklik_mesaj = f"bugün hava {temperature} derece, kısa kollu giyebilirsin"
                else:
                    sicaklik_mesaj = "bugün hava çok sıcak, öğle saatlerinde dışarı çıkmasan iyi olur"

                if weather == "Rain":
                    text = semsiye_mesaj
                elif weather == "Clear":
                    text = clear_mesaj
                elif weather == "Clouds":
                    text = clods_mesaj
                elif weather == "Snow":
                    text = snow_mesaj
                elif weather == "Drizzle":
                    text = drizle_mesaj
                elif weather == "Thunderstorm":
                    text = thunderstorm_mesaj

                gonderilcek_mesaj = (
                    f"{text} ve {sicaklik_mesaj}\n"
                    f"Rüzgar hızı: {ruzgar_hiz} m/s,\n"
                    f"Nem oranı: %{nem_oran}."
                )

                await bot.send_message(chat_id=CHAT_ID, text=gonderilcek_mesaj)

                print(weather)
                print(temperature)
                
            else:
                print("Hava durumu bilgisine ulaşılamadı.")

        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
