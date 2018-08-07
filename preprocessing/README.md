## Preporcessing Steps for DSFG Parking Project
This project analyzes three different methods of detecting car occupancy:
1. Machine Learning Algorithm
2. Crowdsourcing with Automan
3. Park Mobile Data
Each of these three algorthms require varying preprocessing steps. 

### Scope of Data
In this trial study, we collected 24-hours of images every 60 seconds of the Main Street parking log in downtown Amherst. All of the images are hosted on https://www.cameraftp.com/. Therefore, one of the preprocessing steps was to download all of the folders from the cloud and sample images every 15-minutes between 6AM and 8PM.

### Preprocessing Process for each Method
* Machine Learning Algorithm
    * TBD
* Crowdsourcing with Automan
    1. `townhall-data\preprocess-townhall-data.py`: Preprocess the entire dataset from the CameraFTP server. This script executes the following:
        * loops through each folder in `day-by-day\mm-dd`
        * unzips all of the pictures from compressed folders
        * deletes all files outside of a 15-minute increment between 6AM and 8PM
        * copies all files to specified folder in Google Drive
    2. `townhall-data\links-for-automan\list-parking-links.py`: Create a list of links from the Google Drive folder using the [Google Drive API](https://developers.google.com/drive/)
        * cycles through every file in the specified Google Drive folder ID
        * writes the link with the file ID in the **https://drive.google.com/uc?id=xxxxx** format

