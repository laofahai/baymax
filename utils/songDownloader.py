# coding: utf-8
from utils import http
from base.entity.Song import Song
import importlib

class SongDownloader:

    # 来源
    source = "kugou"

    # 播放列表
    playList = []

    # 实例
    instances = {}

    @staticmethod
    def getInstance():
        if SongDownloader.source not in SongDownloader.instances:
            SongDownloader.instances[SongDownloader.source] = importlib.import_module("utils.songDownloaderImpl." + SongDownloader.source)

        return SongDownloader.instances[SongDownloader.source]

    @staticmethod
    def getPlayList(keyword):
        SongDownloader.playList = SongDownloader.getInstance().getPlayList(keyword)
        return SongDownloader.playList

    @staticmethod
    def download(song, savePath = None):
        return SongDownloader.getInstance().download(song, savePath)

    @staticmethod
    def getFilePath(songName):
        return SongDownloader.getInstance().getFilePath(songName)

    @staticmethod
    def setCurrentIndex(index):
        return SongDownloader.getInstance().setCurrentIndex(index)


