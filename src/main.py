import praw
import requests
import os
import shutil
import cv2

reddit = praw.Reddit(
    client_id="BQ-csvDK715FdbrHV9TPbQ",
    client_secret="6pgdR7fVOjFjokSuNMQ2HyVzeuVF5Q",
    user_agent="YoutubeMemes 0.1.0 by /u/Charan__C github.com/ChurroC/Meme-Youtube",
)

file_base = "./images"
if os.path.exists(file_base):
    shutil.rmtree(file_base)

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
        if not os.path.exists(file_base):
            os.makedirs(file_base)
        with open(os.path.join(file_base, file_name), "wb") as handler:
            handler.write(img_data)
            if "png" in file_name:
                image = cv2.imread(os.path.join(file_base, file_name))
                cv2.imwrite(
                    os.path.join(
                        file_base, "".join(file_name.split(".")[0:-1]) + ".jpeg"
                    ),
                    image,
                    [int(cv2.IMWRITE_JPEG_QUALITY), 100],
                )
                os.remove(os.path.join(file_base, file_name))

import ffmpeg

# (
#     ffmpeg.input("./*.jpeg", pattern_type="glob", framerate=1)
#     .filter("deflicker", mode="pm", size=10)
#     .filter("scale", size="hd1080", force_original_aspect_ratio="increase")
#     .output(
#         "movie.mp4", crf=20, preset="slower", movflags="faststart", pix_fmt="yuv420p"
#     )
#     .run()
# )
output_name = "movie.mp4"
if os.path.exists(output_name):
    os.remove(output_name)
# (
#     ffmpeg.input(
#         "./images/*.jpeg", pattern_type="glob", framerate=1 / 7
#     )  # each frame is 7 seconds
#     .filter("scale", "trunc(iw/2)*2", "trunc(ih/2)*2")
#     .output(output_name)
#     .run()
# )
(
    ffmpeg.input(
        "./images/*.jpeg", pattern_type="glob", framerate=1 / 7
    )  # each frame is 7 seconds
    .filter("scale", "1080", "1920")
    .filter("pad", "1080", "1920", "(ow-iw)/2", "(oh-ih)/2")
    .output(output_name)
    .run()
)
