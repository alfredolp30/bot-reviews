from datetime import datetime
from db.db_manager import DBManager
from model.review_appstore import ReviewAppstore


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

    
    def save(self, review: ReviewAppstore):
        self.dbManager.insert(self.tableName, review.asJson())

    def contains(self, review: ReviewAppstore) -> bool:
        return self.dbManager.contains(self.tableName, "id", "'{}'".format(review.id))

    def getReviewsByDate(self, appId: str, date: int) -> list[ReviewAppstore]:
        values = self.dbManager.get(self.tableName, "appId='{}' and date>='{}'".format(appId, date), orderBy = "date")
        
        reviews = []

        for value in values: 
            id = value[0]
            appId = value[1]
            appName = value[2]
            appVersion = value[3]
            url = value[4]
            author = value[5]
            date = value[6]
            title = value[7]
            description = value[8]
            rating = value[9]
            region = value[10]
            iconUrl = value[11]

            reviews.append(ReviewAppstore(
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
                iconUrl))

        return reviews