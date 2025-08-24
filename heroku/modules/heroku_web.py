# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

# ©️ Codrago, 2024-2025
# This file is a part of Heroku Userbot
# 🌐 https://github.com/coddrago/Heroku
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import asyncio
import logging
import os
import random
import string
import typing

import herokutl
from herokutl.errors import (
    FloodWaitError,
    PasswordHashInvalidError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
    YouBlockedUserError,
)
from herokutl.sessions import MemorySession
from herokutl.utils import get_display_name, parse_phone
from herokutl.tl.functions.messages import (
    GetDialogFiltersRequest,
    UpdateDialogFilterRequest,
)
from herokutl.tl.types import Message, User

from .. import loader, log, main, utils
from .._internal import fw_protect, restart
from ..inline.types import InlineCall
from ..tl_cache import CustomTelegramClient
from ..version import __version__
from ..web import core

logger = logging.getLogger(__name__)


@loader.tds
class HerokuWebMod(loader.Module):
    """Web/Inline mode add account"""

    strings = {"name": "HerokuWeb"}


    @loader.command()
    async def weburl(self, message: Message, force: bool = False):

        if "SHARKHOST" in os.environ or "HIKKAHOST" in os.environ or "JAMHOST" in os.environ:
            await utils.answer(message, self.strings["host_denied"])
        else:
        
            if "LAVHOST" in os.environ:
                form = await self.inline.form(
                    self.strings("lavhost_web"),
                    message=message,
                    reply_markup={
                       "text": self.strings("web_btn"),
                       "url": await main.heroku.web.get_url(proxy_pass=False),
                    },
                    photo="https://imgur.com/a/yOoHsa2.png",
                )
                return

            if (
                not force
                and not message.is_private
                and "force_insecure" not in message.raw_text.lower()
            ):
                try:
                    if not await self.inline.form(
                        self.strings("privacy_leak_nowarn").format(self._client.tg_id),
                        message=message,
                        reply_markup=[
                            {
                                "text": self.strings("btn_yes"),
                                "callback": self.weburl,
                                "args": (True,),
                            },
                            {"text": self.strings("btn_no"), "action": "close"},
                        ],
                        photo="https://raw.githubusercontent.com/coddrago/assets/refs/heads/main/heroku/web_interface.png",
                    ):
                        raise Exception
                except Exception:
                    await utils.answer(
                        message,
                        self.strings("privacy_leak").format(
                            self._client.tg_id,
                            utils.escape_html(self.get_prefix()),
                        ),
                    )

                return

            if not main.heroku.web:
                main.heroku.web = core.Web(
                    data_root=main.BASE_DIR,
                    api_token=main.heroku.api_token,
                    proxy=main.heroku.proxy,
                    connection=main.heroku.conn,
                )
                await main.heroku.web.add_loader(self._client, self.allmodules, self._db)
                await main.heroku.web.start_if_ready(
                    len(self.allclients),
                    main.heroku.arguments.port,
                    proxy_pass=main.heroku.arguments.proxy_pass,
                )

            if force:
                form = message
                await form.edit(
                    self.strings("opening_tunnel"),
                    reply_markup={"text": "🕔 Wait...", "data": "empty"},
                    photo=(
                        "https://raw.githubusercontent.com/coddrago/assets/refs/heads/main/heroku/opening_tunnel.png"
                    ),
                )
            else:
                form = await self.inline.form(
                    self.strings("opening_tunnel"),
                    message=message,
                    reply_markup={"text": "🕔 Wait...", "data": "empty"},
                    photo=(
                        "https://raw.githubusercontent.com/coddrago/assets/refs/heads/main/heroku/opening_tunnel.png"
                    ),
                )

            url = await main.heroku.web.get_url(proxy_pass=True)

            await form.edit(
                self.strings("tunnel_opened"),
                reply_markup={"text": self.strings("web_btn"), "url": url},
                photo="https://raw.githubusercontent.com/coddrago/assets/refs/heads/main/heroku/tunnel_opened.png",
            )

    @loader.command()
    async def addacc(self, message: Message):
        id = utils.get_args(message)
        if not id:
            reply = await message.get_reply_message()
            id = reply.sender_id if reply else None
        else:
            id = id[0]
        
        user = None
        if id:
            try:
                id = int(id)
            except ValueError:
                pass

            try:
                user = await self._client.get_entity(id)
            except Exception as e:
                logger.error(f"Error while fetching user: {e}")

        if not user or not isinstance(user, User) or user.bot:
            await utils.answer(
                message,
                "Ответьте на сообщение человека, которого хотите добавить, или укажите его корректный @username/id."
            )
            return
        
        if user.id == self._client.tg_id:
            await utils.answer(
                message,
                "Вы не можете добавить самого себя же."
            )
            return
        
        if "force_insecure" in message.text.lower():
            await self._inline_login(message, user)
        
        try:
            if not await self.inline.form(
                    "Вы действительно хотите добавить аккаунт {} ({})?".format(
                        utils.escape_html(user.first_name),
                        user.id,
                    ),
                    message=message,
                    reply_markup=[
                        {
                            "text": self.strings("btn_yes"),
                            "callback": self._inline_login,
                            "args": (user,),
                        },
                        {"text": self.strings("btn_no"), "action": "close"},
                    ],
                    photo="",
                ):
                raise Exception
        except Exception:
            await utils.answer(
                message,
                "Вы действительно хотите добавить аккаунт {} ({})? Используйте команду <code>{}addacc {} force_insecure</code> для подтверждения.".format(
                    utils.escape_html(user.first_name),
                    user.id,
                    utils.escape_html(self.get_prefix()),
                    user.id,
                )
            )
        return
        
    async def _inline_login(self, call: typing.Union[Message, InlineCall], user: User, after_fail: bool = False):
        reply_markup = [
            {"text": "Ввести номер", "input":"Ваш номер телефона", "handler":self.inline_phone_handler, "args":(user,)}
        ]

        fail = "Вы ввели неверный номер телефона.\n\n" if after_fail else ""

        await utils.answer(
            call,
            fail + "Введите свой номер телефона в международном формате (например, +79212345678):",
            reply_markup=reply_markup,
            always_allow=[user.id]
        )


    def _get_client(self) -> CustomTelegramClient:
        return CustomTelegramClient(
            MemorySession(),
            main.heroku.api_token.ID,
            main.heroku.api_token.HASH,
            connection=main.heroku.conn,
            proxy=main.heroku.proxy,
            connection_retries=None,
            device_model=main.get_app_name(),
            system_version="Windows 10",
            app_version=".".join(map(str, __version__)) + " x64",
            lang_code="en",
            system_lang_code="en-US",
        )
    
    async def schedule_restart(self,One=None):
        # Yeah-yeah, ikr, but it's the only way to restart
        await asyncio.sleep(1)
        await main.heroku.save_client_session(self._pending_client, delay_restart=False)
        restart()

    async def inline_phone_handler(self, call, data, user):
        if not (phone := parse_phone(data)):
            await self._inline_login(call, user)
            return
        
        client = self._get_client()

        await client.connect()
        try:
            await client.send_code_request(phone)
        except FloodWaitError as e:
            await utils.answer(
                call,
                "Слишком много попыток. Попробуйте снова через {} секунд.".format(e.seconds),
                reply_markup={"text": "Закрыть", "action": "close"},
            )
            return
        
        reply_markup = [
            {"text": "Ввести код", "input":"Ваш код для входа", "handler":self.inline_code_handler, "args":(client, phone, user,)},
        ]
        
        await utils.answer(
            call,
            "Код был отправлен. Введите его",
            reply_markup=reply_markup,
            always_allow=[user.id]
        )
        
    async def inline_code_handler(self, call, data, client, phone, user):
        if not data or len(data) != 5:
            await utils.answer(
                call,
                "Невалидный код. Повторите попытку.",
                reply_markup={"text": "Ввести код", "input":"Ваш код для входа", "handler":self.inline_code_handler, "args":(client, phone, user,)},
                always_allow=[user.id]
            )
            return
        
        if any(c not in string.digits for c in data):
            await utils.answer(
                call,
                "Код должен состоять только из цифр. Повторите попытку.",
                reply_markup={"text": "Ввести код", "input":"Ваш код для входа", "handler":self.inline_code_handler, "args":(client, phone, user,)},
                always_allow=[user.id]
            )
            return
        
        try:
            await client.sign_in(phone, code=data)
        except SessionPasswordNeededError:
            reply_markup = [
                {"text": "Ввести 2FA пароль", "input":"Ваш пароль", "handler":self.inline_2fa_handler, "args":(client, phone, user,)},
            ]
            await utils.answer(
                call,
                "У вас включена двухфакторная аутентификация. Введите пароль.",
                reply_markup=reply_markup,
                always_allow=[user.id]
            )
            return 
        except PhoneCodeExpiredError:
            reply_markup = [
                {"text": "🔃 Запросить код снова", "callback": self.inline_phone_handler, "args": (phone, user)}
            ]
            await utils.answer(
                call,
                "Срок действия кода истек.",
                reply_markup=reply_markup,
                always_allow=[user.id],
            )
            return 
        except PhoneCodeInvalidError:
            reply_markup = [
                {"text": "Ввести код", "input":"Ваш код для входа", "handler":self.inline_code_handler, "args":(client, phone, user,)},
            ]
            await utils.answer(
                call,
                "Неверный код. Повторите попытку.",
                reply_markup=reply_markup,
                always_allow=[user.id]
            )
            return 
        except FloodWaitError as e:
            await utils.answer(
                call,
                "Слишком много попыток. Попробуйте снова через {} секунд.".format(e.seconds),
                reply_markup={"text": "Закрыть", "action": "close"},
            )
            return
        
        asyncio.ensure_future(self.schedule_restart(self))


    async def inline_2fa_handler(self, call, data, client, phone, user):
        if not data:
            await utils.answer(
                call,
                "Невалидный пароль. Повторите попытку.",
                reply_markup={"text": "Ввести 2FA пароль", "input":"Ваш пароль", "handler":self.inline_2fa_handler, "args":(client, phone, user,)},
                always_allow=[user.id]
            )
            return
        
        try:
            await client.sign_in(phone, password=data)
        except PasswordHashInvalidError:
            await utils.answer(
                call,
                "Неверный пароль. Повторите попытку.",
                reply_markup={"text": "Ввести 2FA пароль", "input":"Ваш пароль", "handler":self.inline_2fa_handler, "args":(client, phone, user,)},
                always_allow=[user.id]
            )
            return 
        except FloodWaitError as e:
            await utils.answer(
                call,
                "Слишком много попыток. Попробуйте снова через {} секунд.".format(e.seconds),
                reply_markup={"text": "Закрыть", "action": "close"},
            )
            return
        
        asyncio.ensure_future(self.schedule_restart(self))