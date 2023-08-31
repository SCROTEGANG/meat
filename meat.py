from typing import Dict, List, Optional
import logging
import re
import random

import aitextgen
import aiohttp
import discord

log = logging.getLogger(__name__)

MENTION_RE = re.compile(r"<[\!\@]?\d{1,20}>")


class Meat(discord.Client):
    """A flesh experiment of Shang Tsung gone wrong, but more importantly the one that got away. </3"""

    def __init__(self, options: Dict):
        self.options = options
        self.ai = aitextgen.aitextgen(model_folder=options.get("MEAT_MODEL_PATH"), )  # type: ignore

        intents = discord.Intents.all()
        allowed_mentions = discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=True)

        super().__init__(
            intents=intents,
            allowed_mentions=allowed_mentions,
        )

    async def setup_hook(self) -> None:
        self.session = aiohttp.ClientSession(raise_for_status=True)

    async def on_message(self, m: discord.Message):
        if m.author.bot:
            return

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

                if random.randint(1, 100) == 1:
                    try:
                        if resp is not None:
                            translation = await self.translate(resp)
                            if translation is not None:
                                resp = translation
                    except aiohttp.ClientResponseError as e:
                        log.error(f"error translating text: {e}")

                await m.reply(resp)

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
