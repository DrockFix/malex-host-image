from pyrogram import Client


async def get_chat_members(name, api_id, api_hash, bot_token, chat_id):
    async with Client(name, api_id=api_id, api_hash=api_hash, bot_token=bot_token) as app:
        try:
            members = [member async for member in app.get_chat_members(chat_id)]
            return members
        except Exception as e:
            print(f"Ошибка: {e}")
            return []

