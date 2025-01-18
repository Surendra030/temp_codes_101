
from mega import Mega
import json
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os


options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
options.add_argument("--headless") 
options.add_argument("--disable-notifications")
options.add_argument("--disable-blink-features=AutomationControlled")

chromedriver_path = r"chromedriver"


with open("file_path.json",'r',encoding='utf-8')as f:
    data = json.load(f)



   
def update_file_data(f_name):

    keys = os.getenv("M_TOKEN")
    keys = keys.split("_")

    mega = Mega()
    m = mega.login(keys[0],keys[1])
    try:
        m.upload(f_name)
        return True
    except Exception as e:
        print("Error failed to upload..")




v1 = os.getenv("START")
v = os.getenv('END')

start = int(v1)
end = int(v)

print(f"start : {start}/ end :{end}")
data = data[start:end]


result = []
continue_flag = False
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)


try:
    for index,url in enumerate(data):

        if index%100 ==0:
            driver.quit()
            print("waiting for 10 sec..")
            time.sleep(10)

            service = Service(executable_path=chromedriver_path)
            driver = webdriver.Chrome(service=service, options=options)

        print(f"index : {index} / {len(data)}")
        driver.get(url)
        time.sleep(2)
        anchors = driver.find_elements(By.TAG_NAME, "a")
        temp_lst  = []
        count = 0
        if len(anchors) < 0: continue

        for anchor in anchors:
            href = anchor.get_attribute('href')  # Get the href attribute
            img = anchor.find_element(By.TAG_NAME, "img") if anchor.find_elements(By.TAG_NAME, "img") else None
            title = img.get_attribute('title') if img else None
            text = anchor.text.strip()  # Get the text content of the <a> tag
            
            # Only include items with href
            if href and '/chapter/' in href:
                count +=1
                obj = {
                    'href': href,
                    'text': text,
                    'title': title
                }
                temp_lst.append(obj) 
                

        obj = {
            'index':index,
            'url':url,
            'anchors_len':count,
            'data':temp_lst
        }

        result.append(obj)
        end = index


    continue_flag = True

except Exception as e:
    print("Error : ",e)
finally:
    f_name = f"{end}_manga_data.json"
    with open(f_name, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4)
    
    flag = update_file_data(f_name)
    if flag:
        print("Files uploaded successfully...")
    else:
        print("Files not uploaded...")
