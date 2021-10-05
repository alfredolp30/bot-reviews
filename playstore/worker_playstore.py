import logging
from playstore.playstore import PlayStore
from db.playstore_dao import PlayStoreDao

class WorkerPlayStore:
    def __init__(self, configManager, dbManager, msTeams) -> None:
        self.configManager = configManager
        self.playStoreDao = PlayStoreDao(dbManager)
        self.msTeams = msTeams

    def __workReview(self, appId, playStoreKey): 
        
        reviews = PlayStore(appId, playStoreKey).getReviews()

        print(reviews)

        for review in reviews:
            contains = self.playStoreDao.contains(review)

            if not contains:
                self.playStoreDao.save(review)
                self.msTeams.postReviewPlayStore(review)
            else:
                logging.debug("Contains review with id {}".format(review.id))
                break

    def run(self): 
        apps = self.configManager.getValueFromConfig("apps_android")
        
        for app in apps:
            try: 
                appId = app['appId']
                playStoreKey = app['playStoreKey']

                self.__workReview(appId, playStoreKey)
            except Exception as e:
                logging.error("key not found {}".format(e))