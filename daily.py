from selenium.webdriver.support import wait
from wabott import WhatsApp
import csv
from datetime import datetime as date

# Initializing
today = date.today().strftime("%A")
tanggal = date.today().strftime("%d")
print(tanggal)
app = WhatsApp(100)
app.override_timeout(30)

# Data Collection
participants = app.get_group_participants("Test")

messageDaily = """
1. Haloo, bagaimana kabarnya hari ini? Jangan lupa berdoa sebelum belajar yaaa
2. Bagaimana suasana kelas hari ini? Menyenangkan bukan?
3. Bagaimana aktivitas belajarnya hari ini? Apakah menyenangkan?
4. Untuk hari ini, apakah kamu semangat mengikuti pelajaran? Seberapa semangat kamu untuk hari ini

Dijawab dengan nilai 1-4 (dimana 1 tidak baik dan 4 sangat baik)
Jawabannya tanpa diberi spasi yaa, misalnya seperti ini: 3243
"""

messageWeekly = """
1. Bagaimana semangat belajar dalam 1 minggu ini?
2. Apakah sekolah dalam sepekan ini menyenangkan?
3. Apakah kamu memahami pelajaran dalam sepekan ini?
"""
replieds = app.unread_usernames(scrolls=50)
penjawabs = replieds.intersection(participants)
semuaJawaban = []

# Receive result
if today == "Monday":
    jawaban = []
    for penjawab in penjawabs:
        jawaban.append(penjawab)
        jawaban.append(app.get_last_message_for(penjawab))
        jawaban.append("w")
        jawaban.append(tanggal)
        semuaJawaban.append(jawaban)
else:
    jawaban = []
    for penjawab in penjawabs:
        jawaban.append(penjawab)
        jawaban.append(app.get_last_message_for(penjawab))
        jawaban.append("d")
        jawaban.append(tanggal)
        semuaJawaban.append(jawaban)

# Write Result
with open('result.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(semuaJawaban)

# Send Message
if today == "Saturday":
    for participant in participants:
        try:
            app.send_message(participant.strip(), messageWeekly)
        except Exception as e:
            participant = participant.replace("+", "")
            participant = participant.replace(" ", "")
            app.send_anon_message(participant.strip(), messageWeekly)
        app.goto_main()

elif today == "Sunday":
    pass
else:
    for participant in participants:
        try:
            app.send_message(participant.strip(), messageDaily)
        except Exception as e:
            participant = participant.replace("+", "")
            participant = participant.replace(" ", "")
            app.send_anon_message(participant.strip(), messageWeekly)
        app.goto_main()