import requests
from io import BytesIO
import pandas as pd

def get_price_mikado(url):

    response = requests.get(url)
    response.raise_for_status()

    df = pd.read_excel(BytesIO(response.content))
    return df

#print(df.head())
#print(df.shape)
# Test Git