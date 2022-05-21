from core.base import BaseClient


class TikiClient(BaseClient):
    def __init__(self) -> None:
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
            'referer': 'https://tiki.vn/search?q=laptop',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            'x-guest-token': 'fS5jQwqAUMucVvbWl19teNEIRKzko2Zr'
        }

    def send_request(self, url: str, method: str, data: dict = {}, headers: dict = {}, params: dict = {}):
        response = self.request(
            url=url, data=data, headers=headers, params=params, method=method)
        if response.status_code != 200:
            print(
                f'Failed to send request: url: {url} - params: {params} - header: {headers} - code: {response.status_code}')
        return response
