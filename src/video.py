import os
from googleapiclient.discovery import build


class Video:
    """Класс видео"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        """инициализация"""
        self.video_id = video_id
        data = self.youtube.videos().list(id=self.video_id,
                                          part='snippet,contentDetails,statistics'
                                          ).execute()['items'][0]
        self.title = data['snippet']['title']
        self.url = f"https://youtu.be/{self.video_id}"
        self.count_views = data['statistics']['viewCount']
        self.count_likes = data['statistics']['likeCount']

    def __str__(self):
        """название видеон"""
        return self.title

    def __repr__(self):
        return f"Video({self.video_id}, {self.title}, {self.url}, {self.count_views}, {self.count_likes})"


class PLVideo(Video):
    """Класс плейлиста"""

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __repr__(self):
        return f"PLVideo({self.video_id}, {self.title}, {self.url}, {self.count_views}, " \
               f"{self.count_likes}, {self.playlist_id})"
