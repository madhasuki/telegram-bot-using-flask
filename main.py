import re
import os
import json
import requests
import random

from flask import Flask, request, Response

#TOKEN_BOT = your bot token
DIR = os.getcwd()

app = Flask(__name__)

# --- COMMAND FUNCTION ---


def start(nama):
    return "Assalamu'alaikum kak {}".format(nama)


def acak():
    no_surah = random.randrange(1, 115)

    file_path = DIR + "/bot/json/{}.json".format(no_surah)

    with open(file_path, "r", encoding="utf8") as datafile:
        data = json.loads(datafile.read())
        data_surah = data["data"]
        jumlah_ayat = data_surah["numberOfVerses"]
        nama_surah = data_surah["name"]['transliteration']['id']
    no_ayat = random.randrange(jumlah_ayat)

    data_ayat = data_surah["verses"][int(no_ayat)-1]
    arab = data_ayat["text"]["arab"]
    indo = data_ayat["translation"]["id"]

    return "{} \n{} \nQ.S {} [{}:{}]".format(arab, indo, nama_surah, no_surah, no_ayat)


def info():
    return """
    Berikut info nama surah dalam Al-Qur'an secara berurutan dan arti dari nama surah tersebut :

    1. Al Fatihah (Pembuka)
    2. Al Baqarah (Sapi Betina)
    3. Ali Imran (Keluarga Imran)
    4. An Nisa (Wanita)
    5. Al Ma'idah (Jamuan)
    6. Al An'am (Hewan Ternak)
    7. Al-A'raf (Tempat yang Tertinggi)
    8. Al-Anfal (Harta Rampasan Perang)
    9. At-Taubah(Pengampunan)
    10. Yunus (Nabi Yunus)
    11. Hud (Nabi Hud)
    12. Yusuf (Nabi Yusu)
    13. Ar-Ra'd (Guruh)
    14. Ibrahim (Nabi Ibrahim)
    15. Al-Hijr (Gunung Al Hijr)
    16. An-Nahl (Lebah)
    17. Al-Isra' (Perjalanan Malam)
    18. Al-Kahf (Penghuni-penghuni Gua)
    19. Maryam (Maryam)
    20. Ta Ha (Ta Ha)
    21. Al-Anbiya (Nabi-Nabi)
    22. Al-Hajj (Haji)
    23. Al-Mu'minun (Orang-orang mukmin)
    24. An-Nur (Cahaya)
    25. Al-Furqan (Pembeda)
    26. Asy-Syu'ara' (Penyair)
    27. An-Naml (Semut)
    28. Al-Qasas (Kisah-kisah)
    29. Al-'Ankabut (Laba-laba)
    30. Ar-Rum (Bangsa Romawi)
    31. Luqman (Keluarga Luqman)
    32. As-Sajdah (Sajdah)
    33. Al-Ahzab (Golongan-golongan yang Bersekutu)
    34. Saba' (Kaum Saba')
    35. Fatir (Pencipta)
    36. Ya Sin (Yaasiin)
    37. As-Saffat (Barisan-barisan)
    38. Sad (Shaad)
    39. Az-Zumar (Rombongan-rombongan)
    40. Ghafir (Yang Mengampuni)
    41. Fussilat (Yang Dijelaskan)
    42. Asy-Syura (Musyawarah)
    43. Az-Zukhruf (Perhiasan)
    44. Ad-Dukhan (Kabut)
    45. Al-Jasiyah (Yang Bertekuk Lutut)
    46. Al-Ahqaf (Bukit-bukit Pasir)
    47. Muhammad (Nabi Muhammad)
    48. Al-Fath (Kemenangan)
    49. Al-Hujurat (Kamar-kamar)
    50. Qaf (Qaaf)
    51. Az-Zariyat (Angin yang Menerbangkan)
    52. At-Tur (Bukit)
    53. An-Najm (Bintang)
    54. Al-Qamar (Bulan)
    55. Ar-Rahman (Yang Maha Pemurah)
    56. Al-Waqi'ah (Hari Kiamat)
    57. Al-Hadid (Besi)
    58. Al-Mujadilah (Wanita yang Mengajukan Gugatan)
    59. Al-Hasyr (Pengusiran)
    60. Al-Mumtahanah (Wanita yang Diuji)
    61. As-Saff (Satu Barisan)
    62. Al-Jumu'ah (Hari Jum'at)
    63. Al-Munafiqun (Orang-orang yang Munafik)
    64. At-Tagabun (Hari Dinampakkan Kesalahan-kesalahan)
    65. At-Talaq (Talak)
    67. Al-Mulk (Kerajaan)
    68. Al-Qalam (Pena)
    69. Al-Haqqah (Hari Kiamat)
    70. Al-Ma'arij (Tempat Naik)
    71. Nuh (Nabi Nuh)
    72. Al-Jinn (Jin)
    73. Al-Muzzammil (Orang yang Berselimut)
    74. Al-Muddassir (Orang yang Berkemul)
    75. Al-Qiyamah (Kiamat)
    76. Al-Insan (Manusia)
    77. Al-Mursalat (Malaikat-Malaikat Yang Diutus)
    78. An-Naba' (Berita Besar)
    79. An-Nazi'at (Malaikat-Malaikat Yang Mencabut)
    80. 'Abasa (Ia Bermuka Masam)
    81. At-Takwir (Menggulung)
    82. Al-Infitar (Terbelah)
    83. Al-Tatfif (Orang-orang yang Curang)
    84. Al-Insyiqaq (Terbelah)
    85. Al-Buruj (Gugusan Bintang)
    86. At-Tariq (Yang Datang di Malam Hari)
    87. Al-A'la (Yang Paling Tinggi)
    88. Al-Gasyiyah (Hari Pembalasan)
    89. Al-Fajr (Fajar)
    90. Al-Balad (Negeri)
    91. Asy-Syams (Matahari)
    92. Al-Lail (Malam)
    93. Ad-Duha (Waktu Matahari Sepenggalahan Naik (Dhuha))
    94. Al-Insyirah (Melapangkan)
    95. At-Tin (Buah Tin)
    96. Al-'Alaq (Segumpal Darah)
    97. Al-Qadr (Kemuliaan)
    98. Al-Bayyinah (Pembuktian)
    99. Az-Zalzalah (Kegoncangan)
    100. Al-'Adiyat (Berlari Kencang)
    101. Al-Qari'ah (Hari Kiamat)
    102. At-Takasur (Bermegah-megahan)
    103. Al-'Asr (Masa)
    104. Al-Humazah (Pengumpat)
    105. Al-Fil (Gajah)
    106. Quraisy (Suku Quraisy)
    107. Al-Ma'un (Barang-barang yang Berguna)
    108. Al-Kausar (Nikmat yang Berlimpah)
    109. Al-Kafirun (Orang-orang Kafir)
    110. An-Nasr (Pertolongan)
    111. Al-Lahab (Gejolak Api)
    112. Al-Ikhlas (Ikhlas)
    113. Al-Falaq (Waktu Subuh)
    114. An-Nas (Umat Manusia)

    TAFSIR YANG DIGUNAKAN PADA BOT INI ADALAH TAFSIR DARI KEMENAG !!!"""


def help():
    return '''
    Untuk menggunakan bot ini, silahkan masukkan nomor surah dan nomor ayat yang dipisahkan dengan titik dua.\nContohnya seperti 78:8 untuk mencari Surah An-Naba ayat 78'''

# ------------------------


def save_chat_id(chat_id):
    filename = DIR + "/bot/chat_id.txt"
    chat_id_file = open(filename, "r")
    content_list = chat_id_file.readlines()
    content_list.append("{}\n".format(chat_id))
    rm_dup = set(content_list)
    with open(filename, "w") as f:
        for isi in rm_dup:
            f.write(isi)


def send_no_button(chat_id, text):
    url = "https://api.telegram.org/bot{}/sendMessage".format(TOKEN_BOT)
    payload = {
        "chat_id":chat_id,
        "text": text
    }
    requests.post(url, json=payload)


def send_with_button(chat_id, text, first, last):
    url = "https://api.telegram.org/bot{}/sendMessage".format(TOKEN_BOT)
    if first:
        keyboard =  [[
                        {
                            "text": "Ayat Setelahnya",
                            "callback_data": "after"
                        }
                    ],
                    [
                        {
                            "text": "Tafsir Kemenag",
                            "callback_data": "tafsir"
                        }
                    ]]
    elif last:
        keyboard =  [[
                        {
                            "text": "Ayat Sebelumnya",
                            "callback_data": "before"
                        }
                    ],
                    [
                        {
                            "text": "Tafsir Kemenag",
                            "callback_data": "tafsir"
                        }
                    ]]
    else:
        keyboard =  [[
                        {
                            "text": "Ayat Sebelumnya",
                            "callback_data": "before"
                        },
                        {
                            "text": "Ayat Setelahnya",
                            "callback_data": "after"
                        }
                    ],
                    [
                        {
                            "text": "Tafsir Kemenag",
                            "callback_data": "tafsir"
                        }
                    ]]

    payload = {
        "chat_id":chat_id,
        "text": text,
        "reply_markup": {
            "inline_keyboard": keyboard
        }
    }
    requests.post(url, json=payload)


def callback_process(message, query_data):
    chat_id = message["message"]["chat"]["id"]
    text = message["message"]["text"]
    text_re = re.findall("[0-9]+:[0-9]+", text)[0]
    no_surah, no_ayat = text_re.split(":")

    file_path = DIR + "/bot/json/{}.json".format(no_surah)

    with open(file_path, "r", encoding="utf8") as datafile:
        data = json.loads(datafile.read())
        data_surah = data["data"]
        nama_surah = data_surah["name"]['transliteration']['id']
        data_ayat = data_surah["verses"][int(no_ayat)-1]

    if query_data == "tafsir":
        tafsir = data_ayat["tafsir"]["id"]["long"]
        reply = "{} \nQ.S {} [{}:{}]".format(tafsir, nama_surah, no_surah, no_ayat)
        send_no_button(chat_id, reply)
    elif query_data == "before":

        data_ayat = data_surah["verses"][int(no_ayat)-2]
        arab = data_ayat["text"]["arab"]
        indo = data_ayat["translation"]["id"]
        text = "{}\n{}\nQ.S {} [{}:{}]".format(arab, indo, nama_surah, no_surah, (int(no_ayat)-1))
        send_with_button(chat_id, text)
    elif query_data == "after":
        data_ayat = data_surah["verses"][int(no_ayat)]
        arab = data_ayat["text"]["arab"]
        indo = data_ayat["translation"]["id"]
        text = "{}\n{}\nQ.S {} [{}:{}]".format(arab, indo, nama_surah, no_surah, (int(no_ayat)+1))
        send_with_button(chat_id, text)



def update_process(message):
    chat_id = message["message"]["chat"]["id"]
    text = message["message"]["text"]
    err = None

    # the input we actually want. So we can get surah and ayat
    text_re = re.search("^[0-9]+:[0-9]+$", text)

    # first, we separate the input, is it a command or not
    if text[0] == "/":
        # It is a command input
        command = text[1:].lower()
        if command == "start":
            nama = message['message']['from']['first_name']
            # save chat id
            save_chat_id(chat_id)
            reply = start(nama)
            send_no_button(chat_id, reply)
        elif command == "help":
            reply = help()
            send_no_button(chat_id, reply)
        elif command == "info":
            reply = info()
            send_no_button(chat_id, reply)
        elif command == "acak":
            reply = acak()
            send_with_button(chat_id, reply)
        else:
            reply = "Maaf perintah tidak dikenali"
            send_no_button(chat_id, reply)


    elif text_re: # if the input format is True
        # we split the text input into number of surah and number of ayat
        no_surah, no_ayat = text.split(":")

        # make sure number of surah is valid
        if int(no_surah) > 0 and int(no_surah) <= 114:

            # after that, make sure the number of ayat is valid by accessing the data
            file_path = DIR + "/bot/json/{}.json".format(no_surah)

            with open(file_path, "r", encoding="utf8") as datafile:
                data = json.loads(datafile.read())
                data_surah = data["data"]
                jumlah_ayat = data_surah["numberOfVerses"]
                nama_surah = data_surah["name"]['transliteration']['id']

            if int(no_ayat) > 0 and int(no_ayat) <= jumlah_ayat:
                data_ayat = data_surah["verses"][int(no_ayat)-1]
                arab = data_ayat["text"]["arab"]
                indo = data_ayat["translation"]["id"]

                text = "{}\n{}\nQ.S {} [{}:{}]".format(arab, indo, nama_surah, no_surah, no_ayat)
                first = True if int(no_ayat) == 1 else False
                last = True if int(no_ayat) == jumlah_ayat else False
                send_with_button(chat_id, text, first, last)

            else:
                err = "Maaf, surah {} tidak memiliki ayat {}".format(nama_surah, no_ayat)

        else:
            err = "Sepertinya anda typo, ingatlah kalau Al-Qur'an hanya punya 114 surah"

    else:
        err = "Maaf, input tidak valid. Gunakan /help untuk bantuan"

    if err is not None:
        send_no_button(chat_id, err)



def answer_callback(callback_id):
    url = "https://api.telegram.org/bot{}/answerCallbackQuery".format(TOKEN_BOT)
    payload = {
        'callback_query_id':callback_id
    }

    requests.post(url, json=payload)


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        update = request.get_json()

        # check if the request is callback query
        if "callback_query" in update:
            cb_query = update['callback_query']
            cb_query_id = cb_query['id']
            query_data = cb_query["data"]
            answer_callback(cb_query_id)
            callback_process(cb_query, query_data)
        else:
            update_process(update)

        return Response('ok', status=200)

    else:
        return "TELEGRAM BOT SEDANG BERJALAN"

if __name__ == "__main__":
    app.run()