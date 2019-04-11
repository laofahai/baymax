from utils import http
from base.entity.Song import Song
from urllib import request
from utils.configure import Configure
from pydub import AudioSegment
from pydub.utils import which
import os

queryListUrl = "https://www.ximalaya.com/revision/play/album?albumId={0}&pageNum={1}&sort=0&pageSize=30"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


def getPlayList(keyword):
    playList = []

    # 最后播放的 index
    latestIndex = int(Configure.get("ximalaya", "LATEST_INDEX"))
    pageNum = latestIndex = int(latestIndex // 30) + 1

    listUrl = queryListUrl.format(Configure.get("ximalaya", "ALBUM_ID"), pageNum)
    lists = http.get(listUrl, headers)

    if "data" not in lists or "tracksAudioPlay" not in lists["data"]:
        return []

    for item in lists["data"]["tracksAudioPlay"]:
        if item["index"] <= latestIndex:
            continue

        song = Song(
            item["src"],
            item["trackName"],
            item["albumName"]
        )
        song.index = item["index"]
        playList.append(song)

    if len(playList) < 15:
        listUrl = queryListUrl.format(Configure.get("ximalaya", "ALBUM_ID"), pageNum + 1)
        lists = http.get(listUrl, headers)
        if "data" in lists and "tracksAudioPlay" in lists["data"]:
            for item in lists["data"]["tracksAudioPlay"]:
                song = Song(
                    item["src"],
                    item["trackName"],
                    item["albumName"]
                )
                song.index = item["index"]
                playList.append(song)


    #
    # if len(listResult["data"]["lists"]) <= 0:
    #     return []
    #
    # for item in listResult["data"]["lists"]:
    #     playList.append(
    #         Song(
    #             item["FileHash"],
    #             item["SongName"].replace("<em>", "").replace("</em>", ""),
    #             item["SingerName"]
    #         )
    #     )

    return playList


def download(song, savePath):
    savePath = getFilePath(song.songName, "m4a")

    request.urlretrieve(song.hash, savePath)

    AudioSegment.converter = which("ffmpeg")
    raw = AudioSegment.from_file(savePath, format="mp4")

    mp3SavePath = savePath.replace(".m4a", ".mp3")
    file_handle  = raw.export(mp3SavePath, format="mp3")

    os.remove(savePath)

    setCurrentIndex(song.index)

    return mp3SavePath

def getFilePath(songName, format = "mp3"):
    songName = songName[0:10]
    return "data/story/" + songName + "." + format

def setCurrentIndex(index):
    Configure.init()
    Configure.config.set("ximalaya", "LATEST_INDEX", index)
