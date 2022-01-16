#code structure:

# 1. y2b login, identify list and extract the song name/artist to then append to dict
# 2. Create new playist on spotify and extract playlist id
# 3. iterate through dict to find spotify uri for songs. add uris to list
# 4. iterate through uri list and add songs to new spotify list


import pprint

import requests
import json
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl

#Get changing variables by manual entry

y_playlistid = input("Paste your youtube playlist ID here: ")
user_id = input("Enter your spotify ID here:  ")
token = input("Paste you spotify token here: ")
Play_list_name = input ("Enter play list name here: ")

#scopes in y2b API set to read

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]



class Y2B_to_Spot:

    def __init__(self):

        self.scopes = scopes

        self.y_playlistid = y_playlistid

        self.song_dict = self.request_y2b()

        self.user_id = user_id

        self.token = token

        self.playlist_id = self.create_spot_playlist()

        self.urls = self.search_spot_item()



# 1. y2b login and grab item in specified list

#
    def request_y2b(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.playlistItems().list(
            part="snippet",
            maxResults=50,
            playlistId=y_playlistid
        )

        response = request.execute()

        #check there is a next page token, len of list >50.

        try:

            nextPageToken = response["nextPageToken"]

        except:
            pass

        # collect the videoid from the first page and get nextpage token the response and pass to youtube dl

        vid_ids = []

        for item in response['items']:
            dict_items = dict(item["snippet"].items())
            resource_id = dict_items["resourceId"]
            video_Id = resource_id["videoId"]

            vid_ids.append(video_Id)

        #run this code if pagetoken is found else pass

        try:
            while nextPageToken:

                request_n = youtube.playlistItems().list(
                    part="snippet",
                    maxResults=50,
                    pageToken=nextPageToken,
                    playlistId= y_playlistid
                )

                response_n = request_n.execute()

                for item in response_n['items']:
                    dict_items = dict(item["snippet"].items())
                    resource_id = dict_items["resourceId"]
                    video_Id = resource_id["videoId"]

                    vid_ids.append(video_Id)

                    try:

                        nextPageToken = response_n["nextPageToken"]

                    except:

                        nextPageToken = False

        except:
            pass

        song_dict = {}

        # use youtube_dl to collect the song name, artist and append to song_dict


        for item in vid_ids:
            try:
                youtube_url = "https://www.youtube.com/watch?v={}".format(item)

                video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
                song_name = video["track"]
                artist = video["artist"]

                song_dict.update({song_name: artist})

            except:
                pass


        pprint.pprint(song_dict)

        return song_dict


# 2. Create new playist on spotify and extract playlist id


    def create_spot_playlist(self):


        #In Post requests, the data body has to be sent in json format

        request_body = json.dumps({
            "name": Play_list_name,
            "description": "Py_auto_added",
            "public": False
        })
        response = requests.post(

            "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id),

            data=request_body,

            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }

        )

        response_json = response.json()
        playlist_id = response_json["id"]

        return playlist_id




# 3. search for song on spotify, and extract uris. append uris to list

    def search_spot_item(self):

    #empty list to be populated by response from spotify API
        urls = []

        #check if the k, v in dictionary are properly extracted and appended to dong_dict, sometimes None elements can sneak in
        try:

            for item in self.song_dict.items():
                track = item[1]
                artist = item[0]

                query = "https://api.spotify.com/v1/search?q={}%20{}+&type=track&offset=0&limit=20".format(
                    track,
                    artist
                )
                response = requests.get(
                    query,
                    headers={
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "Authorization": "Bearer {}".format(token)
                    }
                )
                response_json = response.json()

                #check the response, if track not found, pass to the next. Append the the uri of the found songs to URLS list

                try:
                    songs = response_json["tracks"]["items"]

                    # only use the first song
                    uri = songs[0]["uri"]

                    urls.append(uri)
                except:
                    pass



        except:

            print(" error in extracting spotify uris")

        pprint.pprint(urls)

        return urls




# 4. iterate through uris list and add to spotify list

    def add_song_to_spotify_list(self):

        for item in self.urls:

            r_data = json.dumps({
                "uris": [item]
            })

            query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
                self.playlist_id)

            response = requests.post(
                query,
                data=r_data,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.token)
                }
            )

        print ("All songs are added to your new playlist")

#run class

if __name__ == '__main__':
    cp = Y2B_to_Spot()
    cp.add_song_to_spotify_list()
