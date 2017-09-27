from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
import time


proxy_file = open('proxies.txt', 'r')


def get_proxy(line_num):
    if not proxy_file.closed:
        proxy_file.seek(line_num)
        return proxy_file.readline()


def get_profile():

    p_host = str(get_proxy(line_num=current_line).split(':')[0])
    p_port = int(get_proxy(line_num=current_line).split(':')[1])

    f_profile = webdriver.FirefoxProfile()

    f_profile.set_preference("browser.privatebrowsing.autostart", True)
    f_profile.set_preference('network.proxy.type', 1)
    f_profile.set_preference('network.proxy.http', p_host)
    f_profile.set_preference('network.proxy.http_port', p_port)
    f_profile.set_preference('network.proxy.ssl', p_host)
    f_profile.set_preference('network.proxy.ssl_port', p_port)

    return f_profile


def load_page():
    driver = webdriver.Firefox(firefox_profile=get_profile())

    driver.get("http://whatismyipaddress.com")


def proxy_file_length():

    a = proxy_file.read()

    return a.count('\n')

my_link = str(raw_input("Enter your link: "))

current_line = 0

proxy_file.seek(0)

while not current_line == proxy_file_length() + 1:

    print "Current Proxy: ", get_proxy(line_num=current_line)

    print "Now opening the url!"

    print get_proxy(line_num=current_line).split(':')[0]
    print get_proxy(line_num=current_line).split(':')[1]

    try:
        driver = webdriver.Firefox(firefox_profile=get_profile())

        driver.get(my_link)

        wait = WebDriverWait(driver=driver, timeout=10)

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "video-stream html5-main-video")))

    except TimeoutException as t_e:
        print "Something went wrong! Error: ", t_e
        driver.quit()

    except WebDriverException as w_e:
        print "Proxy is probably dead! Error: ", w_e
        driver.quit()

    finally:
        driver.quit()

    time.sleep(5)

    current_line += 1

proxy_file.close()








