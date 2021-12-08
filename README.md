# Bot-Reviews
Script to get reviews from App Store (iOS) and Google Play (Android). This is a scraper to user reviews in stores makes in python. All reviews are stored in the database SQLite to query and also are posted in Teams channel. 

This project is heavily inspired by [App-Reviews](https://github.com/armanso/app-reviews)

## Installation
    pip3 install -r requirements.txt 

## Configuration
It needs to set up config/config.json as template: [config_template.json](config/config_template.json):

### Options
All bellow options are required: 

-   **teamsHook:**  URL to your webhook teams channel
-   **logLevel:**  Level for logging terminal [debug, info, warn, error] 
-   **intervalInSeconds:**  Interval of seconds to retry getting user reviews
-   **dryRun:** If true it's only saving user reviews in database and don't post in teams channel 
-   **report:** Report object
-   **appsAndroid:**  List of AppAndroid object
-   **appsIos:**  List of AppIos object

**Report** object definition:
-   **intervalInDays:** Interval of days to generate report
-   **firebaseKey:** Path to Firebase Key
-   **firebaseKey:** Project ID

Firebase is using to save wordcloud images

**AppAndroid** object definition:
-   **appId:** Bundle ID of application
-   **playStoreKey:** Path to Play Store Console Key 

**AppIos** object definition:
-   **appId:** App ID of application (only numbers)
-   **appStoreKeyId:** Key ID column after generate App Store Connect API
-   **appStoreKey:** Path to private key generate in App Store Connect API
-   **appStoreIssuerId:** Private issuer ID generate in App Store Connect API

