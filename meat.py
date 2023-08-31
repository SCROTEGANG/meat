from typing import Dict, List, Optional
import logging
import re
import random

import aitextgen
import aiohttp
import discord
from discord.ext import tasks

from config import Config

log = logging.getLogger(__name__)

MENTION_RE = re.compile(r"<[\!\@]?\d{1,20}>")


class Meat(discord.Client):
    """A flesh experiment of Shang Tsung gone wrong, but more importantly the one that got away. </3"""

    def __init__(self, options: Dict):
        self.options = options
        self.ai = aitextgen.aitextgen(model_folder=options.get("MEAT_MODEL_PATH"), )  # type: ignore

        default_config = {
            "speak": options.get("MEAT_SPEAK_DEFAULT")
        }

        self.config = Config(options.get("MEAT_CONFIG_PATH"), default_config)

        intents = discord.Intents.all()
        allowed_mentions = discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=True)

        super().__init__(
            intents=intents,
            allowed_mentions=allowed_mentions,
        )

    async def setup_hook(self) -> None:
        self.session = aiohttp.ClientSession(raise_for_status=True)
        await self.config.load()
        self.speak.start()

    @tasks.loop(minutes=34, hours=8,)
    async def speak(self):
        should_speak = self.config.get("speak")
        if should_speak is not None and should_speak:
            content = self.ai.generate_one()
            content = await self._do_translate(content)

            await self.send_message(self.options.get("MEAT_SPEAK_CHANNEL"), content)

        new_hour = random.randint(8, 12)
        new_minute = random.randint(0, 59)
        self.speak.change_interval(minutes=new_minute, hours=new_hour)

    @speak.before_loop
    async def before_speak(self):
        await self.wait_until_ready()

    async def on_message(self, m: discord.Message):
        if m.author.bot:
            return

        lower = m.content.lower()
        if lower.startswith("meat, "):
            if m.author.id != self.application.owner.id and not m.author.guild_permissions.manage_guild:
                return

            command = lower.removeprefix("meat, ")
            if command == "speak":
                self.config.set("speak", True)
                await self.config.save()
                await m.reply("hguuuuuuuurrrrrrrghh \\*gurgle\\*")
            elif command == "shut up":
                self.config.set("speak", False)
                await self.config.save()
                await m.reply("<:huh:1146847007684710590>")

        if self.user.mentioned_in(m):
            async with m.channel.typing():
                clean_content = MENTION_RE.sub(m.content, "")
                contents = self.ai.generate(n=10, temperature=1.0, prompt=clean_content.strip(), return_as_list=True)

                resp = ""
                for content in contents:
                    # loop through the 10 pieces of text we generated
                    # skip if they're the same as the input
                    if content == content:
                        continue
                    resp = content

                if resp == clean_content:
                    resp = self.ai.generate_one()

                if resp is not None:
                    await self.reply(m, resp)

    async def _do_translate(self, content: str):
        if random.randint(0, 100) == 1:
            try:
                translation = await self.translate(content)
                if translation is not None:
                    content = translation
            except aiohttp.ClientResponseError as e:
                log.error(f"error translating text: {e}")

        return content

    async def send_message(self, id: int, content: str):
        channel = self.get_channel(id)
        content = await self._do_translate(content)
        await channel.send(content=content)

    async def reply(self, m: discord.Message, content: str):
        content = await self._do_translate(content)
        await m.reply(content)

    async def translate(self, body: str) -> Optional[str]:
        params = {
            "api-version": "3.0",
            "from": "en",
            "to": ["ko"],
        }
        headers = {
            "Ocp-Apim-Subscription-Key": self.options.get("MEAT_TRANSLATE_KEY"),
            "Ocp-Apim-Subscription-Region": self.options.get("MEAT_TRANSLATE_REGION"),
            "Content-Type": "application/json",
        }
        _text = [{
            "text": body
        }]
        url = f"{self.options.get('MEAT_TRANSLATE_ENDPOINT')}/translate"

        async with self.session as sess:
            async with sess.post(url, params=params, headers=headers, json=_text) as resp:
                data: List[Dict[str, str]] = await resp.json()
                if len(data) > 0:
                    translations = data[0].get("translations")
                    if len(translations) > 0:
                        return translations[0].get("text")

                return None
