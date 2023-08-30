import asyncio
import os
import sys
import re

import aitextgen
import discord

async def main():
    token = os.getenv("MEAT_TOKEN")
    model_path = os.getenv("MEAT_MODEL_PATH")

    if token is None:
        sys.exit("$MEAT_TOKEN is not set")
    
    if model_path is None:
        sys.exit("$MODEL_PATH is not set")


    client = discord.Client(allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=True))
    ai = aitextgen.aitextgen(model_folder=model_path)
    mention_re = re.compile(r"<[\!\@]?\d{1,20}>")

    @client.event
    async def on_message(msg: discord.Message):
        if msg.author.bot:
            return
        
        if client.user.mentioned_in(msg):
            async with msg.channel.typing():
                content = mention_re.sub(msg.content, "")
                cnts = ai.generate(n=10, temperature=1.0, prompt=content.strip(), return_as_list=True)
                for cnt in cnts:
                    if cnt == content:
                        continue
                    await msg.reply(cnt)
                    return
                
                cnt = ai.generate_one()
                await msg.reply(cnt)

    await client.start(token)

if __name__ == "__main__":
    asyncio.run(main())
