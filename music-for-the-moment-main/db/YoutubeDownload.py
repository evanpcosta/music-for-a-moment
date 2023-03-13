from youtube_dl import YoutubeDL
import os
import sys

audio_downloader = YoutubeDL({'format': 'bestaudio'})

def youtube_downloader(URL):

    try:
        # THIS IS PARAMS OBJECT FOR THE YOUTUBE DOWNLOADER
        # TO SEE MORE DOCUMENTATION TYPE youtube-dl -help in command line

        options = {
            'verbose': False,
            'audioformat': 'mp3',
            'outtmpl': './downloadedsongs/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            "restrictfilenames": True,
            "yesplaylist": True,
            "ignore-errors": True,
        }

        print('Youtube Downloader'.center(40, '_'))

        audio_downloader.extract_info(URL)
        with YoutubeDL(options) as ydl:
            ydl.download([URL])

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print("Couldn\'t download the audio")