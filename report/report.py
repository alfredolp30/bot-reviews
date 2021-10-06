from io import BytesIO
import logging
from PIL import Image
import base64
from config.configmanager import ConfigManager
from db.appstore_dao import AppStoreDao
from db.db_manager import DBManager
from db.playstore_dao import PlayStoreDao
import datetime
from wordcloud import WordCloud

from pathlib import Path

from notify.msteams import MSTeams
from report.firebase_bucket import FirebaseBucket
from report.platform import Platform



class Report: 
    REPORT_FOLDER = "wordcloud"
    SEPARATOR = "/"
    WORDCLOUD_FILE = '{}_{}_{}_wc.png'

    def __init__(self, dbManager: DBManager, configManager: ConfigManager, msTeams: MSTeams, firebaseBucket: FirebaseBucket) -> None:
        self.appStoreDao = AppStoreDao(dbManager)
        self.playStoreDao = PlayStoreDao(dbManager)
        self.appsIos = configManager.getValueFromConfig('appsIos')
        self.appsAndroid = configManager.getValueFromConfig('appsAndroid')
        self.intervalReportInDays = configManager.getValueFromConfig('report/intervalInDays')
        self.msTeams = msTeams
        self.firebaseBucket = firebaseBucket


    def __createFilename(self, platform: Platform, appName: str) -> str: 
        strDatetime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        return self.WORDCLOUD_FILE.format(appName.replace(' ', '-'), platform.value, strDatetime)


    def __generateWordCloudImageUri(self, platform: Platform, appName: str, text: str) -> str:
        wordCloud = WordCloud(width=1024, height=720).generate(text)

        Path(self.REPORT_FOLDER).mkdir(parents=True, exist_ok=True)
        filename = self.__createFilename(platform, appName)
        filepath = self.REPORT_FOLDER + self.SEPARATOR + filename
        
        wordCloud.to_file(filepath)

        if self.firebaseBucket.isActive():
            imageUri = self.firebaseBucket.saveFirebaseImage(filepath, filename)
        else:
            with Image.open(filename) as imageWordCloud:
                imageResized = imageWordCloud.resize(size=(100, 50))
                buffered = BytesIO()
                imageResized.save(buffered, format="PNG")
                imageBase64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            imageUri = "data:image/png;charset=utf-8;base64,{}".format(imageBase64)
        

        logging.debug("generate word cloud URI: {}".format(imageUri))

        return imageUri
    
    def generateReport(self, platform: Platform) -> None:
        date = datetime.datetime.now() - datetime.timedelta(days=self.intervalReportInDays)

        apps = self.appsIos if platform == Platform.ios else self.appsAndroid
        dao = self.appStoreDao if platform == Platform.ios else self.playStoreDao
        

        for app in apps:
            appId = app['appId']
            reviews = dao.getReviewsByDate(appId, int(date.timestamp()))
            reviewCount = len(reviews)

            if reviewCount == 0:
                continue

            ratingSum = 0
            descriptions = "" 

            for review in reviews:
                ratingSum += review.rating
                descriptions += " {}".format(review.description)
        
            appName = reviews[0].appName
            iconUrl = reviews[0].iconUrl

            ratingAvg = "{:.2f}".format(ratingSum / reviewCount)

            logging.debug("{} rating average: {}".format(appName, ratingAvg)) 

            imageUri = self.__generateWordCloudImageUri(platform, appName, descriptions)

            self.msTeams.postReport(appName, platform, iconUrl, self.intervalReportInDays, ratingAvg, imageUri)