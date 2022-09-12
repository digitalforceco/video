from ast import Return
from flask import Flask, request, redirect, send_file
import pathlib
import random
import re
import urllib.request
import yt_dlp
import re
from pytube import YouTube



app = Flask(__name__)


socialMediaFile = "SocialMedia.txt"


class VideoConnectionError(Exception):
    def __init__(self):
        print("Connection Error......")


class NotSocialMediaVideo(Exception):
    def __init__(self):
        print("The URL is not a SocialMedia Video")


def generateRandomNumber(min_value: int, max_value: int):
    """
    :param min_value:
    :param max_value:
    :return: random Number to be concatenated with the file name
    """
    return random.randint(min_value, max_value)


def generteRandomFileName(extension: str = '.mp4', delimiter: str = '/', url: str = " ") -> str:
    """
    :param url:
    :param extension:
    :param delimiter:
    :param url:
    :return: video file name
    """
    folder_path: str = 'Downloads/'
    video_name = re.sub('[^A-Za-z0-9]+', '', url.split(delimiter)[-1])
    output_file = "{0}{1}{2}".format(folder_path, video_name, extension)
    while pathlib.Path(output_file).exists():
        print("The video {0} exists...".format(video_name))
        video_name = video_name.join(str(generateRandomNumber(0, 99)))
        output_file = "{0}{1}{2}".format(folder_path, video_name, extension)
    print("Downloading {0}".format(output_file.split(delimiter)[1]))
    return output_file


def checkSocialMediaVideo(url: str, delimiter: str = '/', www: str = 'www') -> bool:
    """
    :param url: user input url
    :param delimiter:
    :param www:
    :return: True if it is social media video
    """
    if url.split(delimiter)[2].split('.')[0] == www:
        sm = url.split(delimiter)[2].split('.')[1]
    else:
        sm = url.split(delimiter)[2].split('.')[0]
    with open(socialMediaFile, "r") as file:
        for line in file:
            if sm in line:
                print("{0} video.".format(sm))
                return True

        return False




@app.route('/')
def holamundo():
    return 'Hola Mundo!'


@app.route('/youtube', methods=["POST"])
def youtube():

    url1 = request.form["youtube"]
    try:
        response = urllib.request.urlopen(url1)

        if checkSocialMediaVideo(url1):
            file_name = generteRandomFileName(url=url1)

            # Download
            try:
                ydl_opts = {'outtmpl': file_name}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    print(ydl.download([url1]))

                    ydl.download([url1])
       

                    return send_file(file_name, as_attachment=True)

            except yt_dlp.utils.DownloadError:
                VideoConnectionError()
                return 'error de conexion!'

        else:
            NotSocialMediaVideo()
            return 'no es un video de las redes sociales!'

    except Exception:
        VideoConnectionError()
        return 'no pudimos encontrar el video !'


if __name__ == '__main__':
    app.run(port=80, debug=True)
