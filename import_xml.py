import re
from download_email_prices import get_price_profit
from download_prices import get_price_mikado

pr_lg = get_price_profit()
mikado = get_price_mikado('https://polomkam.net/api/Price/GetPriceExcel?StockId=92&Key=E0162337-649E-42A7-B547-6A818BDD3055')

'''print(mikado.head())
print(pr_lg.head())

print(pr_lg.columns)
print(mikado.columns)'''

#приводим артикул в разных прайсах к единому виду
def normalize_oem(oem):
    oem = str(oem).upper()

    for symbol in ('-', '.', ' '):
        oem = oem.replace(symbol, '')

    return oem

# обработка прайса Профит-Лиги
def load_price_profit(pr_lg, price_list):

    for _, dt in pr_lg.iterrows():
        brand = dt['Номенклатура.Производитель']
        oem = normalize_oem(dt['Артикул'])
        key = (brand.upper().strip(),oem)
        price = int(dt['Цена'])

        if price >2000:
            price = round(price*1.23,-1)
        else:
            price = round(price*1.25,-1) 

        qty = int(dt['В наличии остаток'])
        if key not in price_list:
            price_list[key] = {
                'price': price,
                'qty': qty
            }
        elif price < price_list[key]['price']:
            price_list[key]['price'] = price
            price_list[key]['qty'] = qty

    return price_list

# обработка прайса Профит-Лиги
def load_price_mikado(mikado, price_list):

    for _,dt in mikado.iterrows():
        brand = dt['BrandName']
        oem = normalize_oem(dt['Code'])
        key = (brand.upper().strip(),oem)
        price = int(float(dt['PriceOut']))

        if price > 2000:
            price = round(price*1.23,-1)
        else:
            price = round(price*1.25,-1)
        
        qty = int(dt['QTY'].replace('>',''))
        if key not in price_list:
            price_list[key] = {
                'price': price,
                'qty': qty
            }
        elif price < price_list[key]['price']:
            price_list[key]['price'] = price
            price_list[key]['qty'] = qty
    return price_list        

price_list = {}
load_price_profit(pr_lg,price_list)
load_price_mikado(mikado,price_list)

import xml.etree.ElementTree as ET
import copy

old_tree = ET.parse('articles.xml')
old_root = old_tree.getroot()

new_root = ET.Element(old_root.tag)

updated = 0

ads = old_root.findall('Ad')
for ad in ads:
    oem = ad.find('OEM')
    brand = ad.find('Brand')
    if oem is None or brand is None:
        continue
    key = (
        brand.text.upper().strip(),
        normalize_oem(oem.text)
    )

    if key in price_list:
        new_ad = copy.deepcopy(ad)
        data = price_list[key]
        price = new_ad.find('Price')
        if price is not None:
            price.text = str(data["price"])  
            new_root.append(new_ad)
            updated += 1
        
new_tree = ET.ElementTree(new_root)

new_tree.write(
    "new_articles.xml",
    encoding="utf-8",
    xml_declaration=True
)

print('Обновлено: ', updated,' строк')

from upload_yandex import upload_to_yandex_disk

upload_to_yandex_disk("new_articles.xml")