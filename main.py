from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
import time


def get_proxy(line_num):

    with open("proxies.txt", 'r') as proxy_file:
        for line, proxy in enumerate(proxy_file):
            if line == line_num-1:
                return proxy


class OpenBrowser:

    def __init__(self, url):
        self.url = url

    def chrome_option(self):

        proxy = get_proxy(line_num=current_line)

        option = webdriver.ChromeOptions()

        option.add_argument("--incognito")
        option.add_argument("--proxy-server=http://%s" % proxy)

    def open_chrome(self):

        driver = webdriver.Chrome(executable_path='drivers/chromedriver.exe', chrome_options=self.chrome_option())

        try:

            driver.get(url=self.url)

            try:
                wait = WebDriverWait(driver=driver, timeout=15)

                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "video-stream html5-main-video")))

            except TimeoutException as t_e:
                print "Page load time out!\nError: ", t_e
                driver.quit()

            except WebDriverException as w_e:
                print "Proxy is probably dead!\nError: ", w_e
                driver.quit()

        except Exception, e:
            print "Something went wrong while loading firefox!\nError: ", e

        finally:
            driver.quit()

    def firefox_profile(self):

        p_host = str(get_proxy(line_num=current_line).split(':')[0])
        p_port = int(get_proxy(line_num=current_line).split(':')[1])

        f_profile = webdriver.FirefoxProfile()

        f_profile.set_preference("browser.privatebrowsing.autostart", True)
        f_profile.set_preference('network.proxy.type', 1)
        f_profile.set_preference('network.proxy.http', p_host)
        f_profile.set_preference('network.proxy.http_port', p_port)
        f_profile.set_preference('network.proxy.ssl', p_host)
        f_profile.set_preference('network.proxy.ssl_port', p_port)
        f_profile.set_preference('http.response.timeout', 10)

        return f_profile

    def open_firefox(self):

        driver = webdriver.Firefox(executable_path=r'firefox_driver\geckodriver.exe', firefox_profile=self.firefox_profile())

        try:

            driver.get(url=self.url)

            try:

                wait = WebDriverWait(driver=driver, timeout=10)

                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "video-stream html5-main-video")))

            except TimeoutException as t_e:
                print "Something went wrong! Error: ", t_e
                driver.quit()

            except WebDriverException as w_e:
                print "Proxy is probably dead! Error: ", w_e
                driver.quit()

        except Exception, e:
            print "Something went wrong while loading firefox!\nError: ", e

        finally:
            driver.quit()


def select_browser():

    print "Select your browser. Press num key:"
    while True:
        try:
            browser_name = int(raw_input("'1' Firefox\n'2' Chrome\nEnter you choice: "))

        except ValueError:
            print "UhhOhh! Please enter only integer, Try again!"
            continue
        else:
            break
    if browser_name == 1:
        print "You selected Firefox browser!\n"
    else:
        print "You selected Chrome browser!\n"
    return browser_name


def proxy_file_length():

    with open("proxies.txt", "r") as proxy_file:
        a = proxy_file.read()
        return a.count('\n')

my_link = str(raw_input("Enter your YouTube link: "))

current_line = 1

myYoutube = OpenBrowser(url=my_link)

if select_browser() == 1:
    while not current_line == proxy_file_length() + 1:
        print "Entered loop.... test"
        print "Current Proxy: ", get_proxy(line_num=current_line)

        print "Now opening the url!"

        myYoutube.open_firefox()

        time.sleep(1)

        current_line += 1

else:

    while not current_line == proxy_file_length() + 1:

        print "Entered loop.... test"
        print "Current Proxy: ", get_proxy(line_num=current_line)

        print "Now opening the url!"

        myYoutube.open_chrome()

        time.sleep(1)

        current_line += 1
