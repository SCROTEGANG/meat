# Meat

The half-baked genetic experiment of Shang Tsung. But more importantly, the one who got away. 💔

Made and ran for [SCROTEGANG](https://twitter.com/scrotegang).

# Running
You can run Meat using the provided [Docker image](https://github.com/SCROTEGANG/meat/pkgs/container/meat). However you will have to train your own GPT-2 model. Check out [aitextgen](https://github.com/minimaxir/aitextgen) for more info on doing that.

```sh
# Your Discord bot token
MEAT_TOKEN=wowafake.token
# Path to your trained model
MEAT_MODEL_PATH=/trained_model
# Azure text translation variables so Meat can speak Korean.
# See https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation-overview for more info.
MEAT_TRANSLATE_KEY=wowthisisfake
MEAT_TRANSLATE_REGION=westus2
MEAT_TRANSLATE_ENDPOINT=https://somelink.url
```

# License
[GPL](LICENSE)