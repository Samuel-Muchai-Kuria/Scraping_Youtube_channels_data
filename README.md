# YouTube Channel Data Analysis

This Python script allows you to gather and analyze data from YouTube channels using the YouTube Data API. The script fetches channel statistics, video details, and performs analysis to provide insights into the channels' performance.

## Prerequisites

Before running the script, make sure you have the following:

- A valid API Key from the Google Developer Console, which provides access to the YouTube Data API.
- Python installed on your system.
- Required Python libraries: `googleapiclient.discovery`, `pandas`, `seaborn`, and `requests`.

## Usage

1. Open the script in your preferred Python development environment, such as Visual Studio Code.
2. Modify the script's `api_key` variable by replacing `'Api Key'` with your actual YouTube Data API Key.
3. Enter the YouTube usernames (channel usernames) you want to analyze in the `names` variable. Separate multiple usernames with spaces.
4. Run the script. It will prompt you to provide the channel username(s).
5. The script will retrieve and display channel statistics, including subscribers, total views, and total videos.
6. For each provided channel username, the script will fetch video details, identify the top 10 videos based on views, and provide the number of videos posted per month.
7. The data for each channel will be saved in separate CSV files, named `file_0.csv`, `file_1.csv`, and so on.

## Notes

- Ensure you have the necessary permissions and quotas in your Google Developer Console for the YouTube Data API.
- The script fetches data from multiple channels (if provided), performs analysis, and saves results in separate CSV files.

## Disclaimer

This script is provided for educational and informational purposes. Make sure to review and comply with YouTube's terms of service and API usage policies. The script's functionality may change over time due to updates in the YouTube API or other factors.

## Author

Created by  Samuel Muchai Kuria
