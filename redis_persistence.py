import pickle
import os
from urllib.parse import urlparse
from collections import defaultdict
from copy import deepcopy
from typing import Any, DefaultDict, Dict, Optional, Tuple
from redis import Redis, from_url

from telegram.ext import BasePersistence


class RedisPersistence(BasePersistence):

    def __init__(
        self,
        url: str,
        store_user_data: bool = True,
        store_chat_data: bool = True,
        store_bot_data: bool = True
        ):

        super().__init__(store_user_data= store_user_data, store_chat_data= store_chat_data, store_bot_data= store_bot_data)
        redis_url = urlparse(url)
        self.redis: Redis = Redis(host=redis_url.hostname, port=redis_url.port, username=redis_url.username, password=redis_url.password, ssl=True, ssl_cert_reqs=None)
        self.user_data: Optional[DefaultDict[int, Dict]] = None
        self.chat_data: Optional[DefaultDict[int, Dict]] = None
        self.bot_data: Optional[Dict] = None
        self.conversations: Optional[Dict[str, Dict]] = None

    def load_redis(self) -> None:
        try:
            data_bytes = self.redis.get('TelegramBotPersistence')
            if data_bytes:
                data = pickle.loads(data_bytes)
                self.user_data = defaultdict(dict, data['user_data'])
                self.chat_data = defaultdict(dict, data['chat_data'])
                self.bot_data = data.get('bot_data', {})
                self.conversations = data['conversations']
            else:
                self.conversations = dict()
                self.user_data = defaultdict(dict)
                self.chat_data = defaultdict(dict)
                self.bot_data = {}
        except Exception as ex:
            raise TypeError(f"Something went wrong unpickling from Redis") from ex

    def dump_redis(self) -> None:
        data = {
            'conversations': self.conversations,
            'user_data': self.user_data,
            'chat_data': self.chat_data,
            'bot_data': self.bot_data,
        }
        data_bytes = pickle.dumps(data)
        self.redis.set('TelegramBotPersistence', data_bytes)

    def get_user_data(self) -> DefaultDict[int, Dict[Any, Any]]:
        if self.user_data:
            pass
        else:
            self.load_redis()
        return deepcopy(self.user_data)

    def get_chat_data(self) -> DefaultDict[int, Dict[Any, Any]]:
        if self.chat_data:
            pass
        else:
            self.load_redis()
        return deepcopy(self.chat_data)

    def get_bot_data(self) -> Dict[Any, Any]:
        if self.bot_data:
            pass
        else:
            self.load_redis()
        return deepcopy(self.bot_data)

    def get_conversations(self, name: str) -> DefaultDict[str, Dict]:
        if self.conversations:
            pass
        else:
            self.load_redis()
        return self.conversations.get(name, {}).copy()  # type: ignore[union-attr]

    def update_conversation(self, name: str, key: Tuple[int, ...], new_state: Optional[object]) -> None:
        if not self.conversations:
            self.conversations = dict()
        if self.conversations.setdefault(name, {}).get(key) == new_state:
            return
        self.conversations[name][key] = new_state
        self.dump_redis()

    def update_user_data(self, user_id: int, data: Dict) -> None:
        if self.user_data is None:
            self.user_data = defaultdict(dict)
        if self.user_data.get(user_id) == data:
            return
        self.user_data[user_id] = data
        self.dump_redis()

    def update_chat_data(self, chat_id: int, data: Dict) -> None:
        if self.chat_data is None:
            self.chat_data = defaultdict(dict)
        if self.chat_data.get(chat_id) == data:
            return
        self.chat_data[chat_id] = data
        self.dump_redis()

    def update_bot_data(self, data: Dict) -> None:
        if self.bot_data == data:
            return
        self.bot_data = data.copy()
        self.dump_redis()

    def flush(self) -> None:
        self.dump_redis()
