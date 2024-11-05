import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request, send_file
import ffmpeg
import zipfile
from PIL import Image
import io

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Dictionary to store user's file and selected conversion
user_files = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the File Converter Bot! Send me a file to convert.")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    user_files[message.chat.id] = {'file': downloaded_file, 'name': message.document.file_name}
    show_conversion_options(message.chat.id)

def show_conversion_options(chat_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("ZIP", callback_data="zip"),
        InlineKeyboardButton("IMG", callback_data="img"),
        InlineKeyboardButton("MP4", callback_data="mp4"),
        InlineKeyboardButton("MP3", callback_data="mp3"),
        InlineKeyboardButton("GIF", callback_data="gif")
    )
    bot.send_message(chat_id, "Choose the format to convert to:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data in ["zip", "img", "mp4", "mp3", "gif"]:
        chat_id = call.message.chat.id
        if chat_id in user_files:
            user_files[chat_id]['convert_to'] = call.data
            bot.answer_callback_query(call.id, "Converting your file...")
            convert_and_send_file(chat_id)
        else:
            bot.answer_callback_query(call.id, "Please send a file first.")

def convert_and_send_file(chat_id):
    file_data = user_files[chat_id]['file']
    original_filename = user_files[chat_id]['name']
    convert_to = user_files[chat_id]['convert_to']
    
    try:
        if convert_to == 'zip':
            converted_file = io.BytesIO()
            with zipfile.ZipFile(converted_file, 'w') as zf:
                zf.writestr(original_filename, file_data)
            converted_file.seek(0)
            new_filename = f"{os.path.splitext(original_filename)[0]}.zip"
        elif convert_to == 'img':
            image = Image.open(io.BytesIO(file_data))
            converted_file = io.BytesIO()
            image.save(converted_file, format='PNG')
            converted_file.seek(0)
            new_filename = f"{os.path.splitext(original_filename)[0]}.png"
        elif convert_to in ['mp4', 'mp3', 'gif']:
            input_file = f"/tmp/{original_filename}"
            output_file = f"/tmp/{os.path.splitext(original_filename)[0]}.{convert_to}"
            with open(input_file, 'wb') as f:
                f.write(file_data)
            
            stream = ffmpeg.input(input_file)
            stream = ffmpeg.output(stream, output_file)
            ffmpeg.run(stream)
            
            with open(output_file, 'rb') as f:
                converted_file = io.BytesIO(f.read())
            new_filename = os.path.basename(output_file)
            
            os.remove(input_file)
            os.remove(output_file)
        
        bot.send_document(chat_id, converted_file, visible_file_name=new_filename)
    except Exception as e:
        bot.send_message(chat_id, f"An error occurred during conversion: {str(e)}")
    finally:
        del user_files[chat_id]

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your-app-name.onrender.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))