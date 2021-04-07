import requests
from bs4 import BeautifulSoup 
import tkinter as tk
import plyer
import time
import datetime
import threading


def get_corona_detail():
    html_text = requests.get('https://www.mygov.in/covid-19').text
    soup = BeautifulSoup(html_text,'lxml')
    info_block = soup.find_all('div',class_='information_block')
    all_details = ""
    total_vaccinated = ""
    total_vaccinated_day_before = ""
    total_cases = ""
    total_active = ""
    total_discharged = ""
    total_deaths = ""
    for blocks in info_block:
        # Currently in information block
        vac_block = blocks.find_all('div',class_='vaccination-block')
        for v_block in vac_block:
            # Currently in Vaccination-block
            vac_view = v_block.find_all('div',class_='vaccinated-view')
            for v_view in vac_view:
                # Currently in Vaccinated-view fetching from total-vcount
                vac_count = list(map(str, (v_view.find('div', class_='total-vcount').text).split(" ")))
                total_vaccinated = vac_count[0]
            for v2_view in vac_view:
                # Currently in Vaccinated-view fetching from yday-vcount
                vac_count_day = list(map(str, (v2_view.find('div', class_='yday-vcount').text).split(" ")))
                total_vaccinated_day_before = vac_count_day[0]
        info_row = blocks.find_all('div',class_='information_row')
        for block in info_row:
            case_block = block.find_all('div',class_='iblock t_case')
            for data in case_block:
                total_cases = data.find('span', class_='icount').get_text()
            active_block = block.find_all('div',class_='iblock active-case')
            for data in active_block:
                total_active = data.find('span', class_='icount').get_text()
            discharge_block = block.find_all('div',class_='iblock discharge')
            for data in discharge_block:
                total_discharged = data.find('span', class_='icount').get_text()
            death_block = block.find_all('div',class_='iblock death_case')
            for data in death_block:
                total_deaths = data.find('span', class_='icount').get_text()

    
    all_details = f"Total Vaccinated: {total_vaccinated} \nTotal Vaccinated Day Before:{total_vaccinated_day_before} \nTotal Cases:{total_cases} \nTotal Active:{total_active} \nTotal Discharged:{total_discharged} \nTotal Death:{total_deaths}"

    return all_details

def refresh():
    ref_data = get_corona_detail()
    print("Refreshing...")
    print(get_corona_detail())
    mainlabel['text'] =ref_data

def notify():
    while True:
        plyer.notification.notify(
        title="Covid-19 cases of INDIA",
        message=get_corona_detail(),
        timeout=10,
        app_icon='images (1).ico'
        )
        time.sleep(20) # Specifies the time after which it should notify

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

clabel=tk.Label(root, font=f1,bg="white")
clabel.pack(side="bottom", anchor="ne")

th1 = threading.Thread(target=notify)
th1.setDaemon(True)
th1.start()

root.mainloop()
