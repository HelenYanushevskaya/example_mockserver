import requests


class Mocks:
    """
    A mock configured to return specific responses for different requests or
    a proxy recording and optionally modifying requests and responses
    https://www.mock-server.com/#what-is-mockserver"""

    def __init__(self):
        # type: () -> None
        # self.mock_server_url = 'http://mock.server.admitad.test:1080'
        # self.dashboard_url = 'http://mock.server.admitad.test:1080/mockserver/dashboard'
        self.mock_server_url = 'http://0.0.0.0:1080'
        self.dashboard_url = 'http://localhost:1080/mockserver/dashboard'

    def _set_expectation(self, json_body):
        # type: (AnyStr) -> None
        expectation_url = '/mockserver/expectation'
        requests.put(self.mock_server_url + expectation_url, json=json_body)

    def reset_mock(self):
        # type: () -> None
        """clears all expectations and recorded requests"""
        requests.put(self.mock_server_url + '/reset')

    def set_example_mock(self, path, status_code=200):
        json_body = {
            "httpRequest": {
                "method": "GET",
                "path": path,
            },
            "httpResponse": {
                "statusCode": status_code,
                "body": {
                    "username": "foo",
                    "password": "bar"
                }
            }
        }
        self._set_expectation(json_body)
