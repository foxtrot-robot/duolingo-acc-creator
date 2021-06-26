try:
    import random
    from selenium import webdriver
    import time
    import random2
    import requests
    import sys
    import json

    with open("config.json", "r") as f:
        config = json.load(f)
        # Config values
        download_wordlists = config.get('download-wordlists')
        invite_url = config.get('invite-url')
        selenium_driver_path = config.get('selenium-driver-path')

except:
    command = "pip3 install -r requirements.txt"
    print(f"Please execute this command in your shell: {command}")

# these two functions are for download needed wordlists.
def download_usernames():
    url = r"https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/xato-net-10-million-usernames-dup.txt"
    r = requests.get(url, allow_redirects=True)
    open('usernames.txt', 'wb').write(r.content)
    time.sleep(10)
def download_passwords():
    url = r"https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/xato-net-10-million-passwords-100000.txt"
    r = requests.get(url, allow_redirects=True)
    open('passwords.txt', 'wb').write(r.content)
    time.sleep(10)
def gen_password():
    with open("passwords.txt", "r") as file:
        text = file.read()
        words = list(map(str, text.split()))
        generated_password = random.choice(words)
        return generated_password
def fake_email():
    with open("usernames.txt", "r") as file:
        text = file.read()
        words = list(map(str, text.split()))
        generated_email = random.choice(words) + "@gmail.com"

        return generated_email
def selenium_work():
    try:
        global driver
        driver = webdriver.Firefox(executable_path=selenium_driver_path)

        driver.get(invite_url)

        language = driver.find_element_by_css_selector("a.uS_Xr:nth-child(1) > div:nth-child(1)").click()
        time.sleep(5)

        exitlesson = driver.find_element_by_class_name("fCAG0").click()

        time.sleep(3)

        create_profile = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[2]/div/div/div[1]/div[2]/button[1]").click()

        age = driver.find_element_by_css_selector(
            "div._2a3s4:nth-child(1) > label:nth-child(1) > div:nth-child(1) > input:nth-child(1)")
        age.click()
        generated_age = random2.randint(18, 50)
        age.send_keys(generated_age)

        email = driver.find_element_by_css_selector(
            "div._2a3s4:nth-child(3) > label:nth-child(1) > div:nth-child(1) > input:nth-child(1)")
        email.click()

        email.send_keys(fake_email())

        password = driver.find_element_by_css_selector(
            "div._2a3s4:nth-child(4) > label:nth-child(1) > div:nth-child(1) > input:nth-child(1)")
        password.click()
        password.send_keys(gen_password())
        time.sleep(2)

        finish_button = driver.find_element_by_xpath("/html/body/div[2]/div[5]/div/div/form/div[1]/button")
        finish_button.click()

        print("Account registered succesfully!")

        driver.__exit__()
        selenium_work()
    except:
        print("Oops!", sys.exc_info()[0], ".")
        driver.__exit__()
        selenium_work()

if __name__ == "__main__":
    if download_wordlists == "true":
        print("Downloading email wordlist...")
        download_usernames()
        print("Downloaded email wordlist succesfully!")
        time.sleep(10)
        print("Downloading password wordlist...")
        download_passwords()
        print("Downloaded password wordlist succesfully!")
        time.sleep(10)

        print("Loading main function!")
        selenium_work()
    else:
        print("Loading main function...")
        selenium_work()