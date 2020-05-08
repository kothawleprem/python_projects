import requests
import bs4
import tkinter as tk
import plyer
import time
import datetime
import threading

def get_html_data(url):
    data = requests.get(url)
    return data

def get_corona_detail():
    url = "https://www.mohfw.gov.in/"
    html_data=get_html_data(url)
    #print(html_data.text)
    bs = bs4.BeautifulSoup(html_data.text,'html.parser')
    stats_div = bs.find("div",class_="site-stats-count").find_all("li")
    all_details = ""
    for block in stats_div:
        try:
            count = block.find("strong").get_text()
            text = block.find("span").get_text()
            all_details = all_details + text + " : " + count + "\n"
        except:
            break
    return all_details

def refresh():
    ref_data = get_corona_detail()
    print("Refreshing...")
    mainlabel['text'] =ref_data

def notify():
    while True:
        plyer.notification.notify(
        title="Covid-19 cases of INDIA",
        message=get_corona_detail(),
        timeout=10,
        app_icon='images (1).ico'
        )
        time.sleep(10800)

print(get_corona_detail())

root = tk.Tk()

root.geometry("900x800")
root.iconbitmap("images (1).ico")
root.title("Corona Stats Tracker - India")
root.configure(background="white")
f=("poppins",25,"bold")
f1=("poppins",10,"italic")

img = tk.PhotoImage(file="images.png")
imgLabel = tk.Label(root,image=img)
imgLabel.pack()

mainlabel=tk.Label(root,text = get_corona_detail(), font=f,bg="white")
mainlabel.pack()




ref=tk.Button(root,text="Refresh",font=f,relief='solid', command=refresh)
ref.pack()

clabel=tk.Label(root,text = "BY PSK", font=f1,bg="white")
clabel.pack(side="bottom", anchor="ne")

th1 = threading.Thread(target=notify)
th1.setDaemon(True)
th1.start()

root.mainloop()
