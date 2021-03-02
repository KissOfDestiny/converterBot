import requests
import json
from config import keys


class ConversionException(Exception):
    pass


class CurConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversionException(f'\nА смысл конвертировать {quote} в {base}?')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'\nНе удалось опознать валюту {quote}, /values')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'\nНе удалось опознать валюту {base}, /values')
        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'\nНеверное количество {amount}')
        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={quote_ticker}&symbols={base_ticker}')
        total = round((float(amount) * float(json.loads(r.content)['rates'][keys[base]])), 3)
        return total
