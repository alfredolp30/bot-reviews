from datetime import datetime
import logging
from db.db_manager import DBManager
from model.review_appstore import ReviewAppStore


class AppStoreDao:

    def __init__(self, dbManager: DBManager) -> None:
        self.tableName = "appstore"
        self.dbManager = dbManager
        self.__createTable()
    
    def __createTable(self) -> None: 
        createTable = '''
            CREATE TABLE IF NOT EXISTS {} (
                id "TEXT" PRIMARY KEY,
                appId "TEXT",
                appName "TEXT",
                appVersion "TEXT",
                url "TEXT",
                author "TEXT",
                date "INTEGER",
                title "TEXT",
                description "TEXT",
                rating "INTEGER",
                region "TEXT",
                iconUrl "TEXT"
            )
        '''.format(self.tableName)

        self.dbManager.createTable(createTable)
    
    def save(self, review: ReviewAppStore):
        self.dbManager.insert(self.tableName, review.asJson())

    def contains(self, review: ReviewAppStore) -> bool:
        return self.dbManager.contains(self.tableName, where="appId='{}' and id='{}'".format(review.appId, review.id))

    def getReviewsByDate(self, appId: str, date: int) -> list[ReviewAppStore]:
        values = self.dbManager.get(self.tableName, where="appId='{}' and date>={}".format(appId, date), orderBy = "date")
        
        reviews = []

        for value in values: 
            reviews.append(self.__valueToReview(value))

        return reviews

    def __valueToReview(self, value: list[any]) -> ReviewAppStore:
        id = value[0]
        appId = value[1]
        appName = value[2]
        appVersion = value[3]
        url = value[4]
        author = value[5]
        date = datetime.utcfromtimestamp(value[6])
        title = value[7]
        description = value[8]
        rating = value[9]
        region = value[10]
        iconUrl = value[11]

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

    def lastReview(self, appId) -> ReviewAppStore:  
        values = self.dbManager.get(self.tableName, where="appId='{}'".format(appId), orderBy = "date", limit=1)

        if len(values) > 0:
            value = values[0]
            return self.__valueToReview(value)
        else:
            logging.warning("Error getting first ReviewAppStore")
            return None