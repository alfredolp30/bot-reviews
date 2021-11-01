from appstore.appstore import AppStore
import logging
from config.configmanager import ConfigManager
from db.appstore_dao import AppStoreDao
from db.db_manager import DBManager
from model.review_appstore import ReviewAppStore
from notify.msteams import MSTeams

class WorkerAppStore:
    def __init__(self, configManager: ConfigManager, dbManager: DBManager, msTeams: MSTeams) -> None:
        self.configManager = configManager
        self.appStoreDao = AppStoreDao(dbManager)
        self.msTeams = msTeams

    def __workReview(self, appId: str, appStoreKeyId: str, appStoreKey: str, appStoreIssuerId: str, regions: dict) -> None: 
        
        lastReview = self.appStoreDao.lastReview(appId)
        lastDate = lastReview.date if lastReview else None
        reviews = AppStore(appId, appStoreKeyId, appStoreKey, appStoreIssuerId, regions, lastDate).getReviews()

        for review in reviews:
            contains = self.appStoreDao.contains(review)

            if not contains:
                self.appStoreDao.save(review)
                self.msTeams.postReviewAppStore(review)
            else:
                logging.debug("Contains review #{} with id {}".format(reviews.index(review), review.id))
                break

    def run(self) -> None: 
        apps = self.configManager.getValueFromConfig("appsIos")
        regions = self.configManager.getRegions() 
        
        for app in apps:
            try: 
                appId = app['appId']
                appStoreKeyId = app['appStoreKeyId'] 
                appStoreKey = app['appStoreKey']
                appStoreIssuerId = app['appStoreIssuerId']

                self.__workReview(appId, appStoreKeyId, appStoreKey, appStoreIssuerId, regions)
            except Exception as e:
                logging.error("key not found {}".format(e))