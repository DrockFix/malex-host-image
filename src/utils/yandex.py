from aiogram.client.session import aiohttp


# async def upload_to_yandex_disk(dir, file, yandex_token):
#     dir_yandex = dir.replace("./", "/")
#     url = f'https://cloud-api.yandex.net/v1/disk/resources?path=disk:{dir_yandex}'
#     headers = {
#         'Authorization': f'OAuth {yandex_token}'
#     }
#     async with aiohttp.ClientSession() as session:
#         try:
#             async with session.put(url, headers=headers) as response:
#                 url = f'https://cloud-api.yandex.net/v1/disk/resources/upload?path={dir_yandex}/{file}&overwrite=true'
#                 async with session.get(url, headers=headers) as response:
#                     if response.status == 200:
#                         data = await response.json()
#                         upload_url = data.get('href')
#                         if upload_url:
#                             async with session.put(upload_url, data=open(f"{dir}/{file}", 'rb')):
#                                 pass
#         except aiohttp.ClientError as e:
#             print(e)


async def upload_to_yandex_disk(dir, file, yandex_token):
    dir_yandex = dir.replace("./", "/")
    url = f'https://cloud-api.yandex.net/v1/disk/resources?path=disk:{dir_yandex}'
    headers = {
        'Authorization': f'OAuth {yandex_token}'
    }
    async with aiohttp.ClientSession() as session:
        try:
            # Create directories recursively
            dirs = dir_yandex.split('/')
            for i in range(1, len(dirs)):
                dir_path = '/'.join(dirs[:i+1])
                url = f'https://cloud-api.yandex.net/v1/disk/resources?path=disk:{dir_path}'
                async with session.put(url, headers=headers) as response:
                    pass
            # Upload file
            url = f'https://cloud-api.yandex.net/v1/disk/resources/upload?path={dir_yandex}{file}&overwrite=true'
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    upload_url = data.get('href')
                    if upload_url:
                        async with session.put(upload_url, data=open(f"{dir}/{file}", 'rb')):
                            pass
        except aiohttp.ClientError as e:
            print(e)