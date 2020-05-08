from pytube import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from threading import *

file_size = 0




def startDownload():
    global file_size
    try:
        url = urlField.get()
        print(url)
        btn.config(text='Please wait...')
        btn.config(state=DISABLED)

        path = askdirectory()
        print(path)
        if path is None:
            return

        ob = YouTube(url)
        # strms = ob.streams.all()
        # for s in strms:
        #    print(s)
        strm = ob.streams.first()

        vTitle.config(text=strm.title)
        vTitle.pack(side=TOP)

        print(file_size)
        strm.download(path)
        print("Done")
        btn.config(text='Done')
        btn.config(text='start Download')
        btn.config(state=NORMAL)
        showinfo("Download Finished", "Downloaded Successfully")
        urlField.delete(0, END)
        vTitle.pack_forget()
    except Exception as e:
        print(e)
        print("Error")


def startDownloadThread():
    thread = Thread(target=startDownload)
    thread.start()


main = Tk()
main.title("My Youtube Downloader")
main.iconbitmap('yt_downloader_prem.ico')

main.geometry("500x600")
file = PhotoImage(file='yt_downloader_prem.png')
headingIcon = Label(main, image=file)
headingIcon.pack(side=TOP)

urlField = Entry(main, justify=CENTER)
urlField.pack(side=TOP, fill=X, padx=10)

btn = Button(main, text="Start Download", relief='ridge', command=startDownloadThread)
btn.pack(side=TOP, pady=10)

vTitle = Label(main, text="video title")
# vTitle.pack(side=TOP)


main.mainloop()
