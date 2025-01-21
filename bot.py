import telebot
import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_TOKEN = '7424829556:AAEarbNLH2Or_XD8P83xwI6qOiDj2zIuTOU'

bot = telebot.TeleBot(API_TOKEN)

AUTHORIZED_USER_ID = {'1142240722'}  # Admin User ID
USERS_FILE = 'users.txt'  # ملف محلي لتخزين المستخدمين المصرح لهم
MAX_LINES = 20

# قراءة المستخدمين من الملف
def read_users():
    try:
        with open(USERS_FILE, 'r') as file:
            return set(line.strip() for line in file if line.strip())
    except FileNotFoundError:
        logging.warning(f"File {USERS_FILE} not found. Creating a new one.")
        open(USERS_FILE, 'w').close()
        return set()

# كتابة المستخدمين إلى الملف
def write_users(users):
    with open(USERS_FILE, 'w') as file:
        file.write('\n'.join(users))

# التحقق من الصلاحيات
def is_authorized(user_id):
    authorized_users = read_users()
    return str(user_id) in AUTHORIZED_USER_ID or str(user_id) in authorized_users

# إضافة مستخدم جديد
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
    existing_users = read_users()
    if number in existing_users:
        bot.send_message(message.chat.id, "This user already exists.")
    else:
        existing_users.add(number)
        write_users(existing_users)
        bot.send_message(message.chat.id, "The user has been added successfully ✅")

# حذف مستخدم
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
    existing_users = read_users()
    if number not in existing_users:
        bot.send_message(message.chat.id, "This User Is Not Found.")
    else:
        existing_users.remove(number)
        write_users(existing_users)
        bot.send_message(message.chat.id, "This User Is Removed Successfully ✅")

# فحص البيانات
@bot.message_handler(commands=['scan', 'X', 'chk', 'x', 'cc'])
def handle_scan(message):
    user_id = str(message.from_user.id)
    if not is_authorized(user_id):
        bot.send_message(
            message.chat.id,
            f'You do not have permission to use the bot.\nContact me to subscribe to the bot.\n\n<b>UR TELEGRAM ID: {user_id}</b>',
            parse_mode="HTML", disable_web_page_preview=True)
        return
    bot.send_message(message.chat.id, "Pls Wait Checking your cards ⏳⏳")
    try:
        command_data = message.text.split(maxsplit=1)[1]
        lines = command_data.split('\n')
        if len(lines) > MAX_LINES:
            lines = lines[:MAX_LINES]
            bot.send_message(message.chat.id, f"تم تجاوز الحد الأقصى لعدد الأسطر، معالجة أول {MAX_LINES} أسطر فقط.")
        # عملية المعالجة الوهمية
        bot.send_message(message.chat.id, "Processing your data... (Simulation)")
    except Exception as e:
        logging.error(f"Error in handle_scan: {e}")
        bot.send_message(message.chat.id, f"حدث خطأ: {str(e)}")
       
bot.polling(none_stop=True, interval=0, timeout=60)
