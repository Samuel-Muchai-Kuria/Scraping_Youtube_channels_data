#!/usr/bin/env python
# coding: utf-8

# In[174]:


from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import requests


# In[140]:


# remember to remove my api key before posting it
api_key = 'AIzaSyA1bDvFjcDl4ncgdq45SzyaQWUh4AJgRX4'

channel_names = ['@HarmanSinghYouTube','@Thuvu5','@AlexTheAnalyst','@antdev010','@ShrenikJain']

youtube = build('youtube', 'v3', developerKey=api_key)


# ## Get Channel ID using channel name

# In[141]:


channel_ids = []
for channel in channel_names:
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={channel}&type=channel&key={api_key}"

    response = requests.get(url)
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
print("Channel IDs =", channel_ids)


# ## Function to get channel details
# 

# In[142]:


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
    return all_data


# In[143]:


channel_stats = get_channel_stats(youtube, channel_ids)


# In[144]:


channel_data = pd.DataFrame(channel_stats)
channel_data


# In[145]:


channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
channel_data['Total_Views'] = pd.to_numeric(channel_data['Total_Views'])
channel_data['Total_videos'] = pd.to_numeric(channel_data['Total_videos'])
# channel_data.dtypes


# In[146]:


sns.set(rc={'figure.figsize':(10,8)})
ax = sns.barplot(x='Channel_title',y='Total_videos', data= channel_data)


# ## Get video ids

# In[147]:


playlist_id = channel_data.loc[channel_data['Channel_title'] == 'Harman Singh','playlist_id'].iloc[0]
playlist_id


# In[148]:


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


# In[150]:


video_ids = get_video_ids(youtube,playlist_id)


# ## Get video details

# In[159]:


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
                              Likes = video['statistics']['likeCount'],
                              Comments = video['statistics']['commentCount'])
        
            all_video_stats.append(video_stats)

    return all_video_stats


# In[160]:


video_details= get_video_details(youtube,video_ids)


# In[163]:


video_data= pd.DataFrame(video_details)


# In[168]:


video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'])
video_data['Likes'] = pd.to_numeric(video_data['Likes'])
video_data['Comments'] = pd.to_numeric(video_data['Comments'])


# In[171]:


top10_videos= video_data.sort_values(by='Views',ascending=False).head(10)


# In[ ]:


ax1 = sns.barplot(x='Views',y='Title', data=top10_videos)


# In[180]:


video_data['Month']= pd.to_datetime(video_data['Published_date']).dt.strftime('%b')


# In[188]:


videos_per_month = video_data.groupby('Month',as_index=False).size()
sort_order= ['Jan', 'Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec' ]
videos_per_month.index = pd.CategoricalIndex(videos_per_month['Month'], categories= sort_order, ordered=True)
videos_per_month= videos_per_month.sort_index()


# In[189]:


ax2 = sns.barplot(x='Month', y='size', data= videos_per_month)


# ## Save the data into csv files

# In[193]:

#path= 'C:\Users\Sammybravol\OneDrive\Desktop\Projects\Youtube scraping api\Video_data(Harman Sigh).csv'
npath="new.csv"
video_data.to_csv(npath, index=False)


# In[ ]:





# In[ ]:




