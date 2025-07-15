#!/usr/bin/env python3
import telebot
import requests
import qrcode
import os
import time
from datetime import datetime, timedelta
from telebot.types import InputFile
import re
from threading import Thread

BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN')
SERPAPI_KEY = os.getenv('SERPAPI_KEY', 'YOUR_SERPAPI_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
goals = {}
def is_valid_url(url):
    regex = r'^(https?://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
    return re.match(regex, url) is not None

def safe_web_search(query):
    try:
        params = {'q': query, 'api_key': SERPAPI_KEY}
        response = requests.get('https://serpapi.com/search', params=params, timeout=10)
        response.raise_for_status()
        results = response.json()
        organic = results.get('organic_results', [])
        if not organic:
            return "No results found."
        return '\n'.join([f"{r.get('title', '')}: {r.get('link', '')}" for r in organic[:3]])
    except requests.RequestException as e:
        return f"Error during web search: {str(e)}"

def schedule_notifications(chat_id, goal, deadline):
    bot.send_message(chat_id, f"Goal set: '{goal}' with deadline {deadline.strftime('%Y-%m-%d %H:%M')}.")
    reminder_time = deadline - timedelta(hours=1)
    now = datetime.now()
    if reminder_time > now:
        time_to_reminder = (reminder_time - now).total_seconds()
        def send_reminder():
            time.sleep(time_to_reminder)
            bot.send_message(chat_id, f"Reminder: Your goal '{goal}' is due in 1 hour!")
        Thread(target=send_reminder).start()

    time_to_deadline = (deadline - now).total_seconds()
    if time_to_deadline > 0:
        def send_deadline():
            time.sleep(time_to_deadline)
            bot.send_message(chat_id, f"Deadline reached for goal: '{goal}'!")
        Thread(target=send_deadline).start()
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to TaskMasterBot! Use /search, /setgoal, /adduser, /qrcode, /groupdata, or /promote.")

@bot.message_handler(commands=['search'])
def search_web(message):
    query = message.text[len('/search '):].strip()
    if not query:
        bot.reply_to(message, "Please provide a search query. Usage: /search <query>")
        return
    bot.reply_to(message, "Searching...")
    results = safe_web_search(query)
    bot.reply_to(message, results)

@bot.message_handler(commands=['setgoal'])
def set_goal(message):
    try:
        parts = message.text[len('/setgoal '):].strip().split('|')
        if len(parts) != 2:
            bot.reply_to(message, "Usage: /setgoal <goal> | <YYYY-MM-DD HH:MM>")
            return
        goal, deadline_str = parts
        deadline = datetime.strptime(deadline_str.strip(), '%Y-%m-%d %H:%M')
        if deadline < datetime.now():
            bot.reply_to(message, "Deadline must be in the future.")
            return
        goals[message.chat.id] = {'goal': goal.strip(), 'deadline': deadline}
        schedule_notifications(message.chat.id, goal.strip(), deadline)
    except ValueError:
        bot.reply_to(message, "Invalid date format. Use: /setgoal <goal> | YYYY-MM-DD HH:MM")

@bot.message_handler(commands=['adduser'])
def add_user(message):
    phone = message.text[len('/adduser '):].strip()
    if not re.match(r'^\+\d{10,15}$', phone):
        bot.reply_to(message, "Invalid phone number. Use format: /adduser +1234567890")
        return
    try:
        bot.reply_to(message, f"User with phone {phone} added to contact list (simulated).")
    except Exception as e:
        bot.reply_to(message, f"Error adding user: {str(e)}")

@bot.message_handler(commands=['qrcode'])
def generate_qr(message):
    url = message.text[len('/qrcode '):].strip()
    if not is_valid_url(url):
        bot.reply_to(message, "Invalid URL. Use format: /qrcode https://example.com")
        return
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcode.png")
    with open("qrcode.png", 'rb') as qr_file:
        bot.send_photo(message.chat.id, InputFile(qr_file))
    os.remove("qrcode.png")

@bot.message_handler(commands=['groupdata'])
def get_group_data(message):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "This command only works in groups.")
        return
    try:
        members = bot.get_chat_members_count(message.chat.id)
        admins = bot.get_chat_administrators(message.chat.id)
        admin_names = [admin.user.first_name for admin in admins]
        bot.reply_to(message, f"Group: {message.chat.title}\nMembers: {members}\nAdmins: {', '.join(admin_names)}")
    except Exception as e:
        bot.reply_to(message, f"Error fetching group data: {str(e)}")

@bot.message_handler(commands=['promote'])
def promote_user(message):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "This command only works in groups.")
        return
    parts = message.text[len('/promote '):].strip().split('|')
    if len(parts) != 2 or parts[1].strip() not in ['member', 'admin']:
        bot.reply_to(message, "Usage: /promote <username> | <member|admin>")
        return
    username, role = parts
    username = username.strip().lstrip('@')
    try:

        members = bot.get_chat_members(message.chat.id)
        user_id = None
        for member in members:
            if member.user.username == username:
                user_id = member.user.id
                break
        if not user_id:
            bot.reply_to(message, f"User @{username} not found in group.")
            return
        if role == 'admin':
            bot.promote_chat_member(
                message.chat.id, user_id,
                can_change_info=True, can_delete_messages=True, can_invite_users=True
            )
            bot.reply_to(message, f"Promoted @{username} to admin.")
        else:

            bot.promote_chat_member(
                message.chat.id, user_id,
                can_change_info=False, can_delete_messages=False, can_invite_users=False
            )
            bot.reply_to(message, f"Set @{username} as member.")
    except Exception as e:
        bot.reply_to(message, f"Error promoting user: {str(e)}")

if __name__ == "__main__":
    bot.infinity_polling()
