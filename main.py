import json
import requests
from flask import Flask
from flask import request
from flask import Response 
from flask_sslify import SSLify
# from flask_ngrok import run_with_ngrok
# from pyngrok import ngrok
# # ngrok authtoken
# ngrok.set_auth_token("20ez4X4SJL9UNgg1z0nrXw4mH9y_7NEpNEkriLPcj4ggJf6vC")

# bot token
TOKEN_BOT = "5404069568:AAFgXr_me8VGucZbXxg3hoReigep8jG9JEg"

app = Flask(__name__)
sslify = SSLify(app)
# run_with_ngrok(app)

# def write_json(data, json_filename):
#     with open(json_filename, 'w') as f:
#         json.dump(data, f, indent=2, ensure_ascii=False)

def get_ayat(no_surat, ayat, surah):
    file_path = 'json/{}.json'.format(no_surat)
    with open(file_path, 'r', encoding="utf8") as j: 
        data = json.loads(j.read())
        the_ayat = data[ayat-1]

    reply = "{}\n{}\n(Q.S. {} : {})".format(the_ayat['ar'], the_ayat['id'], surah['nama'], ayat, ayat)
    return reply

def parse_message(message):
    chat_id = message['message']['chat']['id']
    text = message['message']['text']

    if ":" in text:
        chat = text.split(':')
        # get surah number and ayat
        no_surah, ayat = chat[0], chat[1]
        if no_surah.isdigit() and ayat.isdigit():
            no_surah, ayat = int(chat[0]), int(chat[1])
            if no_surah > 0 and no_surah <= 114:
                # data = requests.get(api).json()
                file_path = 'json/surah.json'
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
        # write_json(msg, 'telegram_request.json')
        return Response('ok', status=200)
    else:
        return "<h1>Quran SIDAQ bot</h1>"

if __name__ == '__main__':
    # main()
    app.run()