"""Клиент-рассылка
Создатель: ITaData
Дата создания: 19.11.2022"""
"""Imports"""
import asyncio
from telethon import TelegramClient
import pandas as pd

"""Глобальные переменные"""
api_id, api_hash = '', ''
df = pd.read_csv('subscribers.csv',sep='\t')
"""Открытие файла с паролем"""
with open("/home/admi/.config/dconf/pass.txt", 'r') as api:
    text = api.readlines()
    api_id = text[0][:-1]
    api_hash = text[1][:-2]
"""Отправка сообщения"""
async def send(df, client):
       for id in df['id'].values:
           await client.send_message(int(id),"Извините проверка бота")

"""Поиск подписчиков для дальнейшей рассылки"""
async def search(df):
    client = TelegramClient('Mailing', api_id, api_hash)
    client = await client.start()
    dialogs = await client.get_dialogs()
    channels = {'tesclient'}  # Список каналов, где вы являетесь АДМИНОМ
    for channel in channels:
        members_telethon_list = await client.get_participants(channel, aggressive=True)
        username_list = [str(member.username) for member in members_telethon_list]
        first_name_list = [member.id for member in members_telethon_list]
        last_name_list = [str(member.first_name) for member in members_telethon_list]
        phone_list = [str(member.phone) for member in members_telethon_list]
        df2 = pd.DataFrame()
        df2['username'] = username_list
        df2['id'] = first_name_list
        df2['id'] =df2['id'].astype('int64')
        df2['first_name'] = last_name_list
        df2['phone'] = phone_list
        # Проверка перед объединением двух датафреймов
        if not df.empty:
            df =df.merge(df2)
        else:
            df = df2
    df = df.drop_duplicates()
    df.to_csv('subscribers.csv', index=False, sep='\t')  # Запись в .csv формат
    await send(df, client)


if __name__ == '__main__':
    # Запуск клиента в асинхронном режиме
    loop = asyncio.get_event_loop()
    loop.run_until_complete(search(df))
