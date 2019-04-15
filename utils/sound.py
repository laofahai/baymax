import pygame
import time
from utils.songDownloader import SongDownloader
from utils.configure import Configure
import os

class Sound:
    
    machineWavPath = "data/audio/machine.mp3"

    inited = False

    isSong = False

    currentPlayIndex = 0

    @staticmethod
    def init():
        pygame.mixer.init()
        pygame.mixer.music.set_volume(.3)

    @staticmethod
    def play(file, isSong = False):
        if not Sound.inited:
            Sound.init()

        Sound.isSong = isSong

        if Configure.debug:
            print("utils.sound.play: " + file, ", is song: ", isSong)

        return Sound.viaPygame(file)

    @staticmethod
    def stop():
        # Sound.currentPlayIndex = 0
        # SongDownloader.playList = []
        pygame.mixer.music.stop()

    @staticmethod
    def pause():
        pygame.mixer.music.pause()

    @staticmethod
    def unpause():
        pygame.mixer.music.unpause()

    @staticmethod
    def replayCurrent():
        if not Sound.isSong or not Sound.isBusy():
            return None

        Sound.stop()
        songPath = SongDownloader.getFilePath(SongDownloader.playList[Sound.currentPlayIndex].songName)
        if not os.path.isfile(songPath):
            if not SongDownloader.download(SongDownloader.playList[Sound.currentPlayIndex]):
                return None
        Sound.play(songPath, True)

    @staticmethod
    def playSong(keyword, source = "kugou"):
        Sound.isSong = True
        SongDownloader.source = source
        playList = SongDownloader.getPlayList(keyword)
        if len(playList) <= 0:
            return None
        # print(playList)
        Sound.currentPlayIndex = 0
        songPath = SongDownloader.getFilePath(playList[0].songName)
        if not os.path.isfile(songPath):
            SongDownloader.download(SongDownloader.playList[0])

        Sound.play(songPath, True)

    @staticmethod
    def playNext():
        playListLen = len(SongDownloader.playList)
        if not Sound.isSong or playListLen < 1:
            return

        if Sound.currentPlayIndex + 1 >= playListLen:
            Sound.currentPlayIndex = 0
        else:
            Sound.currentPlayIndex = Sound.currentPlayIndex + 1

        songPath = SongDownloader.getFilePath(SongDownloader.playList[Sound.currentPlayIndex].songName)
        if not os.path.isfile(songPath):
            SongDownloader.download(SongDownloader.playList[Sound.currentPlayIndex])
        Sound.play(songPath, True)


    @staticmethod
    def playPrevious():
        playListLen = len(SongDownloader.playList)
        if not Sound.isSong or playListLen < 1:
            return

        if Sound.currentPlayIndex < 1:
            Sound.currentPlayIndex = 0
        else:
            Sound.currentPlayIndex = Sound.currentPlayIndex - 1

        songPath = SongDownloader.getFilePath(SongDownloader.playList[Sound.currentPlayIndex].songName)
        if not os.path.isfile(songPath):
            SongDownloader.download(SongDownloader.playList[Sound.currentPlayIndex])
        Sound.play(songPath, True)


    @staticmethod
    def isBusy():
        if not Sound.inited:
            Sound.init()
        return pygame.mixer.music.get_busy()

    @staticmethod
    def viaPygame(file):

        # @todo
        if not os.path.isfile(file):
            return

        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        while Sound.isBusy():
            time.sleep(0.2)

        pygame.mixer.music.load("data/audio/machine.wav")
