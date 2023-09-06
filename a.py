import time
import warnings
import threading

from faker import Faker
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec



proxylist = [
    "192.99.101.142:7497",
    "198.50.198.93:3128",
    "52.188.106.163:3128",
    "20.84.57.125:3128",
    "172.104.13.32:7497",
    "172.104.14.65:7497",
    "165.225.220.241:10605",
    "165.225.208.84:10605",
    "165.225.39.90:10605",
    "165.225.208.243:10012",
    "172.104.20.199:7497",
    "165.225.220.251:80",
    "34.110.251.255:80",
    "159.89.49.172:7497",
    "165.225.208.178:80",
    "205.251.66.56:7497",
    "139.177.203.215:3128",
    "64.235.204.107:3128",
    "165.225.38.68:10605",
    "165.225.56.49:10605",
    "136.226.75.13:10605",
    "136.226.75.35:10605",
    "165.225.56.50:10605",
    "165.225.56.127:10605",
    "208.52.166.96:5555",
    "104.129.194.159:443",
    "104.129.194.161:443",
    "165.225.8.78:10458",
    "5.161.93.53:1080",
    "165.225.8.100:10605",
]

warnings.filterwarnings('ignore')
fake = Faker('en_IN')
MUTEX = threading.Lock()


def sync_print(text):
    with MUTEX:
        print(text)

def get_driver(proxy):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.headless = True
#    options.binary_location = "/usr/lib/chromium-browser/chromedriver"
    options.add_argument(f'user-agent={user_agent}')
    options.add_experimental_option("detach", True)
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-dev-shm-usage')
    #options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    #options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    #options.add_argument("--use-fake-ui-for-media-stream")
    #options.add_argument("--use-fake-device-for-media-stream")
    options.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1
  })
    if proxy is not None:
        options.add_argument(f"--proxy-server={proxy}")
    driver = webdriver.Chrome("chromedriver" ,options=options)
    return driver


def driver_wait(driver, locator, by, secs=10, condition=ec.element_to_be_clickable):
    wait = WebDriverWait(driver=driver, timeout=secs)
    element = wait.until(condition((by, locator)))
    return element


def start(name, proxy, user, wait_time):
    sync_print(f"{name} started!")
    driver = get_driver(proxy)
    driver.get(f'https://zoom.us/wc/join/'+meetingcode)
    driver.execute_script("navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => { console.log(stream) }).catch(error => { console.log(error) });")
    time.sleep(3)
    inp = driver.find_element(By.ID, 'inputname')
    time.sleep(1)
    inp.send_keys(f"{user}")
    time.sleep(2)

    inp2 = driver.find_element(By.ID, 'inputpasscode')
    time.sleep(1)
    inp2.send_keys(passcode)
    btn3 = driver.find_element(By.ID, 'joinBtn')
    time.sleep(1)
    btn3.click()
    time.sleep(5)
    btn3 = driver.find_element(By.ID, 'preview-audio-control-button').click()
    
    #WebDriverWait(driver, 10).until( ec.presence_of_element_located((By.XPATH,'//*[@id="preview-audio-control-button"]'))).click()
    #time.sleep(3)
    WebDriverWait(driver, 10).until( ec.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div[1]/button'))).click()
    time.sleep(5)
    try:
      WebDriverWait(driver, 10).until( ec.presence_of_element_located((By.XPATH,'/html/body/div[14]/div/div/div/div[2]/div/div/button'))).click()
    except:
      pass
      
    WebDriverWait(driver, 10).until( ec.presence_of_element_located((By.XPATH,'//*[@id="voip-tab"]/div/button'))).click()
    sync_print(f"{name} sleep for {wait_time} seconds ...")
    time.sleep(wait_time)
    sync_print(f"{name} ended!")


def main():
    wait_time = sec * 60
    workers = []
    for i in range(number):
        try:
            proxy = proxylist[i]
        except Exception:
            proxy = None
        try:
            user = fake.name()
        except IndexError:
            break
        wk = threading.Thread(target=start, args=(
            f'[Thread{i}]', proxy, user, wait_time))
        workers.append(wk)
    for wk in workers:
        wk.start()
    for wk in workers:
        wk.join()


if __name__ == '__main__':
    number = int(input("Enter number of Users: "))
    meetingcode = input("Enter meeting code (No Space): ")
    passcode = input("Enter Password (No Space): ")
    sec = 5
    main()
