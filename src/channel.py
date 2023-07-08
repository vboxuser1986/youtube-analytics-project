import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        data = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()['items'][0]

        self.__title = data['snippet']['title']
        self.__description = data['snippet']['description']
        self.__url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.__subscriber_count = int(data['statistics']['subscriberCount'])
        self.__video_count = data['statistics']['videoCount']
        self.__viewCount = data['statistics']['viewCount']

    def __str__(self):
        """Возвращает название  и ссылку по шаблону"""
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """Возвращает сумму подписчиков каналов"""
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        """Возвращает разность подписчиков каналов"""
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        """Возвращает результат сравнения подписчиков каналов"""
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        """Возвращает результат сравнения подписчиков каналов"""
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        """Возвращает результат сравнения подписчиков каналов"""
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        """Возвращает результат сравнения подписчиков каналов"""
        return self.subscriber_count <= other.subscriber_count

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def url(self):
        return self.__url

    @property
    def subscriber_count(self):
        return self.__subscriber_count

    @property
    def video_count(self):
        return self.__video_count

    @property
    def view_count(self):
        return self.__viewCount

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, filename: str) -> None:
        """Сохраняет в файл значения атрибутов экземпляра `Channel`"""
        data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "viewCount": self.view_count
        }

        with open(filename, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=3))
