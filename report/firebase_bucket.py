from config.configmanager import ConfigManager

import firebase_admin
from firebase_admin import credentials, storage


class FirebaseBucket:
    FIREBASE_FOLDER = "bot-reviews"
    SEPARATOR = "/"

    def __init__(self, configManager: ConfigManager) -> None:
        firebaseKey = configManager.getValueFromConfig('report/firebaseKey')
        firebaseProject = configManager.getValueFromConfig('report/firebaseProject')
        self.__initializeFirebaseApp(firebaseKey, firebaseProject)

    
    def __initializeFirebaseApp(self, firebaseKey, firebaseProject) -> None: 
        if firebaseKey and firebaseProject and not firebase_admin._apps:
            cred = credentials.Certificate(firebaseKey)
            self.firebaseApp = firebase_admin.initialize_app(cred, {
                'storageBucket': '{}.appspot.com'.format(firebaseProject),
            }, name='storage')
    
    def saveFirebaseImage(self, filepath, filename) -> str: 
        if self.firebaseApp:
            bucket = storage.bucket(app=self.firebaseApp)
            blob = bucket.blob(self.FIREBASE_FOLDER + self.SEPARATOR  + filename)

            blob.upload_from_filename(filepath)
            blob.make_public()

            return blob.public_url
        
        return ''

    def isActive(self) -> bool:
        return self.firebaseApp 
