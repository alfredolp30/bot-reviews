from playstore.worker_playstore import WorkerPlayStore
from report.firebase_bucket import FirebaseBucket
from report.platform import Platform
from report.report import Report
from db.db_manager import DBManager
from notify.msteams import MSTeams
import time
import threading
import logging
from logger import setLogging
from config.configmanager import ConfigManager
from appstore.worker_appstore import WorkerAppStore

configManager = ConfigManager()
msTeams = MSTeams(configManager)

logLevel = configManager.getValueFromConfig('logLevel') 
intervalInSeconds = configManager.getValueFromConfig('intervalInSeconds')

setLogging(logLevel)


def getReviewsIos():
    while True:
        dbManager = DBManager()
        logging.debug("run works to get reviews from App Store")
        WorkerAppStore(configManager, dbManager, msTeams).run()

        logging.debug("sleep for {}".format(intervalInSeconds))
        time.sleep(intervalInSeconds)


def getReviewsAndroid():
    while True:
        dbManager = DBManager()
        logging.debug("run works to get reviews from Play Store")
        WorkerPlayStore(configManager, dbManager, msTeams).run()

        logging.debug("sleep for {}".format(intervalInSeconds))
        time.sleep(intervalInSeconds)


def getReports():
    firebaseBucket = FirebaseBucket(configManager)

    while True:
        dbManager = DBManager()
        logging.debug("run work to get reports")
        report = Report(dbManager, configManager, msTeams, firebaseBucket)

        reportIntervalInSeconds = report.intervalReportInDays * 24 * 60 * 60
        logging.debug("sleep for {}".format(reportIntervalInSeconds))

        report.generateReport(Platform.android)
        report.generateReport(Platform.ios)
        
        time.sleep(reportIntervalInSeconds)



t1 = threading.Thread(target=getReviewsIos)
t1.start()

t2 = threading.Thread(target=getReviewsAndroid)
t2.start()

t3 = threading.Thread(target=getReports)
t3.start()