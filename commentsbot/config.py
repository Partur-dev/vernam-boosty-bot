import os


class Config:
    BOT_TOKEN: str
    SUBSCRIBERS_CHAT_ID: str
    PAID_CHATS: list[str]

    def __load(self, name: str):
        value = os.environ.get(name)
        if not value:
            raise KeyError(f"not {name} in env")
        return value

    def __init__(self) -> None:
        self.BOT_TOKEN = self.__load("BOT_TOKEN")
        self.SUBSCRIBERS_CHAT_ID = self.__load("SUBSCRIBERS_CHAT_ID")
        self.PAID_CHATS = self.__load("PAID_CHATS").split(",")


config = Config()
