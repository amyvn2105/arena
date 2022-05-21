import requests


class BaseClient:
    """
    The base client to connect to platform
    """

    def request(self, url: str, method: str, data: dict = {}, headers: dict = {}, params: dict = {}) -> any:
        response = None
        num_of_retry = 3
        for i in range(num_of_retry):
            if method == 'GET':
                response = requests.get(url=url, data=data, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url=url, data=data, headers=headers, params=params)
            elif method == 'PUT':
                response = requests.put(url=url, data=data, headers=headers, params=params)
            else:
                raise ValueError(f'Wrong http method: {method}')

            if response.status_code != 200:
                print(
                    f'Failed to send request: url: {url} - method: {method} - params: {params} - header: {headers} - code: {response.status_code}')
            else:
                return response
            print(f'Retry request: {url}')

        return response
