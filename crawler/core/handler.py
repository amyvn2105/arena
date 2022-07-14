import json

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from pandas import DataFrame

CRAWLER_PREFIX = 'crawler_file'
TRANSFORM_PREFIX = 'transform_file'
DESTINATION = 'destination'


class BaseHandler:

    def __init__(self) -> None:
        self.product: str

    def _crawl(self):
        pass

    def _transform(self):
        out_prefix = self.get_out_prefix()
        items = self.transform()
        try:
            if items:
                print(f'There are {len(items)} items will be write to {out_prefix}')
                self.write_list(prefix=out_prefix, data=items, product=self.product)
                print('--------------------------------------------------------')
        except Exception as e:
            print(e)

    def _load(self):
        pass

    def transform(self) -> list:
        pass

    def get_out_prefix(self) -> str:
        pass

    def write_json(self, data: dict, prefix: str, product: str):
        file_name = f"{product}.json"
        path = f"{prefix}/{file_name}"

        with open(path, "w") as outfile:
            json.dump(data, outfile)

    def write_list(self, data: list, prefix: str, product: str):
        file_name = f"{product}.json"
        path = f"{prefix}/{file_name}"

        with open(path, "w") as out_file:
            json.dump(data, out_file)
        print(f'Successfully to write {len(data)} to {path}')

    def write_excel(self, data: DataFrame, prefix: str, product: str):
        file_name = f"{product}.xlsx"
        path = f"{prefix}/{file_name}"
        data.to_excel(path, index=False, engine='xlsxwriter')
        print(f'Successfully to write {len(data)} to {path}')

    def read_json(self, prefix: str, product: str):
        file_name = f"{product}.json"
        path = f"{prefix}/{file_name}"

        with open(path, "r") as open_file:
            return json.load(open_file)

    def _to_dataFrame(self, data):
        df = pd.DataFrame(data=data)
        return df

    def _bulk_upsert(self, connection: dict, schema: str, table_name: str, items: dict):
        conn = psycopg2.connect(host=connection.get('host'),
                                port=connection.get('port'),
                                dbname=connection.get('database'),
                                user=connection.get('username'),
                                password=connection.get('password'))

        cur = conn.cursor()
        columns = ','.join(items[0].keys())
        table = f'{schema}.{table_name}'
        # query = "INSERT INTO {} ({}) VALUES %s".format(table, columns)
        query = '''
        INSERT INTO {} ({})
        VALUES %s 
        ON CONFLICT ON CONSTRAINT product_pkey 
        DO NOTHING;
        '''.format(table, columns)

        values = [[value for value in item.values()] for item in items]
        try:
            execute_values(cur=cur, sql=query, argslist=values)
            print(f'Successfully insert {len(items)} records into {table}')
        except Exception as e:
            print(e)

        conn.commit()
        conn.close()
