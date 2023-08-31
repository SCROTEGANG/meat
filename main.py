import os
import sys
import asyncio

from meat import Meat

OPTIONS = ["MEAT_MODEL_PATH", "MEAT_TRANSLATE_KEY", "MEAT_TRANSLATE_REGION", "MEAT_TRANSLATE_ENDPOINT"]


async def main():
    options = {}

    for option in OPTIONS:
        val = os.getenv(option)
        if val == "":
            sys.exit(f"${option} is a required option that is missing")

        options[option] = val

    client = Meat(options=options)
    async with client:
        token = os.getenv("MEAT_TOKEN")
        if token is None:
            sys.exit("$MEAT_TOKEN is not set")

        await client.start(token)


if __name__ == "__main__":
    asyncio.run(main())
