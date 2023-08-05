from googlesearch import search
import requests
import bs4

qlyrics = " lklyrics"
qmp3 = " ananmanan"
b = []
c = []

def songs(query):
    for i in search(query + qmp3, tld="com", num=10, stop=10, pause=1):
        if "ananmanan" in i:
            c.append(i)
    try:
        mp = requests.get(c[0]).text
        print("[*]Getting Information on mp3....")
        id = str(c[0]).split("song/")[1].split("/")[0]
        link = requests.get("https://www.ananmanan.lk/free-sinhala-mp3/download.php?id=" + str(id)).url
        name = (str(c[0]).split(".html")[0].split("/")[-1].replace("-", " "))
        down = requests.get(url=link, stream=True)
        from tqdm import tqdm
        print("[*]Downloading MP3..............")
        size = float(down.headers['content-length'])
        with open(name + ".mp3", "wb") as f:
            for chunk in tqdm(iterable=down.iter_content(1024),unit='KB',total=size/1024,desc="Downloading :"):
                f.write(chunk)
        print("[*]Download Completed")


    except:
        print("[*]MP3 downloading error")
        print("[*]Try again with different query")
def lyrics(query):
    for i in search(query + qlyrics, tld="com", num=10, stop=10, pause=1):
        if "lklyrics" in i:
            b.append(i)

    try:
        ly = requests.get(b[0]).text
        print("[*]Getting Information lyrics....")
        soup = bs4.BeautifulSoup(ly, "lxml")
        ss = (soup.find_all("img")[1])
        lylink = str(ss).split('src="')[1].split('"')[0]
        lylink = requests.get(lylink, stream=True)
        print("[*]Downloading Lyrics.................")
        size = float(lylink.headers['content-length'])
        from tqdm import tqdm
        pbar = tqdm(iterable=lylink.iter_content(1024),unit='KB',total=size/1024,desc="Downloading :")
        import time
        with open(query+".png", "wb") as f:
            for chunk in pbar:
                f.write(chunk)
        print("[*]Download Completed")


    except:
        print("[*]Lyrics downloading error")
        print("[*]Try again with another query")
