import googleapiclient.discovery

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "YOUR_API_KEY"    # YOUR_API_KEY = {your YOUTUBE data api v3}

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY
)

def main():

    # for extracting details of channel through Youtube username
    response = youtube.channels().list(
        part="contentDetails",
        forUsername="USERNAME"      # USERNAME = {Youtube Username of channel you want to fetch info of}
    ).execute()

    # extracting playlist id for all uploaded videos of the channel
    playlistId = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # for extracting details of all uploaded videos in a channel
    videos = fetch_all_videos(playlistId)

    # Empty string for storing Titles of videos
    data = ""

    for video in videos:
        data += video['snippet']['title'] + '\n'
    
    # write Titles of videos in a text file
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(data)
    


def fetch_all_videos(playlistId):
    videos = []
    next_page_token = None

    while True:
        response = youtube.playlistItems().list(
            playlistId = playlistId,
            part = 'snippet',
            maxResults = 50,
            pageToken = next_page_token
        ).execute()

        videos += response['items']
        next_page_token = response.get('nextPageToken')

        if next_page_token is None:
            break

    return videos



if __name__ == "__main__":
    main()