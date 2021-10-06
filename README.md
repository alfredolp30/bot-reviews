# Bot-Reviews
Script to get reviews from App Store (iOS) and Google Play (Android). This python script is a scraper to user reviews in stores. All reviews are stored in the database SQLite for reports and also are posted in Teams channel. 

This project is heavily inspired by [App-Reviews](https://github.com/armanso/app-reviews)


## Installation

    pip3 install -r requirements.txt 

## Configuration
It needs to create config/config.json as template: [config_template.json](config/config_template.json):

### Options
All bellow options are required: 

-   **teamsHook:**  URL to your webhook teams channel
-   **logLevel:**  Level for logging terminal [debug, info, warn, error] 
-   **intervalInSeconds:**  Interval to retry getting list of latest user reviews list from store
-   **apps_android:**  List of AppAndroid  
-   **apps_ios:**  List of AppIos
