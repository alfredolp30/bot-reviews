import logging
from model.review_appstore import ReviewAppStore
import requests
import json
from datetime import datetime

from appstoreconnect import Api


class AppStore:

    HEADERS = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0',
        'Cache-Control': 'no-cache'
    }

    URL_REVIEW = "https://itunes.apple.com/{}/rss/customerreviews/page={}/id={}/sortBy=mostRecent/json"
    URL_ICON = "http://itunes.apple.com/lookup?id={}&country={}"

    def __init__(self, appId: str, appStoreKeyId: str, appStoreKey: str, appStoreIssuerId: str, regions: dict, lastDate: datetime):
        self.appId = appId
        self.regions = regions
        self.appStoreKeyId = appStoreKeyId
        self.appStoreKey = appStoreKey
        self.appStoreIssuerId = appStoreIssuerId
        self.lastDate = lastDate


    def __getAppNameAndBundleId(self) -> None:
        api = Api(self.appStoreKeyId, self.appStoreKey, self.appStoreIssuerId)
        app = api.read_app_information(self.appId)
        self.appName = app.name
        
        indexBeforeHifen = app.primaryLocale.find('-') + 1
        self.defaultRegion = app.primaryLocale[indexBeforeHifen:].lower()


    def __getIconUrl(self) -> None:
        url = self.URL_ICON.format(self.appId, self.defaultRegion)
        logging.debug("url: {}".format(url))

        response = requests.get(url, headers=self.HEADERS)

        self.iconUrl = ''
        if response.status_code == 200: 
            try: 
                responseJson = json.loads(response.text)
                self.iconUrl = responseJson['results'][0]['artworkUrl512']
            except Exception as e:
                logging.error('Cannot get icon URL {}', e)

        


    def __jsonToReviewAppStore(self, entryJson: dict, region: str) -> ReviewAppStore:
        try:
            id = entryJson['id']['label']
            appId = self.appId
            appName = self.appName
            appVersion = entryJson['im:version']['label']
            url = entryJson['author']['uri']['label']
            author = entryJson['author']['name']['label']
            date = datetime.strptime(entryJson['updated']['label'], '%Y-%m-%dT%H:%M:%S%z')
            title = entryJson['title']['label']
            description = entryJson['content']['label']
            rating = int(entryJson['im:rating']['label'])
            iconUrl = self.iconUrl
            
            return ReviewAppStore(
                id, 
                appId, 
                appName, 
                appVersion, 
                url, 
                author, 
                date, 
                title, 
                description, 
                rating, 
                region, 
                iconUrl
            )

        except Exception as e: 
            logging.error("error parser json {}".format(e))

        return None

    def getReviews(self) -> list[ReviewAppStore]:
        self.__getAppNameAndBundleId()
        self.__getIconUrl()

        reviewsAppstore = []

        for region in self.regions:
            reviewsAppstore += self.__getReviews(region)

        reviewsAppstore.sort(key=lambda x: x.date, reverse=True)

        return reviewsAppstore

    def __getReviews(self, region: str) -> list[ReviewAppStore]:
        reviewsAppstore = []
        page = 1

        while page >= 1:
            url = self.URL_REVIEW.format(region, page, self.appId)
            logging.debug("url: {}".format(url))

            response = requests.get(url, headers=self.HEADERS)

            if response.status_code == 200: 
                entriesJson = None
                try: 
                    responseJson = json.loads(response.text)
                    entriesJson = responseJson['feed']['entry']
                except:
                    entriesJson = None
                
                if entriesJson != None: 
                    if not type(entriesJson) is list:
                        entriesJson = [entriesJson]

                    for entryJson in entriesJson: 
                        reviewIos = self.__jsonToReviewAppStore(entryJson, region)
                        if reviewIos != None:
                            reviewsAppstore.append(reviewIos)
                            logging.debug(reviewIos.date)

                    page += 1
                else:
                    page = 0
            else: 
                page = 0
            

            if len(reviewsAppstore) > 0:
                lastReview = reviewsAppstore[-1]
            else: 
                lastReview = None

            # TODO break if newest is saved 
            #if lastReview and self.lastDate and lastReview.date.timestamp() < self.lastDate.timestamp():
            #    page = 0

        
        return reviewsAppstore 


    