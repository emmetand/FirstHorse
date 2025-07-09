import pandas as pd
import random
from gtts import gTTS
import os
import requests
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip


def main():
    #gets quote
    quote = get_gift_horse_quote("gift_horse.csv")
    print(f"Used Quote: {quote}")

    #sets output path for an mp3
    os.makedirs("assets", exist_ok = True)
    output = "assets/voice.mp3"

    #converts text to speech and saves
    horse_to_speech(quote, output)
    print(f"Saved voice file to: {output}")

    #calls pexel API to pull a lower res horse video
    horse_vid_download()

    # combines and saves the horse video and horse audio
    horse_make(quote)


def get_gift_horse_quote(filename):
    # returns random quote from CSV file of quotes
    df = pd.read_csv(filename, quotechar='"')
    return random.choice(df["quote"].dropna())

def horse_to_speech(text, output):
    # converts quote to an mp3 file and saves it
    hts = gTTS(text, lang="en", tld="co.uk")
    hts.save(output)

def horse_vid_download():
    API_KEY = "sUokvpWyNspdCZENkYItxxYcXztLmNfvQJYRdQu09wykWnrEbqP6MQne"

    os.makedirs("assets", exist_ok=True)

    #search for horse videos
    headers = {"Authorization": API_KEY}
    params = {
        "query": "horse running",
        "per_page": 50
    }

    hvid = requests.get("https://api.pexels.com/videos/search", headers = headers, params = params)
    data = hvid.json()
    all_videos = data.get("videos",[])

    # pick random one
    chosen = random.choice(all_videos)

    #save it
    video_files = sorted(chosen["video_files"], key=lambda f: f["width"] * f["height"])
    video_url = chosen["video_files"][0]["link"]
    save = os.path.join("assets", "horse_background.mp4")

    r = requests.get(video_url)
    with open(save, "wb") as f:
        f.write(r.content)
        print(f"Saved video file to: {save}")


def horse_make(quote):
    video_path = "assets/horse_background.mp4"
    audio_path = "assets/voice.mp3"
    output_path = "assets/final_horse_video.mp4"

    # loads video file and adjusts it
    video = VideoFileClip(video_path)
    video = video.subclipped(0,7)

    # loads audio file and adusts it
    audio = AudioFileClip(audio_path)

    # add text overlay
    text = TextClip(
        font='arial',
        text= quote,
        font_size = 24,
        color = 'yellow',
        method = 'caption',
        size = (video.w, None),
        duration = video.duration
    ).with_position(("center", video.h - 100))

    #overlay text to video
    final = CompositeVideoClip([video, text]).with_audio(audio)

    # final output
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")

    print(f"Saved final video file to: {output_path}")

if __name__ == "__main__":
    main()