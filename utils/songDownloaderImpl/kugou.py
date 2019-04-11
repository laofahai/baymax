from utils import http
from base.entity.Song import Song
from urllib import request

queryListUrl = "http://songsearch.kugou.com/song_search_v2?keyword=%s&page=1&pagesize=20&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0"
queryDetailUrl = "http://www.kugou.com/yy/index.php?r=play/getdata&hash=%s"


def getPlayList(keyword):
    listResult = http.get(queryListUrl.replace("%s", keyword))
    playList = []

    if len(listResult["data"]["lists"]) <= 0:
        return []

    for item in listResult["data"]["lists"]:
        playList.append(
            Song(
                item["FileHash"],
                item["SongName"].replace("<em>", "").replace("</em>", ""),
                item["SingerName"]
            )
        )

    return playList


def download(song, savePath):
    detailResult = http.get(queryDetailUrl.replace("%s", song.hash))

    mp3Url = detailResult["data"]["play_url"]

    if not mp3Url:
        return False

    if savePath is None:
        savePath = getFilePath(song.songName)

    request.urlretrieve(mp3Url, savePath)

    return savePath

def getFilePath(songName):
    songName = songName[0:10]
    return "data/music/" + songName + ".mp3"

