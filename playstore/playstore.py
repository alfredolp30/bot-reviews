import logging

from datetime import datetime

from google.oauth2 import service_account
import googleapiclient.discovery
from model.review_playstore import ReviewPlayStore


class PlayStore:
    SCOPES = ['https://www.googleapis.com/auth/androidpublisher']

    def __init__(self, appId, playStoreKey):
        self.appId = appId
        self.playStoreKey = playStoreKey

    def getReviews(self):
        self.__scraperAppNameAndIcon()

        credentials = service_account.Credentials.from_service_account_file(self.playStoreKey, scopes=self.SCOPES)
        service = googleapiclient.discovery.build("androidpublisher", "v3", credentials=credentials, cache_discovery=False)
        response = service.reviews().list(packageName = self.appId).execute()
        
        reviewsPlayStore = []
        if isinstance(response, dict):
            reviewsPlayStore = self.__getReviews(response)
        else: 
            logging.error('Not load json from google api')

        reviewsPlayStore.sort(key=lambda x: x.date, reverse=True)

        return reviewsPlayStore

    def __getReviews(self, resultJson): 
        reviewsPlayStore = []

        reviews = resultJson['reviews']

        for review in reviews:
            reviewId = review['reviewId']
            authorName = review.get('authorName', '')
            comments = review['comments']

            commentCounter = 1

            for comment in comments:
                if 'userComment' not in comment:
                    continue

                userComment = comment['userComment']
                reviewPlayStore = self.__jsonToReviewPlayStore(commentCounter, reviewId, authorName, entryJson = userComment)

                if reviewPlayStore != None:
                    commentCounter += 1
                    reviewsPlayStore.append(reviewPlayStore)
        
        return reviewsPlayStore


    def __scraperAppNameAndIcon(self): 
        from google_play_scraper import app
        result = app(self.appId)

        try:
            self.appName = result['title']
            self.iconUrl = result['icon']
        except:
            self.appName = ''
            self.iconUrl = ''

    def __jsonToReviewPlayStore(self, commentCounter, reviewId, authorName, entryJson): 
        try: 

            ts = int(entryJson['lastModified']['seconds'])
            deviceMetada = entryJson.get('deviceMetadata', None)

            appId = self.appId
            appName = self.appName
            appVersion = entryJson.get('appVersionName', '')
            url = self.__createUrl(reviewId)
            author = authorName
            date = datetime.utcfromtimestamp(ts)
            description = entryJson['text'].removeprefix('\t')
            rating = entryJson['starRating']
            iconUrl = self.iconUrl
            device = entryJson.get('device', '')
            deviceProductName = deviceMetada['productName'] if deviceMetada != None else ''
            androidOsVersion = entryJson.get('androidOsVersion', '')

            id = '{} review: {}'.format(reviewId, commentCounter)

            return ReviewPlayStore(id, appId, appName, appVersion, url, author, date, description, rating, iconUrl, device, deviceProductName, androidOsVersion)
        except Exception as e:
            logging.warn('error parse json {}'.format(e))
        
        return None

    def __createUrl(self, reviewId):
        from urllib import parse
        parameters = parse.urlencode( {'id': self.appId,'reviewId':reviewId } )
        return "https://play.google.com/store/apps/details?{}".format(parameters)