import csv
import matplotlib.pyplot as plt
from wabott import WhatsApp
import os

app = WhatsApp(100)
app.override_timeout(30)

def moving_average(numbers):
    i = 0
    moving_averages = []
    moving_averages.append(numbers[0])
    moving_averages.append((numbers[0]+numbers[1])/2)
    moving_averages.append((numbers[0]+numbers[1]+numbers[2])/3)

    while i < len(numbers) - 3:
        this_window = numbers[i : i + 4]

        window_average = sum(this_window) / 4
        moving_averages.append(window_average)
        i += 1
    return moving_averages

# Data Collection
with open('result.csv',"w+", newline='') as f:
    reader = csv.reader(f)
    data = sorted(list(reader), key=lambda x: x[0])

result={}
for li in data:
    result.setdefault(li[0], []).append(li[1:])

# Processing
for key, value in result.items():
    x = [a[-1] for a in value]
    temp = [a[0] for a in value]
    mood = []
    htb = []
    for e in temp:
        k = [int(i) for i in e]
        mood.append(k[0]+k[1])
        htb.append(k[2]+k[3])
    moodMA = moving_average(mood)
    print(moodMA)
    print(mood)
    plt.title(key)
    plt.ylim(0,8)
    plt.plot(x, mood, label = "Mood")
    plt.plot(x, htb, label = "HTB")
    plt.plot(x, moodMA, label = "MoodMA")
    plt.legend()
    plt.savefig(f'{key}.png', bbox_inches='tight')
    plt.close()
    app.send_picture(key, os.getcwd()+f"/{key}.jpg")
    os.remove(os.getcwd()+f"/{key}.jpg")