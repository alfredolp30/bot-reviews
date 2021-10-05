from datetime import datetime


class ReviewPlayStore:
    
    def __init__(self, id: str, appId: str, appName: str, appVersion: str, url: str, author: str, date: datetime, description: str, rating: int, iconUrl: str, device: str, deviceProductName: str, androidOsVersion: str):
        self.id = id
        self.appId = appId
        self.appName = appName
        self.appVersion = appVersion
        self.url = url
        self.author = author
        self.date = date
        self.description = description
        self.rating = rating
        self.iconUrl = iconUrl
        self.device = device
        self.deviceProductName = deviceProductName
        self.androidOsVersion = androidOsVersion

    def asJson(self) -> dict:
        return {
            'id': self.id,
            'appId': self.appId,
            'appName': self.appName,
            'appVersion': self.appVersion,
            'url': self.url,
            'author': self.author,
            'date': self.date,
            'description': self.description,
            'rating': self.rating,
            'iconUrl': self.iconUrl,
            'device': self.device,
            'deviceProductName': self.deviceProductName,
            'androidOsVersion': self.androidOsVersion
        }