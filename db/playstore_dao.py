from db.db_manager import DBManager
from model.review_appstore import ReviewAppstore
from model.review_playstore import ReviewPlayStore


class PlayStoreDao:

    def __init__(self, dbManager: DBManager) -> None:
        self.tableName = "playstore"
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
                description "TEXT",
                rating "INTEGER",
                iconUrl "TEXT",
                device "TEXT",
                deviceProductName "TEXT",
                androidOsVersion "TEXT"
            )
        '''.format(self.tableName)

        self.dbManager.createTable(createTable)

    
    def save(self, review: ReviewPlayStore) -> None:
        self.dbManager.insert(self.tableName, review.asJson())

    def contains(self, review: ReviewPlayStore) -> bool:
        return self.dbManager.contains(self.tableName, "id", "'{}'".format(review.id))

    def getReviewsByDate(self, appId: str, date: int) -> list[ReviewPlayStore]:
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
            description = value[7]
            rating = value[8]
            iconUrl = value[9]
            device = value[10]
            deviceProductName = value[11]
            androidOsVersion = value[12]

            reviews.append(
                ReviewPlayStore(
                    id, 
                    appId,
                    appName, 
                    appVersion, 
                    url, 
                    author, 
                    date, 
                    description, 
                    rating, 
                    iconUrl,
                    device, 
                    deviceProductName,
                    androidOsVersion
                )
            )

        return reviews