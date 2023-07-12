import os
from googleapiclient.discovery import build
from datetime import timedelta
import isodate


class PlayList:
    """Класс плейлиста"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        """инициализация"""
        self.playlist_id = playlist_id
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.title = self.youtube.playlists().list(id=playlist_id,
                                                   part='snippet').execute()['items'][0]['snippet']['title']
        self.__data = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                        part='contentDetails, snippet',
                                                        maxResults=50,
                                                        ).execute()

        self.__videos_id = [video['contentDetails']['videoId'] for video in self.__data['items']]

        self.__videos_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                            id=','.join(self.__videos_id)
                                                            ).execute()

    def __str__(self):
        return self.playlist_id

    def __repr__(self):
        return f"PlayList({self.playlist_id}, {self.url})"

    @property
    def total_duration(self) -> timedelta:
        """возвращает объект класса datetime.timedelta с суммарной длительность плейлиста"""
        total_duration = timedelta()

        for video in self.__videos_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def total_seconds(self):
        """возвращает объект класса datetime.timedelta с суммарной длительность плейлиста в секундах"""
        return self.total_duration.seconds

    def show_best_video(self):
        """возвращает ссылку на самое популярное видео из плейлиста"""
        result_url = ''
        count_likes = 0

        for video in self.__videos_response['items']:
            if int(video['statistics']['likeCount']) > count_likes:
                count_likes = int(video['statistics']['likeCount'])
                result_url = f"https://youtu.be/{video['id']}"

        return result_url
