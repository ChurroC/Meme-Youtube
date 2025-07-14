import os
import json
from datetime import date
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from dotenv import load_dotenv

load_dotenv()

# YouTube API configuration
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]
CLIENT_SECRET_FILE = "client_secret.json"
CREDENTIALS_FILE = "credentials_storage.json"


def get_authenticated_service():
    """Get authenticated YouTube service"""
    creds = None

    # Load existing credentials
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as token:
            creds_data = json.load(token)
            creds = Credentials.from_authorized_user_info(creds_data, SCOPES)

    # If there are no valid credentials, request authorization
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for future use
        with open(CREDENTIALS_FILE, "w") as token:
            json.dump(json.loads(creds.to_json()), token)

    return build("youtube", "v3", credentials=creds)


# Get authenticated YouTube service (equivalent to channel.login)
youtube = get_authenticated_service()

# Video file path (equivalent to LocalVideo)
video_file_path = "output_with_transitions.mp4"

# Video snippet configuration (equivalent to video.set_* methods)
video_title = f"r/Memes top 9 - {date.today().strftime('%m/%d/%Y')}"

video_description = """
🔥 TOP MEMES FROM r/MEMES 🔥
Welcome to your daily dose of the BEST memes from Reddit! Today we're diving into the top-voted memes from r/Memes that are absolutely breaking the internet right now.
What you'll find in this video:
✅ The funniest memes that got thousands of upvotes
✅ Relatable content that will make you laugh out loud
✅ Fresh daily memes straight from the Reddit community
✅ Memes you can share with your friends
Featured memes include:

Relatable life situations
Trending topics and current events
Classic meme formats with new twists
Original content from creative Redditors

Don't forget to:
👍 LIKE if these memes made you laugh
🔔 SUBSCRIBE for daily meme content
💬 COMMENT your favorite meme from today's video
📤 SHARE with friends who need a good laugh
Follow us for more:

Daily r/Memes compilations
Fresh Reddit content
The best of internet humor

#Memes #Reddit #Funny #DailyMemes #rMemes #RedditMemes #Viral #Comedy #Internet #Trending

Disclaimer: All memes are sourced from r/Memes subreddit. Credit goes to the original creators and posters. This is a compilation for entertainment purposes.
Copyright: This video falls under fair use for commentary and educational purposes. All content belongs to their respective creators.
"""

video_tags = [
    "memes",
    "reddit",
    "r/memes",
    "funny",
    "comedy",
    "viral",
    "trending",
    "hilarious",
    "laugh",
    "humor",
    "internet",
    "redditmemes",
    "bestmemes",
    "topmemes",
    "dailymemes",
    "freshmemes",
    "memecompilation",
    "memereview",
    "redditcompilation",
    "funny",
    "comedyvideos",
    "viralvideos",
    "trendingvideos",
    "internetculture",
    "onlinehumor",
    "relatable",
    "relatablememes",
    "lifememes",
    "workmemes",
    "schoolmemes",
    "gamingmemes",
    "wholesome",
    "wholesomememes",
    "positivevibes",
    "goodvibes",
    "motivation",
    "inspirational",
    "uplifting",
    "feelgood",
    "happiness",
    "joy",
    "smile",
    "laughter",
    "funnymoments",
    "comedy gold",
    "peak comedy",
]

# Video metadata (equivalent to all video.set_* methods)
video_body = {
    "snippet": {
        "title": video_title,
        "description": video_description,
        "tags": video_tags,
        "categoryId": "23",  # Entertainment category
        "defaultLanguage": "en-US",
    },
    "status": {
        "privacyStatus": "public",
        "embeddable": True,
        "license": "creativeCommon",
        "publicStatsViewable": True,
    },
}

# Media upload configuration
media = MediaFileUpload(
    video_file_path, chunksize=-1, resumable=True, mimetype="video/mp4"
)

try:
    # Upload video (equivalent to channel.upload_video)
    insert_request = youtube.videos().insert(
        part=",".join(video_body.keys()), body=video_body, media_body=media
    )

    # Execute the upload
    video_response = insert_request.execute()

    # Print results (equivalent to print(video.id) and print(video))
    video_id = video_response["id"]
    print(f"Video ID: {video_id}")
    print(f"Video Response: {video_response}")

    # Like the video (equivalent to video.like())
    like_request = youtube.videos().rate(id=video_id, rating="like")
    like_response = like_request.execute()
    print(f"Video liked successfully")

except HttpError as e:
    print(f"An HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
