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

clips = [
    VideoClip([ImageClip(img).with_duration(image_duration)]).crossfadein(1)
    for img in image_files
]

# Concatenate with crossfade
fade_duration = 1  # seconds
video = concatenate_videoclips(clips, method="compose", padding=-fade_duration)
video.write_videofile("output_with_transitions.mp4", fps=24)

# import ffmpeg

# (
#     ffmpeg.input("./*.jpeg", pattern_type="glob", framerate=1)
#     .filter("deflicker", mode="pm", size=10)
# #     .filter("scale", size="hd1080", force_original_aspect_ratio="increase")
# #     .output(
# #         "movie.mp4", crf=20, preset="slower", movflags="faststart", pix_fmt="yuv420p"
# #     )
# #     .run()
# # )
# output_name = "movie.mp4"
# if os.path.exists(output_name):
#     os.remove(output_name)
# # (
# #     ffmpeg.input(
# #         "./images/*.jpeg", pattern_type="glob", framerate=1 / 7
# #     )  # each frame is 7 seconds
# #     .filter("scale", "trunc(iw/2)*2", "trunc(ih/2)*2")
# #     .output(output_name)
# #     .run()
# # )
# (
#     ffmpeg.input(
#         "./images/*.jpeg", pattern_type="glob", framerate=1 / 7
#     )  # each frame is 7 seconds
#     .filter("scale", "1080", "1920")
#     .filter("pad", "1080", "1920", "(ow-iw)/2", "(oh-ih)/2")
#     .output(output_name)
#     .run()
# )
