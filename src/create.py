import praw
import requests
import os
import shutil
import cv2
from moviepy import *

reddit = praw.Reddit(
    client_id="BQ-csvDK715FdbrHV9TPbQ",
    client_secret="6pgdR7fVOjFjokSuNMQ2HyVzeuVF5Q",
    user_agent="YoutubeMemes 0.1.0 by /u/Charan__C github.com/ChurroC/Meme-Youtube",
)

image_folder = "./images"
image_duration = 7

if os.path.exists(image_folder):
    shutil.rmtree(image_folder)

# 180(total short time)/7(for each video length) = 25(rounded down)
# but also consider that some are videos and not images
for index, submission in enumerate(
    reddit.subreddit("memes").top(time_filter="day", limit=9), 1
):
    print(submission.title)
    print(submission.url)
    # If video I could get link if I do submission.url + ".json" and then search for media url
    if "v.redd.it" not in submission.url:
        img_data = requests.get(submission.url).content
        file_name = (
            str(index)
            + "_"
            + submission.title.strip()
            + "."
            + submission.url.split(".")[-1]
        )
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        with open(os.path.join(image_folder, file_name), "wb") as handler:
            handler.write(img_data)
            if "png" in file_name:
                image = cv2.imread(os.path.join(image_folder, file_name))
                cv2.imwrite(
                    os.path.join(
                        image_folder, "".join(file_name.split(".")[0:-1]) + ".jpeg"
                    ),
                    image,
                    [int(cv2.IMWRITE_JPEG_QUALITY), 100],
                )
                os.remove(os.path.join(image_folder, file_name))

image_files = sorted(
    [
        os.path.join(image_folder, fname)
        for fname in os.listdir(image_folder)
        if fname.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
)

# clips = [
#     ImageClip(img).with_duration(image_duration).with_effects([vfx.Resize(720, 1280)])
#     for img in image_files
# ]

clips = []
for img in image_files:
    print(img)
    clips.append(
        ImageClip(img)
        .with_duration(image_duration)
        .with_effects([vfx.FadeIn(0.2), vfx.FadeOut(0.2), vfx.Resize((720, 1280))])
    )

# Concatenate with crossfade
video = concatenate_videoclips(clips, method="compose")
video.write_videofile("output_with_transitions.mp4", fps=24)
