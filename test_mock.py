import os

from selenium import webdriver

from mock_server import Mocks

messages = 'http://192.168.1.233:1081/messages_auth'
auth = 'http://192.168.1.233:1081/auth'
base = 'http://192.168.1.233:1081/'
list_messages = 'http://192.168.1.233:1081/messages'


class TestSimple(object):

    def test_messages_request(self):
        response = requests.get(messages)

        assert response.status_code == 200
        assert response.json()['result'][2]['text'] == "welcome to the messages"

    # проверка что сервер работает в браузере
    def test_messages_browser(self):
        driver = webdriver.Chrome(executable_path='/Users/eayanushevskaya/Downloads/chromedriver 2')
        driver.get(base)

        element = driver.find_element_by_id("message")
        assert element.text == 'Check browser'

        driver.close()


class TestMockserver(object):

    def test_mockserver_messages(self):
        os.environ['HTTP_PROXY'] = Mocks().mock_server_url
        Mocks().set_example_mock(path='/messages')

        response = requests.get(messages)

        assert response.status_code == 200
        assert response.json()['username'] == 'foo'

        Mocks().reset_mock()

    def test_mockserver_app_auth(self):
        os.environ['HTTP_PROXY'] = Mocks().mock_server_url
        Mocks().set_example_mock(path='/authorization', status_code=500)

        response = requests.get(messages)

        assert response.json()['error'] == 'Authorization failed'
        Mocks().reset_mock()


class TestMockserverBrowser(object):

    def test_mockserver_messages(self):
        os.environ['HTTP_PROXY'] = Mocks().mock_server_url
        Mocks().set_example_mock(path='/authorization', status_code=200)

        driver = webdriver.Chrome(executable_path='/Users/eayanushevskaya/Downloads/chromedriver 2')
        driver.get(auth)

        element = driver.find_element_by_id("message")
        assert element.text == 'Authorization success'

        Mocks().reset_mock()
        driver.close()

    def test_mockserver_app_browser_request(self):
        os.environ['HTTP_PROXY'] = Mocks().mock_server_url
        Mocks().set_example_mock2(path='/messages', status_code=200)

        options = webdriver.ChromeOptions()
        options.add_argument("--proxy-server=" + Mocks().mock_server_url)

        driver = webdriver.Chrome(executable_path='/Users/eayanushevskaya/Downloads/chromedriver 2', options=options)
        driver.get(list_messages)

        element = driver.find_element_by_xpath("/html/body/pre")
        assert element.text == 'some_response_body'

        Mocks().reset_mock()
        driver.close()
