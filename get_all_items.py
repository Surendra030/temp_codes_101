import json
import requests
from bs4 import BeautifulSoup
import time
from decrypt import decrypt_json
import os
from mega import Mega

data = decrypt_json('doy.json','key000')

start = 201
end = 301
base = 'https://project-get-source-code-1.vercel.app/?url='
data =data[start:end]

results = []

try:
    data1 = []

    for index,obj in enumerate(data):
        print(f"{index}/{len(data)}")
        try:
            url = obj['link']
            pages = int(obj['page'])
            anchors = []
            for page  in  range(pages):
                print(f"{page}/{pages}")
                full_url = f"{base}{url}/{page+1}"
                
                res = requests.get(full_url)
                if res.status_code == 200:
                    # Parse the JSON response
                    data = res.json()
                    
                    # Extract the HTML content from the 'html' key
                    html_content = data.get("html", "")
                    
                    # Use BeautifulSoup to parse the HTML content
                    # Parse the HTML
                    soup = BeautifulSoup(html_content, "html.parser")

                    lst = soup.find_all(class_="thumb-under")

                    for i in lst:
                        an = i.find("a")  # Find the <a> tag inside the element
                        if an:
                            anchor = str(an)
                            
                            anchors.append(anchor)  # Append both href and text to the data list
                        
                                
                else:
                    print(f"Failed to retrieve the page. Status code: {res.status_code}")
            obj={
                'link':url,
                'anchors_data':anchors
            }
            data1.append(obj)
        except Exception as e:
            print("error : ",e)
        time.sleep(4)

except Exception as e:
    print("Error : ",e)


finally:
    file_name = f'{end}_updated.json'
    with open(file_name,'w')as f:
        json.dump(data1,f,indent=4)

    keys = os.getenv("M_TOKEN")
    keys = keys.split("_")
    mega = Mega()
    m  = mega.login(keys[0],keys[1])

    try:
        m.upload(file_name)
    except  Exception as e:
        print("Err : ",e)
