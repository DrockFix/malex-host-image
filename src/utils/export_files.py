import os
import pathlib
from datetime import datetime

from src.common.month import month_names
from src.utils.yandex import upload_to_yandex_disk


async def save_report(bot, data):
    date = datetime.fromisoformat(data['date'])
    full_month_name = date.strftime('%B').capitalize()
    image_dir = pathlib.Path(os.getenv('PATH_IMAGE'))
    for i, img in enumerate(data['image']):
        file_path = await bot.get_file(img)
        downloaded_file = await bot.download_file(file_path.file_path)
        file_dir = image_dir / data['type_name'].upper() / str(date.year) / full_month_name
        if 'place' in data:
            file_dir /= data['place']
        if 'device' in data:
            file_dir /= data['device']
        file_dir.mkdir(parents=True, exist_ok=True)
        file_name = f"{date.strftime('%d.%m.%Y')}_{i+1}.jpg"
        file_path = file_dir / file_name
        with file_path.open('wb') as file:
            file.write(downloaded_file.read())
        # await upload_to_yandex_disk(file_dir, file_name, os.getenv('YANDEX_TOKEN'))
