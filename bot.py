import telebot
import requests
import time

from sum_processor import process_sum
from keep_alive import keep_alive

keep_alive()  # This will keep the bot alive

API_TOKEN = '7424829556:AAEarbNLH2Or_XD8P83xwI6qOiDj2zIuTOU'
GIST_URL = 'https://api.github.com/gists/981d16aec654291008480155fb7eee53'
GIST_TOKEN = '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'

bot = telebot.TeleBot(API_TOKEN)

AUTHORIZED_USER_ID = {'1142240722'}  # Admin User ID
MAX_LINES = 20  # Increased limit to match the first code

# Fetch numbers from Gist
def fetch_numbers_from_gist():
    try:
        response = requests.get(GIST_URL, headers={'Authorization': f'token {GIST_TOKEN}'})
        response.raise_for_status()
        gist_data = response.json()
        if 'numbers.txt' not in gist_data.get('files', {}):
            print("File 'numbers.txt' not found in the Gist.")
            return set()
        file_content = gist_data['files']['numbers.txt']['content']
        return set(file_content.split())
    except requests.RequestException as e:
        print(f"Error fetching numbers from Gist: {e}")
        return set()

# Update numbers in Gist
def update_gist_numbers(numbers):
    try:
        content = '\n'.join(numbers)
        gist_data = {"files": {"numbers.txt": {"content": content}}}
        response = requests.patch(GIST_URL, json=gist_data, headers={'Authorization': f'token {GIST_TOKEN}'})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error updating Gist: {e}")

# Check if user is authorized
def is_authorized(user_id):
    authorized_users = fetch_numbers_from_gist()
    return str(user_id) in AUTHORIZED_USER_ID or str(user_id) in authorized_users

# Add a new number
@bot.message_handler(commands=['add'])
def add_number(message):
    user_id = str(message.from_user.id)
    if not is_authorized(user_id):
        bot.send_message(message.chat.id, "You do not have permission to use this command ❌")
        return
    command_parts = message.text.split()
    if len(command_parts) != 2:
        bot.send_message(message.chat.id, "يرجى استخدام الصيغة الصحيحة: /add <number>")
        return
    number = command_parts[1]
    existing_numbers = fetch_numbers_from_gist()
    if number in existing_numbers:
        bot.send_message(message.chat.id, "This user already exists.")
    else:
        existing_numbers.add(number)
        update_gist_numbers(existing_numbers)
        bot.send_message(message.chat.id, "The user has been added successfully ✅")

# Delete a number
@bot.message_handler(commands=['del'])
def delete_number(message):
    user_id = str(message.from_user.id)
    if not is_authorized(user_id):
        bot.send_message(message.chat.id, "You do not have permission to use this command ❌")
        return
    command_parts = message.text.split()
    if len(command_parts) != 2:
        bot.send_message(message.chat.id, "يرجى استخدام الصيغة الصحيحة: /del <number>")
        return
    number = command_parts[1]
    existing_numbers = fetch_numbers_from_gist()
    if number not in existing_numbers:
        bot.send_message(message.chat.id, "This User Is Not Found.")
    else:
        existing_numbers.remove(number)
        update_gist_numbers(existing_numbers)
        bot.send_message(message.chat.id, "This User Is Removed Successfully ✅")

# Handle scan commands
@bot.message_handler(commands=['scan', 'X', 'chk', 'x', 'cc'])
def handle_scan(message):
    user_id = str(message.from_user.id)
    authorized_users = fetch_numbers_from_gist()
    if user_id not in authorized_users:
        bot.send_message(
            message.chat.id,
            'You do not have permission to use the bot.\nContact me to subscribe to the bot.\n\n<b>BY: <a href="https://t.me/Mdoo100">Midoo</a></b>\n\nUR TELEGRAM ID: {}'.format(user_id),
            parse_mode="HTML", disable_web_page_preview=True)
        return
    bot.send_message(message.chat.id, "Pls Wait Checking your cards ⏳⏳")
    try:
        command_data = message.text.split(maxsplit=1)[1]
        lines = command_data.split('\n')
        if len(lines) > MAX_LINES:
            lines = lines[:MAX_LINES]
            bot.send_message(message.chat.id, f"تم تجاوز الحد الأقصى لعدد الأسطر، معالجة أول {MAX_LINES} أسطر فقط.")
        vbv, dd, tot = 0, 0, 0
        for line in lines:
            result = process_sum(line.strip())
            if "approved" in result:
                vbv += 1
                bot.send_message(message.chat.id, f'<b>APPROVED CARD✅</b>\n<b>UR card</b>⇾ <code>{line.strip()}</code>', parse_mode="HTML")
            elif "dead" in result:
                dd += 1
            else:
                tot += 1
                bot.send_message(message.chat.id, f"<b>UR card</b>⇾ <code>{line.strip()}</code>\n{result}", parse_mode="HTML")
                time.sleep(5)
        total = vbv + dd + tot
        summary = f'<b>TOTAL CARDS = {total}</b>\n<b>LIVE CARDS✅ = {vbv}</b>\n<b>DEAD CARDS❌ = {dd}</b>'
        bot.send_message(message.chat.id, summary, parse_mode="HTML")
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ: {str(e)}")

bot.polling(none_stop=True, interval=0, timeout=60)
