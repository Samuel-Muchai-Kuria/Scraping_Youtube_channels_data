from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import requests

# Function to get channel id from the channel username
def get_channel_ids(channel_names,api_key):
    channel_ids = []
    for channel in channel_names:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={channel}&type=channel&key={api_key}"

        response = requests.get(url,timeout=30)
        data = response.json()

        if "items" in data:
            if len(data["items"]) > 0:
                channel_id = data["items"][0]["snippet"]["channelId"]
                channel_ids.append(channel_id)
                # print("Channel ID:", channel_id)
            else:
                print("No channel found with the provided name.")
        else:
            print("Error in API response.")
    # print("Channel IDs =", channel_ids)
    return channel_ids


# Function to get basic channel statistics such as total views, subcribers and total number of videos
def get_channel_stats(youtube, channel_ids):
    all_data= []
    request = youtube.channels().list(part="snippet,contentDetails,statistics", id= ','.join(channel_ids))
    response = request.execute()
    
    for i in range(len(response['items'])):
        data = dict( Channel_title = response['items'][i]['snippet']['title'],
                    Subscribers = response['items'][i]['statistics']['subscriberCount'],
                   Total_Views = response['items'][i]['statistics']['viewCount'],
                   Total_videos = response['items'][i]['statistics']['videoCount'],
                   Country = response['items'][i]['snippet']['country'],
                   playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads']
                   )
        all_data.append(data)
    channel_data = pd.DataFrame(all_data)
    return channel_data


# Function to get all video ids that have been posted in the channel
def get_video_ids(youtube,playlist_id):
    
    request = youtube.playlistItems().list(
                        part= 'contentDetails',
                        playlistId = playlist_id,
                        maxResults = 50
                        )
    response = request.execute()
    
    video_ids=[]
    
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
    
    next_page_token= response.get('nextPageToken')
    more_pages = True
    
    while more_pages:
        if next_page_token is None:
            more_pages =False
        else:
            request = youtube.playlistItems().list(
                        part= 'contentDetails',
                        playlistId = playlist_id,
                        maxResults = 50,
                        pageToken= next_page_token)
            response = request.execute()
            
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            
            next_page_token = response.get('nextPageToken')      
    return video_ids


# Function to get individual video details from the channel
def get_video_details(youtube,video_ids):
    
    all_video_stats = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
                            part= 'snippet, statistics',
                            id = ','.join(video_ids[i:i+50]))
        response= request.execute()
        
        for video in response['items']:
            video_stats= dict( Title = video['snippet']['title'],
                             Published_date= video['snippet']['publishedAt'],
                              Views = video['statistics']['viewCount'],
                              Likes=video['statistics'].get('likeCount', 0),  # Use .get() to handle missing key
                              Comments = video['statistics'].get('commentCount',0))
        
            all_video_stats.append(video_stats)

    return all_video_stats

 # Function to get top10 videos and also number of videos in terms of months
def get_top10_and_videosper_month(video_data):

    video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
    video_data['Views'] = pd.to_numeric(video_data['Views'])
    video_data['Likes'] = pd.to_numeric(video_data['Likes'])
    video_data['Comments'] = pd.to_numeric(video_data['Comments'])


    top10_videos= video_data.sort_values(by='Views',ascending=False).head(10)

    video_data['Month']= pd.to_datetime(video_data['Published_date']).dt.strftime('%b')



    videos_per_month = video_data.groupby('Month',as_index=False).size()
    sort_order= ['Jan', 'Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec' ]
    videos_per_month.index = pd.CategoricalIndex(videos_per_month['Month'], categories= sort_order, ordered=True)
    videos_per_month= videos_per_month.sort_index()

    return top10_videos,videos_per_month



# Main function
def main():
    # Enter your API key from google console
    api_key = 'Api Key'
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Sample youtube usernames  ['@HarmanSinghYouTube','@Thuvu5','@AlexTheAnalyst','@antdev010','@ShrenikJain','@domainfilmss']
    
    names = input("Please provide the channel Username(@harmanSighYouTube): ")
    channel_names = names.split()
    number_of_channels=len(channel_names)
    print('Number of channels received: ',number_of_channels)

    channel_ids = get_channel_ids(channel_names,api_key)

    channel_data = get_channel_stats(youtube, channel_ids)

    print('###########################')
    print('Channel Statistics')
    print('###########################')
    print(channel_data)
    
    # change the type of values to numeric for calculation and analysis
    channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
    channel_data['Total_Views'] = pd.to_numeric(channel_data['Total_Views'])
    channel_data['Total_videos'] = pd.to_numeric(channel_data['Total_videos'])


    playlist_ids = channel_data['playlist_id'].tolist()
    # print(playlist_ids)
    
    # this for loop caters for when the user enters multiple usernames
    for idx,playlist_id in enumerate(playlist_ids, start=000):

        video_ids = get_video_ids(youtube,playlist_id)

        video_details= get_video_details(youtube,video_ids)
        video_data= pd.DataFrame(video_details)
        print('########################################')
        print("Top 10 videos and videos per month")
        print('########################################')
        print(get_top10_and_videosper_month(video_data))

        #Save the data in Multiple CSV files 
        csvpath=f"file_{idx}.csv"
        video_data.to_csv(csvpath, index=False)

    pass


# Call the main function if the script is executed directly
if __name__ == "__main__":
    main()
