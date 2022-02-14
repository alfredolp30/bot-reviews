import pymsteams
import logging

from config.configmanager import ConfigManager
from model.review_appstore import ReviewAppStore
from model.review_playstore import ReviewPlayStore
from report.platform import Platform

class MSTeams:
    def __init__(self, configManager: ConfigManager) -> None:
        self.hook = configManager.getValueFromConfig("teamsHook")
        self.dryRun = configManager.getValueFromConfig("dryRun")

    def __getColor(self, rating: int) -> str: 
        if rating >= 4: 
            color = "2DB985" 
        elif rating >= 2:
            color = "DA9F38"
        else:
            color = "A30101"
        
        return color
    
    def __getRatingTitle(self, rating: int, title: str) -> str:
        ratingTitle = ""

        for i in range(0, 5, 1):
            if i < rating:
                ratingTitle += "★"
            else:
                ratingTitle += "☆"
    
        if title != None: 
            return "{} - {}".format(ratingTitle, title)
        else:
            return "{}".format(ratingTitle)

    def __postTeamsMessage(self, teamsMessage: pymsteams.connectorcard): 
        if self.dryRun:
            logging.debug(teamsMessage.payload)
            return

        try: 
            teamsMessage.send()
        except Exception as e:
            logging.error("dont send to teams {}".format(e))

    def postReviewAppStore(self, reviewAppStore: ReviewAppStore) -> None:
        logging.debug("postReviewAppStore")
        teamsMessage = pymsteams.connectorcard(self.hook)


        color = self.__getColor(reviewAppStore.rating)
        teamsMessage.color(color)

        title = self.__getRatingTitle(reviewAppStore.rating, reviewAppStore.title)
        teamsMessage.summary("summary")
        
        messageSection = pymsteams.cardsection()
        messageSection.activityTitle(title)
        messageSection.activitySubtitle(reviewAppStore.author)
        messageSection.text(reviewAppStore.description)
        messageSection.activityImage(reviewAppStore.iconUrl)
        messageSection.addFact("App Name", reviewAppStore.appName)
        messageSection.addFact("Platform", "iOS")
        messageSection.addFact("Store", "App Store")
        messageSection.addFact("App Version", reviewAppStore.appVersion)
        messageSection.linkButton("More details", reviewAppStore.url)

        teamsMessage.addSection(messageSection)

        self.__postTeamsMessage(teamsMessage)


    def postReviewPlayStore(self, reviewPlayStore: ReviewPlayStore) -> None:
        logging.debug("postReviewAppStore")
        teamsMessage = pymsteams.connectorcard(self.hook)


        color = self.__getColor(reviewPlayStore.rating)
        teamsMessage.color(color)

        title = self.__getRatingTitle(reviewPlayStore.rating, None)
        teamsMessage.summary("summary")
        
        messageSection = pymsteams.cardsection()
        messageSection.activityTitle(title)
        messageSection.activitySubtitle(reviewPlayStore.author)
        messageSection.text(reviewPlayStore.description)
        messageSection.activityImage(reviewPlayStore.iconUrl)
        messageSection.addFact("App Name", reviewPlayStore.appName)
        messageSection.addFact("Platform", "Android")
        messageSection.addFact("Store", "Play Store")
        messageSection.addFact("App Version", reviewPlayStore.appVersion)
        messageSection.addFact("Device Codename", reviewPlayStore.device)
        messageSection.addFact("Device Market Name", reviewPlayStore.deviceProductName)
        messageSection.addFact("Android Version", reviewPlayStore.androidOsVersion)
        messageSection.linkButton("More details", reviewPlayStore.url)

        teamsMessage.addSection(messageSection)

        self.__postTeamsMessage(teamsMessage)


    def postReport(self, appName: str, platform: Platform, iconUrl: str, periodInDays: int, ratingAverage: str, imageUri: str) -> None:
        teamsMessage = pymsteams.connectorcard(self.hook)
        teamsMessage.summary("summary")

        messageSection = pymsteams.cardsection()
        messageSection.activityTitle("Report")
        messageSection.activitySubtitle("Last {} days".format(periodInDays))
        messageSection.activityImage(iconUrl)
        messageSection.addFact("App Name", appName)
        messageSection.addFact("Platform", platform.value)
        messageSection.addFact("Rating Average", ratingAverage)
        messageSection.addImage(imageUri)

        if imageUri.startswith("https://"): 
             messageSection.linkButton("See image", imageUri)

        teamsMessage.addSection(messageSection)

        self.__postTeamsMessage(teamsMessage)