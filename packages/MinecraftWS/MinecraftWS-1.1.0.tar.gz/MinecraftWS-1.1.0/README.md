# MinecraftWS
![PyPI](https://img.shields.io/pypi/v/MinecraftWS)

Minecraft Bedrock Websocket

## Install
```shell
pip install MinecraftWS
```

## Example
```python
from MinecraftWS import MinecraftWS, Event

class WS(MinecraftWS):
    async def on_connect(self):
        self.add_event(Event.BlockPlaced)

    async def on_event(self, event: str, properties: dict):
        if event == Event.BlockPlaced:
            print(properties)
```