#coding: utf-8
try:
    import RPi.GPIO as GPIO
except:
    pass
import time

class Temperature():

    @staticmethod
    def get(channel = 18):
        data = []			#温湿度值
        j = 0				#计数器
        GPIO.setmode(GPIO.BCM)		#以BCM编码格式

        time.sleep(1)			#时延一秒
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(channel, GPIO.LOW)
        time.sleep(0.02)		#给信号提示传感器开始工作
        GPIO.output(channel, GPIO.HIGH)
        GPIO.setup(channel, GPIO.IN)

        while GPIO.input(channel) == GPIO.LOW:
            continue

        while GPIO.input(channel) == GPIO.HIGH:
            continue

        # 传感器发送40bit数据
        while j < 40:
            k = 0
            while GPIO.input(channel) == GPIO.LOW:
                continue

            while GPIO.input(channel) == GPIO.HIGH:
                k += 1
                if k > 100:
                    break

            if k < 8:
                data.append(0)
            else:
                data.append(1)

            j += 1

        print("sensors is working.")
        print(data)				#输出初始数据高低电平

        humidity_bit = data[0:8]		#分组
        humidity_point_bit = data[8:16]
        temperature_bit = data[16:24]
        temperature_point_bit = data[24:32]
        check_bit = data[32:40]

        humidity = 0
        humidity_point = 0
        temperature = 0
        temperature_point = 0
        check = 0

        for i in range(8):
            humidity += humidity_bit[i] * 2 ** (7 - i)				#转换成十进制数据
            humidity_point += humidity_point_bit[i] * 2 ** (7 - i)
            temperature += temperature_bit[i] * 2 ** (7 - i)
            temperature_point += temperature_point_bit[i] * 2 ** (7 - i)
            check += check_bit[i] * 2 ** (7 - i)

        tmp = humidity + humidity_point + temperature + temperature_point		#十进制的数据相加

        if check == tmp:								#数据校验，相等则输出
            print("temperature : ", temperature, ", humidity : " , humidity)
        else:										#错误输出错误信息，和校验数据
            print("wrong temperature: ", temperature, ", humidity: " , humidity, " check: ", check, " tmp: ", tmp)
            temperature = humidity = 0

        GPIO.cleanup()

        return {
            "temperature": temperature,
            "humidity": humidity
        }

if __name__ == "__main__":
    Temperature.get(18)
