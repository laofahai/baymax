# 基于树莓派的儿童机器人 - Baymax
以超能陆战队大白为外观基础制作，软件部分主要使用 Python 开发， 给孩子做点好玩的

语音识别及合成使用了 [百度语音API](http://ai.baidu.com)，语音对话使用了 [百度UNIT](https://ai.baidu.com/unit/home) 及 [图灵机器人](http://www.turingapi.com/)；
音乐及故事接口使用了 酷狗、喜马拉雅的查询接口；

音频播放使用 `pygame.mixer.music`, 录音使用 `pyAudio`

## 设想功能
* 实现一个N自由度的“会动”的机器人
* 实现一个可以识别意图、关联上下文对话的语音交互机器人
* 实现简单的动作交互（如碰拳、拥抱、挥手等等）
* 实现`移动`(考虑用舵机实现双足行走)
* 以及其他各种传感器做出实时处理
* 手机端可以进行一些控制
* and more...

## 目前已实现功能
* 语音识别及对话， 唤醒/休眠/意图识别处理/预设语句处理
* 音乐、故事(不是很好用，主要是m4a格式处理)下载播放
* 音乐控制，暂停/上下首/音量/语速等
* fist bump 碰拳动作

## 目前用到硬件
* 外壳： TB买的 60cm 高的毛绒玩偶，掏掉所有填充物
* Raspberry 3B
* 声卡: WM8960 + 音箱
* PWM: PCA9685  16路PWM信号发生器，用于控制伺服舵机
* 伺服舵机： MG995 / SG90
* DHT11 温湿度传感器
* 其他各种小零件

右臂舵机 index： 从上至下 15/14
左臂舵机 index:  从上至下 11/10

因为大白体型的限制，手臂没有做更多的自由度，暂时先这样

## 目录结构
```
|- abilities # 能力
|- - intentions # 基于 百度 UNIT 的意图实现
|- - sentence # 本地对语句的预置分析
|- base # 基类等
|- - entity # 实体
|- - arm.py # 手臂基类
|- - event.py # 事件基类
|- - organ.py # 器官基类
|- data # 数据存储，音频等
|- - audio # 对话数据
|- - music # 音乐
|- - story # 故事
|- organs # 器官
|- - brain.py / ears / mouth / leftArm / rightArm / skin ... 各器官的具体实现
|- sensors # 传感器
|- utils # 工具
|- baymax.py # 入口
```

## 大致运行流程
上电自动运行唤醒-> 每个器官单独一个线程及处理队列-> 通过 `threading.Event` 来进行线程之间的交互
-> ears / skin 等器官输入并通知到 brain -> brain进行处理后-> 通过 brain.giveCommand 发送命令到器官
-> 器官做出响应(如 mouth.speak / mouth.sing / rightArm.fistBump 等等)

## 遇到的问题
* 用 PCA9685 控制所有舵机，但左右臂目前是两个独立的线程，在同时进行控制的时候，会出现舵机抖动问题，目前暂时通过time.sleep缓解
* 声卡问题，各种掉线 / 突然杂音 / 找不到设备 等等。。
* 舵机抖动
* 图灵接口每天免费调用次数只有100
* 喜马拉雅下载的音频格式是 m4a，但pygame.mixer.music不能播放，用 ffmpeg 转换又太慢
* 线程队列冲突问题


## 改成其他的机器人
后面会把机器人 hard code 的部分放到配置文件，通过设置名字、语调音色语速，改变外壳等等，可以做成其他的机器人 
