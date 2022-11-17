import re
import httpx
import asyncio
import time


url_methods = [
    'GET',
    'HEAD',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'CONNECT',
    'OPTIONS',
    'TRACE',
]
url_pattern = 'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
value_list = [
    "https://ca-manager-api.herokuapp.com/api/user",
    "hello World",
    "https://google.com",
    "facebook.com",
    "https://www.facebook.com",
    "https://esp8266.ru/forum/threads/ehnergopotreblenie-esp-novoe.2591/",
    "https://www.python-httpx.org/quickstart/",
    "jlad;asmdl;as.com",
]


def url_validator(url):
    val_urls = re.match(url_pattern, url)
    if val_urls:
        return url
    return None


async def check_methods(method, url):
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url)
        if response.status_code != 405:
            return method, response.status_code


async def get_available_methods(url, methods_list):
    validated_url = url_validator(url)
    if validated_url is None:
        print(f'{url} is not url')
        return None
    methods = tuple(await asyncio.gather(*(check_methods(method, url) for method in methods_list)))
    methods = tuple(filter(lambda x: x is not None, methods))
    return url, dict(methods)


async def main(url_list, methods_list):
    start_time = time.time()
    url_methods_cont = tuple(await asyncio.gather(*(get_available_methods(url, methods_list) for url in url_list)))
    url_methods_cont = tuple(filter(lambda x: x is not None, url_methods_cont))
    print("--- %s seconds ---" % (time.time() - start_time))
    return dict(url_methods_cont)


if __name__ == '__main__':
    print(asyncio.run(main(value_list, url_methods)))
