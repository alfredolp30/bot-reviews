from datetime import datetime


class ReviewAppStore:
    
    def __init__(self, id: str, appId: str, appName: str, appVersion: str, url: str, author: str, date: datetime, title: str, description: str, rating: int, region: str, iconUrl: str):
        self.id = id
        self.appId = appId
        self.appName = appName
        self.appVersion = appVersion
        self.url = url
        self.author = author
        self.date = date
        self.title = title
        self.description = description
        self.rating = rating
        self.region = region
        self.iconUrl = iconUrl

    def asJson(self) -> dict:
        return {
            'id': self.id,
            'appId': self.appId,
            'appName': self.appName,
            'appVersion': self.appVersion,
            'url': self.url,
            'author': self.author,
            'date': int(self.date.timestamp()),
            'title': self.title,
            'description': self.description,
            'rating': self.rating,
            'region': self.region,
            'iconUrl': self.iconUrl
        }