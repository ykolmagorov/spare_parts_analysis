#import imaplib

import ssl
import certifi
from imapclient import IMAPClient
from email.header import decode_header
from email import message_from_bytes
from io import BytesIO
import pandas as pd

def decode_header_value(value):
    result = ""

    for part, encoding in decode_header(value):
        if isinstance(part, bytes):
            result += part.decode(encoding or "utf-8")
        else:
            result += part

    return result

import os
from dotenv import load_dotenv

load_dotenv("yandex.env")

def get_price_profit():

    email = "avtoberloga92@yandex.ru"
    token = os.getenv("YANDEX_MAIL_avtoberloga92_TOKEN")

    '''mail = imaplib.IMAP4_SSL("imap.yandex.ru", 993)

    auth_string = f"user={email}\1auth=Bearer {token}\1\1"

    mail.authenticate("XOAUTH2", lambda x: auth_string)

    print("Авторизация успешна")'''

    #получаем данные о входящих
    '''status, data = mail.select("INBOX")

    print(status)
    print(data)

    status, data = mail.search(None, 'ALL')

    email_ids = data[0].split()

    print(status)
    print("Количество писем:", len(email_ids))'''

    #получаем список папок
    '''status, folders = mail.list()

    print(status)

    for folder in folders:
        print(folder.decode())'''

    ssl_context = ssl.create_default_context(
        cafile=certifi.where()
    )

    mail = IMAPClient(
        "imap.yandex.ru",
        ssl=True,
        ssl_context=ssl_context
    )

    mail.oauth2_login(email, token)

    print("Авторизация успешна")

    folders = mail.list_folders()

    found_messages = []

    for folder in folders:
        folder_name = folder[2]

        print("Ищем в:", folder_name)

        mail.select_folder(folder_name)

        messages = mail.search([
        "FROM", "robot@pr-lg.ru"
        ,"SUBJECT", "прайс-лист ПрофитЛига склад СИМФЕРОПОЛЬ"
        ], charset="UTF-8")

        if messages:
            # Получаем дату каждого найденного письма
            data = mail.fetch(messages, ["INTERNALDATE"])
            for message_id, message_data in data.items():
                found_messages.append(
                    (
                        folder_name,
                        message_id,
                        message_data[b"INTERNALDATE"]
                    )
                )

            latest = max(found_messages, key=lambda x: x[2])
            print("Самое свежее письмо:")
            print("Папка:", latest[0])
            print("ID:", latest[1])
            print("Дата:", latest[2])
            break
        

    #print(data)

    '''print("Всего найдено:", len(found_messages))

    for folder_name, message_id in found_messages:
        print(folder_name, message_id)'''

    mail.select_folder(latest[0])

    message = mail.fetch(
        [latest[1]],
        ["RFC822"]
    )

    raw_message = message[latest[1]][b"RFC822"]

    email_message = message_from_bytes(raw_message)

    '''print("Отправитель:", email_message["From"])
    print("Тема:", email_message["Subject"])
    print("Дата:", email_message["Date"])'''

    for part in email_message.walk():

        if part.get_content_type() == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":

            filename = part.get_filename()
            filename = decode_header_value(filename)
            print("Имя файла:", filename)
            if filename and filename.startswith('ПрофитЛига ПРАЙС-ЛИСТ'):
                print("Нашли нужный файл")
                file_data = part.get_payload(decode=True)
                df = pd.read_excel(BytesIO(file_data))
                #print(df)
    return df