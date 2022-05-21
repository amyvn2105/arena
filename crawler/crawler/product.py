from core.handler import BaseHandler, CRAWLER_PREFIX, TRANSFORM_PREFIX
from core.tiki import TikiClient
from datetime import datetime
import os

COOKIE = '_trackity=c5171f6c-5b54-f8d6-09e4-746e5e737130'
PREFIX = f'{os.getcwd()}/..'
PLATFORM = 'TIKI'
CONNECTION = {
    'host': 'localhost',
    'port': '5433',
    'database': 'csd',
    'username': 'postgres',
    'password': 'postgres'
}


class Handler(BaseHandler):

    def __init__(self) -> None:
        super().__init__()

    def get_data(self, product, page, product_list):
        crawler = TikiClient()
        self.headers = {**crawler.headers, **{'cookie': COOKIE, 'authority': 'tiki.vn'}}
        url = f"https://tiki.vn/api/v2/products?limit=48&include=advertisement&aggregations=2&q={product}&page={page}"

        print(f'Send request to {url}')
        response = crawler.send_request(url=url, method='GET', headers=self.headers)

        body = response.json()
        product_list.extend(body.get('data'))

        if not body.get('data'):
            print(f'No data from {url}')
            result = {
                'data': product_list,
                'len': len(product_list)
            }
            return result
        else:
            page = page + 1
            return self.get_data(product, page, product_list)

    def _crawl(self):
        date = datetime.now()
        try:
            data = self.get_data(product=self.product, page=1, product_list=[])
            prefix = self.get_prefix(method=CRAWLER_PREFIX, date=date)
            self.write_json(prefix=prefix, data=data, product=self.product)
            print(f"Successfully to write {len(data.get('data'))} to {prefix}")
            print('--------------------------------------------------------')
        except Exception as e:
            print(f'Error: {e}')

    def transform(self) -> list:
        date = datetime.now()
        prefix = self.get_prefix(method=CRAWLER_PREFIX, date=date)
        raw_data = self.read_json(prefix=prefix, product=self.product)
        items = self._parse(raw_data)
        res_list = list({frozenset(item.values()): item for item in items}.values())
        return res_list

    def _load(self):
        date = datetime.now()
        prefix = self.get_prefix(method=TRANSFORM_PREFIX, date=date)
        items = self.read_json(prefix=prefix, product=self.product)
        self._bulk_upsert(schema='crawler', table_name='product', connection=CONNECTION, items=items)

    def get_prefix(self, method: str, date: datetime):
        day = date.strftime('%Y/%m/%d')
        path = f"{PREFIX}/{method}/{day}"

        if not os.path.exists(path):
            os.makedirs(path)
            print("The new directory is created!")
        return path

    def get_out_prefix(self):
        date = datetime.now()
        return self.get_prefix(method=TRANSFORM_PREFIX, date=date)

    def _parse(self, raw):
        data = []
        try:
            if raw.get('data'):
                for item in raw.get('data'):
                    record = self._to_item(item)
                    if record is not None:
                        data.append(record)
            return data
        except Exception as e:
            print(e)
        return []

    def _to_item(self, item):
        record = {}
        if item:
            record = {
                'platform': PLATFORM,
                'category': self.product,
                'product_id': item.get('id'),
                'product_name': item.get('name'),
                'price': float(item.get('price')),
                'original_price': float(item.get('original_price')),
                'discount_rate': round(item.get('discount_rate') / 100, 2),
                'seller_id': item.get('seller_id'),
                'seller_name': item.get('seller_name'),
                'brand_id': item.get('brand_id'),
                'brand_name': item.get('brand_name'),
                'rating_average': round(item.get('rating_average'), 2),
                'review_count': item.get('review_count'),
                'url_path': f"tiki.vn/{item.get('url_path')}"
            }
        return record


if __name__ == '__main__':
    crawler = Handler()
    crawler.product = 'dien thoai'
    time = datetime.now()
    crawler._crawl()
    crawler._transform()
    crawler._load()
    # print(datetime.now() - time)