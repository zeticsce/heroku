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

import logging
import os
import random
import typing

import herokutl
from herokutl.tl.functions.messages import (
    GetDialogFiltersRequest,
    UpdateDialogFilterRequest,
)
from herokutl.tl.types import Message, User
from herokutl.utils import get_display_name

from .. import loader, log, main, utils
from .._internal import fw_protect, restart
from ..inline.types import InlineCall
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
        
        try:
            id = int(id)
        except ValueError:
            pass

        try:
            user = await self._client.get_entity(id)
        except Exception as e:
            logger.error(f"Error while fetching user: {e}")
            user = None
            
        
        if user.id == self._client.tg_id:
            await utils.answer(
                message,
                "Вы не можете добавить самого себя же."
            )
            return

        if not user or not isinstance(user, User) or user.bot:
            await utils.answer(
                message,
                "Ответьте на сообщение человека, которого хотите добавить, или укажите его корректный @username/id."
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
        
    async def _inline_login(self, call: typing.Union[Message, InlineCall], user: User):
        reply_markup = [
            {"text": "Ввести номер", "input":"Ваш номер телефона", "handler":self.inline_phone_handler, "args":(user,)}
        ]
        await utils.answer(
            call,
            "Введите свой номер телефона в международном формате (например, +79212345678):",
            reply_markup=reply_markup,
            always_allow=[user.id]
        )


    async def inline_phone_handler(self, call, data, user): pass
        
    async def inline_code_handler(self, call, data, user): pass

    async def inline_2fa_handler(self, call, data, user): pass