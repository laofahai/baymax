# coding: utf-8
import json
from urllib import request
from utils.configure import Configure
from utils import http

class UNIT:

    accessToken = None

    latestSessionId = "null"

    latestLogId = "null"

    @staticmethod
    def init():
        pass

    @staticmethod
    def getAccessToken():
        if UNIT.accessToken is None:
            clientId = Configure.get("UNIT", "CLIENT_ID")
            clientSecret = Configure.get("UNIT", "CLIENT_SECRET")
            url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + clientId +'&client_secret=' + clientSecret
            response = http.post(url, None)
            UNIT.accessToken = response["access_token"]

        return UNIT.accessToken

    @staticmethod
    def talk(question):
        accessToken = UNIT.getAccessToken()
        # accessToken = "24.4a04ddb4bfad21c6a47a1f21723a6d13.2592000.1556881503.282335-15885624"

        data = {
            "version": "2.0",
            # 机器人ID
            "service_id": "S15930",
            # "bot_id": 44363,
            "log_id": UNIT.latestLogId,
            "session_id": UNIT.latestSessionId,
            "request": {
                "query": question,
                "user_id": 140321, # 修改
            },
            "dialog_state": {

            }
        }

        url = r"https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=" + accessToken
        response = http.post(url, data)

        if int(response["error_code"]) <= 0:
            UNIT.latestSessionId = response["result"]["session_id"]
            UNIT.latestLogId = response["result"]["log_id"]

        return response

    @staticmethod
    def parseSlot(slots):
        cleared = {}

        for slot in slots:
            cleared[slot["name"]] = slot

        return cleared
