from mega import Mega

def fetch_m():
        
    keys = 'afg154010@gmail.com_megaMac02335!'.split("_")
    mega = Mega()
    m = mega.login(keys[0],keys[1])

    return m if m else None