from telethon.sync import TelegramClient, events
import re, random, asyncio, requests, telebot

token = "7521910621:AAGblqyWQ4LOmX7WRSG_8Acu8GCqqExZxvs"
bot = telebot.TeleBot(token, parse_mode="HTML")

api_id = '28334196'
api_hash = 'dd3c4aa0133fb57ec9eef25252b2f266'

client = TelegramClient("sessioa", api_id, api_hash)

target_channel_id = "-1002416940134"  # يوزر القناة التي يتم النشر فيها

photo_urls = [
"https://t.me/icons_drag/163",
"https://t.me/icons_drag/164",
"https://t.me/icons_drag/165",
"https://t.me/icons_drag/166",
"https://t.me/icons_drag/168",
"https://t.me/icons_drag/169",
"https://t.me/icons_drag/170",
"https://t.me/icons_drag/171",
"https://t.me/icons_drag/172",
"https://t.me/icons_drag/173",
"https://t.me/icons_drag/174",
"https://t.me/icons_drag/175",
]  # روابط صور يستخدمها عشوائيًا
used_photos = []  # قائمة لتتبع الصور التي تم استخدامها

new = []

async def extract_card(search):  # استخراج الفيزا من الرسالة
    month_match = re.search(r'\b(0?[1-9]|1[0-2])\b', search)
    month = month_match.group(0)
    year_match = re.search(r'\b(20[2-4][0-9]|2[4-9]|3[0-5])\b', search)
    year = year_match.group(0)
    
    num_match = re.search(r'\b\d{15,16}\b', search)
    num = num_match.group(0)
    if num.startswith("3"):
        cvv_match = re.search(r'\b(?!20[2-3][0-9])\d{4}\b', search)
    else:
        cvv_match = re.search(r'\b\d{3}\b(?!\s*(20[2-4][0-9]|2[4-9]|3[0-5]))', search)

    cvv = cvv_match.group(0)
    card = f'{num}|{month}|{year}|{cvv}'
    print(card)
    return num, month, year, cvv

ids = [
    -1002284237960
]  # أيدي القنوات التي يتم مراقبتها

from telethon.tl.custom import Button

@client.on(events.NewMessage(chats=ids))
async def process_message(event):
    print(event.message.text)
    search = event.message.text
    if search:
        try:
            num, month, year, cvv = await extract_card(search)
        except:
            return
        card = f'{num}|{month}|{year}|{cvv}'
        if num not in new:
            new.append(num)

            # اختيار صورة عشوائية بدون تكرار
            global used_photos
            available_photos = [url for url in photo_urls if url not in used_photos]
            if not available_photos:  # إذا تم استخدام جميع الصور، أعد التهيئة
                used_photos = []
                available_photos = photo_urls
            photo_url = random.choice(available_photos)
            used_photos.append(photo_url)

            brand, bin, type, level, bank, country_name, country_flag = await info(card)

            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(
                Button.url("𝗢𝘄𝗻𝗲𝗿", "https://t.me/mohamed_was_here1"),
                Button.url("𝗦𝗼𝘂𝗿𝗰𝗲", "https://t.me/c/2416940134/12")
            )
            bot.send_photo(target_channel_id, photo_url, caption=f'''
• 𝖢𝖢 ⇾ <code>{card}</code>
• 𝖦𝖺𝗍𝖾𝗐𝖺𝗒 ⇾ Braintree Auth & Stripe Auth
• 𝖱𝖾𝗌𝗉𝗈𝗇𝗌𝖾 ⇾ SUCCESS
• 𝖱𝖾𝗌𝗎𝗅𝗍𝗌 ⇾ Approved ✅
━━━━━━•𝗜𝗻𝗳𝗼•━━━━━━
• 𝖡𝗂𝗇 ⇾ {bin} - {type} - {brand} - {level}
• 𝖡𝖺𝗇𝗄 ⇾ {bank}
• 𝖢𝗈𝗎𝗇𝗍𝗋𝗒 ⇾ {country_name} {country_flag}
''', reply_markup=markup, parse_mode='HTML')

async def info(card):
    response = requests.get('https://bins.antipublic.cc/bins/' + card[:6])
    
    data = ['bin', 'brand', 'type', 'level', 'bank', 'country_name', 'country_flag']
    result = []
        
    for field in data:
        try:
            result.append(response.json()[field])
        except:
            result.append("------")  
    
    return tuple(result)

print("Bot started. Listening for commands...")
client.start()
client.run_until_disconnected()