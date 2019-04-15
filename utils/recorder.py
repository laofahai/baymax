import pyaudio
import numpy
import wave
import time
from utils.sound import Sound
from utils import light

class Recorder:

    savPath = "data/audio/input.wav"

    # weight: 录音触发阈值， 数字越大需要音量越大
    # maxDownSum: 无声音后停止， 数字越大时间越长
    @staticmethod
    def startRecord(weight = 5000, maxDownSum = 15):
        CHUNK = 320  #每次读取的音频流长度
        FORMAT = pyaudio.paInt16  #格式
        CHANNELS = 1  #声道
        RATE = 16000  #采样率
        p = pyaudio.PyAudio()
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            input_device_index=1
        )
        frames = []

        downSum = 0
        i = 0
        latestData = None # 记录触发前上一段数据

        while True:

            if not Sound.isSong and Sound.isBusy():
                continue

            # print(Sound.isBusy() and not Sound.isSong)
            if i < 50:
                i+= 1

            data = stream.read(CHUNK, exception_on_overflow = False)
            audio_data = numpy.fromstring(data, dtype=numpy.short)
            isLargeVoice = numpy.sum(
                numpy.max(audio_data) > weight
            )
            # print("temp>weight", numpy.max(audio_data), weight, len(frames))
            if (i > 5 and isLargeVoice) or len(frames) > 0:
                print("recording... ")
                # light.open(21)
                if len(frames) <= 0:
                    frames.append(latestData)
                frames.append(data)
                if not isLargeVoice:
                    downSum += 1
                else:
                    downSum = 0

                if downSum > 50:
                    # light.close(21)
                    break

            latestData = data
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        wf = wave.open(Recorder.savPath, 'wb')
        
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        return Recorder.savPath

if __name__ == "__main__":
    Recorder.startRecord(80)
