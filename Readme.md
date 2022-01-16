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

## Structure & function: 

### Class CreatePlaylist

### y2b login and grab item in specified list

### Create new playist on spotify and extract playlist id

### Search for song on spotify, and extract uris. append uris to list

### Iterate through uris list and add to spotify list







