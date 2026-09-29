import os
import time

import yadisk
from dotenv import load_dotenv

load_dotenv('yandex.env')

TOKEN = os.getenv("YANDEX_DISK_y.kolmagorov_TOKEN")
if TOKEN is None:
    raise RuntimeError(
        "YANDEX_DISK_y.kolmagorov_TOKEN не найден в yandex.env"
    )

def upload_to_yandex_disk (filename):

    print("Начинаем загрузку...")
    start = time.time()

    with yadisk.Client(token=TOKEN) as disk:
        disk.upload(
            filename,
            f"Автоберлога/Автозагрузка Авито/{filename}",
            overwrite=True,
            spoof_user_agent=True,
            timeout=600
        )

    elapsed = time.time() - start

    print(f"Загрузка заняла: {elapsed:.1f} сек.")
    print(f"Файл {filename} загружен на Яндекс Диск")
