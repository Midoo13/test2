import telebot
import requests
from sum_processor import process_sum
import re
import base64
# توكن بوت تليجرام
API_TOKEN = '7416403497:AAE74rtu-2jMn7umERsn1mvxM9OVsTBwnyI'
GIST_TOKEN = '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'
bot = telebot.TeleBot(API_TOKEN)

# معرفات المستخدمين الذين لديهم حق الوصول للأوامر
AUTHORIZED_USER_ID = { '5149942884' ,'1167798421'}  # معرف المستخدم الذي يمكنه استخدام أوامر /add و /del

# رابط Gist
GIST_URL = 'https://api.github.com/gists/a23e1511367cce16d168cccbdd942a04'
GIST_au = 'https://api.github.com/gists/b2d4287953d98bdc6a93a9a63117133a'

def fetch_numbers_from_gist():
    response = requests.get(GIST_URL, headers={'Authorization': f'token {GIST_TOKEN}'})
    response.raise_for_status()
    gist_data = response.json()
    file_content = gist_data['files']['numbers.txt']['content']
    return set(file_content.split())

def update_gist_numbers(numbers):
    gist_data = requests.get(GIST_URL, headers={'Authorization': f'token {GIST_TOKEN}'}).json()
    content = '\n'.join(numbers)
    gist_data['files']['numbers.txt']['content'] = content
    requests.patch(GIST_URL, json=gist_data, headers={'Authorization': f'token {GIST_TOKEN}'})

@bot.message_handler(commands=['add'])
def add_number(message):
    user_id = str(message.from_user.id)

    if user_id not in AUTHORIZED_USER_ID:
        bot.send_message(message.chat.id, "ليس لديك صلاحية لاستخدام هذا الأمر.")
        return

    command_parts = message.text.split()
    if len(command_parts) != 2:
        bot.send_message(message.chat.id, "يرجى استخدام الصيغة الصحيحة: /add <number>")
        return
    
    number = command_parts[1]
    existing_numbers = fetch_numbers_from_gist()
    
    if number in existing_numbers:
        bot.send_message(message.chat.id, "هذا المستخدم موجود بالفعل.")
        return
    
    existing_numbers.add(number)
    update_gist_numbers(existing_numbers)
    bot.send_message(message.chat.id, "✅✅تمت إضافة المستخدم بنجاح.")

@bot.message_handler(commands=['del'])
def delete_number(message):
    user_id = str(message.from_user.id)
    
    if user_id not in AUTHORIZED_USER_ID:
        bot.send_message(message.chat.id, "ليس لديك صلاحية لاستخدام هذا الأمر.")
        return
    
    command_parts = message.text.split()
    if len(command_parts) != 2:
        bot.send_message(message.chat.id, "يرجى استخدام الصيغة الصحيحة: /del <number>")
        return
    
    number = command_parts[1]
    existing_numbers = fetch_numbers_from_gist()
    
    if number not in existing_numbers:
        bot.send_message(message.chat.id, "هذا المستخدم غير موجود.")
        return
    
    existing_numbers.remove(number)
    update_gist_numbers(existing_numbers)
    bot.send_message(message.chat.id, "✅✅تمت إزالة المستخدم بنجاح.")

@bot.message_handler(commands=['scan', 'SCAN', 'cc', 'CC'])
def handle_scan(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    authorized_users = fetch_numbers_from_gist()

    if user_id not in authorized_users:
        bot.send_message(
    message.chat.id,
    'ليس لديك صلاحية لاستخدام البوت\nتواصل معي للاشتراك في البوت\n\n<b>BY: <a href="https://t.me/ModyMohamed2">3𝑨𝑴𝑶 𝑫𝑬𝑽𝑰𝑳</a></b>\n\nUR TELEGRAM ID: {}'.format(user_id),
    parse_mode="HTML" , disable_web_page_preview=True)
        return

    MAX_LINES = 20

    bot.send_message(message.chat.id, "We are now processing your cards.🤌🤌")

    try:
        vbv = 0
        dd = 0
        tot = 0
        command_data = message.text.split(maxsplit=1)[1]
        lines = command_data.split('\n')
        if len(lines) > MAX_LINES:
            lines = lines[:MAX_LINES]
            bot.send_message(message.chat.id, f"تم تجاوز الحد الأقصى لعدد الأسطر، معالجة أول {MAX_LINES} أسطر فقط.")

        for line in lines:
            result = process_sum(line.strip() )
            if "approved" in result:
                approved_message = f'<b>APPROVED CARD✅</b>\n<b>UR card</b>⇾ <code>{line.strip()}</code>\n<b>BY : <a href="https://t.me/ModyMohamed2">3𝑨𝑴𝑶 𝑫𝑬𝑽𝑰𝑳</a></b>'
                bot.send_message(message.chat.id, approved_message, parse_mode="HTML", disable_web_page_preview=True)
                vbv += 1
            elif "dead" in result:
                dd += 1
            else:
                approved_message = f"<b></b>\n<b>UR card</b>⇾ <code>{line.strip()}</code>\n{result}"
                bot.send_message(message.chat.id, approved_message, parse_mode="HTML")
                tot += 1

        # حساب المجموع
        total = vbv + dd + tot
        massa = f'<b>Thank you for checking your cards.</b>\n\n<b>TOTAL CARDS = {total}</b>\n\n<b>LIVE CARDS</b>✅ = {vbv}\n\n<b>DEAD CARDS</b>❌ = {dd}\n\n<b>UNKNOWN CARDS</b>❓ = {tot}\n<b>BY: <a href="https://t.me/ModyMohamed2">3𝑨𝑴𝑶 𝑫𝑬𝑽𝑰𝑳</a></b>'
        bot.send_message(message.chat.id, massa, parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ: {str(e)}")

bot.polling()