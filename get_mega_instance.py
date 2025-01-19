import os
import subprocess
from mega import Mega



def fetch_m():
        

    keys = os.getenv("M_TOKEN")
    keys = keys.split("_")
    mega  = Mega()
    keys[0] = keys[0].replace('6@','8@')
    m = mega.login(keys[0],keys[1])
    return m