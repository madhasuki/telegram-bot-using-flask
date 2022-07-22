import json
import requests
from flask import Flask
from flask import request
from flask import Response
# from flask_ngrok import run_with_ngrok
# from pyngrok import ngrok
# # ngrok authtoken
# ngrok.set_auth_token("20ez4X4SJL9UNgg1z0nrXw4mH9y_7NEpNEkriLPcj4ggJf6vC")

# bot token
TOKEN_BOT = "5404069568:AAFgXr_me8VGucZbXxg3hoReigep8jG9JEg"

app = Flask(__name__)
# run_with_ngrok(app)

# --- COMMAND FUNCTION ---


def start(nama):
    return "Assalamu'alaikum kak {}".format(nama)


def help():
    return '''
    Untuk menggunakan bot ini, silahkan masukkan nomor surah dan nomor ayat yang dipisahkan dengan titik dua.\nContohnya seperti 78:8 untuk mencari Surah An-Naba ayat 78'''

# ------------------------

def save_chat_id(chat_id):
    list_chat_id = []
    filename = "/home/madhasoeki/bot/chat_id.txt"
    # open file in write mode
    with open(filename, 'r') as f:
        for line in f:
            x = line[:-1]
            list_chat_id.append(x)
    if chat_id not in list_chat_id:
        list_chat_id.append(chat_id)
        with open(filename, 'w') as f:
            for item in list_chat_id:
                f.write("%s\n" % item)

def get_ayat(no_surat, ayat, surah):
    # If using local json file
    file_path = '/home/madhasoeki/bot/json/{}.json'.format(no_surat)
    with open(file_path, 'r', encoding="utf8") as j:
        data = json.loads(j.read())
        the_ayat = data[ayat-1]

    reply = "{}\n{}\n(Q.S. {} : {})".format(the_ayat['ar'], the_ayat['id'], surah['nama'], ayat)
    return reply

def parse_message(message):
    nama = message['message']['from']['first_name']
    chat_id = message['message']['chat']['id']
    text = message['message']['text']

    # save chat id
    save_chat_id(chat_id)
    # check if if it is a command or not
    if text[0] == "/":
        command = text[1:].lower()
        if command == "start":
            reply = start(nama)
        elif command == "help":
            reply = help()
        else:
            reply = "Maaf perintah tidak dikenali"

    elif ":" in text:
        chat = text.split(':')
        # get surah number and ayat
        no_surah, ayat = chat[0], chat[1]
        if no_surah.isdigit() and ayat.isdigit():
            no_surah, ayat = int(chat[0]), int(chat[1])
            if no_surah > 0 and no_surah <= 114:
                file_path = '/home/madhasoeki/bot/json/surah.json'
                with open(file_path, 'r', encoding="utf8") as j:
                    data = json.loads(j.read())
                surah = data[no_surah-1]
                jumlah_ayat = surah['ayat']
                if ayat > 0 and ayat <= jumlah_ayat:
                    reply = get_ayat(no_surah, ayat, surah)
                else:
                    reply = "Maaf ayat ini tidak ada"
            else:
                reply = "Maaf no_surah ini tidak ada"
        else:
            reply = '''
            Maaf format yang anda masukkan salah.\nPastikan anda memasukkan nomor no_surah dan ayat dan dibatasi dengan titik dua (:)\nContoh : 2:5'''
    else:
        reply = '''
        Maaf format yang anda masukkan salah.\nPastikan anda memasukkan nomor no_surah dan ayat dan dibatasi dengan titik dua (:)\nContoh : 2:5'''

    return chat_id, reply


def send_message(chat_id, text):
    url = "https://api.telegram.org/bot{}/sendMessage".format(TOKEN_BOT)
    payload = {
        "chat_id":chat_id,
        "text": text
    }

    r = requests.post(url, json=payload)
    return r


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id, reply = parse_message(msg)
        send_message(chat_id, reply)
        return Response('ok', status=200)
    else:
        return "OK"

if __name__ == '__main__':
    app.run()