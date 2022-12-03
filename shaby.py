import random
from asyncio import sleep
import os
from .. import loader, utils


@loader.owner
def register(cb):
    cb(ShabyMod())


class ShabyMod(loader.Module):
    strings = {"name": "Shaby"}

    async def client_ready(self, client, db) -> None:
        self.db = db
        self.client = client

    async def dlrcmd(self, message):
        """Команда .dlr <реплай на файл> <название (по желанию)> скачивает файл, либо сохраняет текст в файл на который был сделан реплай."""
        name = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if reply:
            await message.edit('Скачиваем...')
            if reply.text:
                text = reply.text
                fname = f'{name or message.id + reply.id}.txt'
                file = open(fname, 'w')
                file.write(text)
                file.close()
                await message.edit(
                    f'Файл сохранён как: <code>{fname}</code>')
            else:
                ext = reply.file.ext
                fname = f'{name or message.id + reply.id}{ext}'
                await message.client.download_media(reply, fname)
                await message.edit(
                    f'Этот файл сохранён как: <code>{fname}')
        else:
            return await message.edit('Нет реплая.')

    async def shbcmd(self, message):
        """тайминг в секундах + название шаблона(с .txt) + шапка"""
        shapka = utils.get_args_raw(message)
        if not shapka:
            self.db.set(self.strings["name"], "state", False)
            await utils.answer(message, "<b>Модуль Shaby остановлен!</b>")
            return
        await utils.answer(
            message,
            "<b>Модуль Shaby запущен!\n\n"
            "Чтобы его остановить, используй <code>.shb</code></b>",
        )
        text = shapka.split(' ')
        time = int(text[0])
        sh = ''.join(text[1])
        shp = ' '.join(text[2:])
        self.db.set(self.strings["name"], "state", True)
        while self.db.get(self.strings["name"], "state"):
            with open(f'{sh}', 'r', encoding='utf-8') as f:
                s = f.read()
                w = s.split('\n')
                await message.respond((shp + random.choice(w)))
                await sleep(time)


