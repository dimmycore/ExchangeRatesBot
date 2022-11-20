import requests
import json
from config import keys


class APIException(Exception):
    pass


class GetPrice:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException('нужно указать разные криптовалюты')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'не удалось обработать криптовалюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'не удалось обработать криптовалюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'не удалось обработать количество {amount}')

        r = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={quote_ticker}{base_ticker}')
        j = json.loads(r.content)
        total_base = float(amount) * float(j['price'])

        return total_base