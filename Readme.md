# Y2B_to_Spot 

Code uses youtube API, to extract artists and song names from a given youtube playlist. A spotify playlist and extract identifier. (spotify API) 
The information from youtube is used to search through spotify for the spotify song identifier uri. (spotify API)
The uris are fed back to spotify API, to find the songs and add to the new spotify list. (spotify API)

# How to use: 

## Getting your OAuth Credentials from youtube:

1. sign up for a developer account via:  https://console.cloud.google.com/. You can find more information about creating an app and getting your access credentials here: https://developers.google.com/youtube/registering_an_application. 
2. Set up you email account as a user for the app when creating the app
3. Generate an OAuth 2.0 credential and download your secret file with credentials. Name your file: YOUR_CLIENT_SECRET_FILE.json and deposit at your code depository. 

## Getting your Spotify token and user ID: 

### Token: 

1. sign up for a developer account and visit https://developer.spotify.com/console/post-playlist-tracks 
2. Fill in the required fields and select generate token, make sure you check the boxes for both: 
- playlist-modify-public
- playlist-modify-private 

  under "Required scopes for this endpoint"


### Find your user ID:

1. find your *user_name here: https://www.spotify.com/no-nb/account/overview/ 
*NOTE: if you signed up spotify via facebook, your user_name should be entirely numerical 

## Getting your playlist ID:

1. On your youtube profile under playlists, find the playlist you want to add to spotify 
2. in url, your youtube playlist id should be the part right after "https://www.youtube.com/playlist?list="

  Example: 

  https://www.youtube.com/playlist?list=PLjf37AovvUXrptV_XNk-KZq5kjIlHopZk

  playlist ID: PLjf37AovvUXrptV_XNk-KZq5kjIlHopZk

# Code content & structure: 

**Details about how the code is built and an explanation of the different blocks to follow**

## Recources: 

 - Requests: https://docs.python-requests.org/en/latest/ 
 - Spotify and Youtube API (referenced above) 
 - json: https://docs.python.org/3/library/json.html
 - youtube_dl: https://github.com/ytdl-org/youtube-dl/

To install all Dependencies:
```
pip3 install -r requirements.txt
```

## Structure & function: 

The following is a short explanation of the code structure. 

### Class Y2B_to_Spot

Use of class due to the interdeoendencies in the functions output in the code. Inputs and function output fed to the def __init__function, to easily reference later where needed. 

### y2b login and grab item in specified list

First block of code follows the instruction for credential verification on the youtube API portal. The maximum results extracted for each request - you will discover - is 50 items. For youtube lists with >50 songs, a "nextPageToken" is printed in the response. This token is then used to generate another request and continue to grab video ids (vid_ids) for the playlist item untill the last page. Last page doesn't contain a "nextPageToken", while loop is then exited. All vid_ids are added to a list. 

The vid_ids list is then looped through using youtube_dl to extract the name and artist variable for each song. The items are added to a dictionary (in pairs of song: artist) song_dict.

Try block: 

youtube videos not containing the name and artist paramters properly filled in the description generate an error. The code passes the error and proceeds to the next youtube song item on the list. 

### Create new playist on spotify and extract playlist id

Using the code privided by spotify API guide for playlist generation, a POST request with json body containing the desired playlist name is sent. The response from the API will provide a playlist_id which will be used in the final step of the code. 

### Search for song on spotify, and extract uris. append uris to list

The function loops through the song_dict and sends a GET request with the song name and artis to spotify API. Spotfy response will contain a unique song identifier called uri-a sort of url :) . The uris extracted and are added to a list called urls. 

Try block: 

Not all artists and songs can be found on spotify, the try block checks for the absence of a proper reponse containing a uri and skips to the next item on the dictionary.

### Iterate through uris list and add to spotify list

This block of the code, loops through the urls list and sends a POST request to spotify. The POST request is to add the song to the playlist generated previously on spotify. 

##Improvements: 

 - At the different Try blocks, add an explanation of the error when Exception 








