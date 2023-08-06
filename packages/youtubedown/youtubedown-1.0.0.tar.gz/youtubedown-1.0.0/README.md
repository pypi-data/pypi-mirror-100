# mcuser


![PYTHON](https://img.shields.io/badge/python-v3.8-blue)
> Asynchronous download using a simple created youtube_dl.

> testing python version 3.8



## Asynchronous
```py
import asyncio
from youtubedown import asyncdown


async def main():
    Main = await asyncdown.lookup(title="My Songs title or url", nick="music")
    download = await Main.download() #return json
    search = await Main.search() #retrun json

asyncio.run(main())
```

