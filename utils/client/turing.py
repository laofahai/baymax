import requests
from utils.configure import Configure


class Turing:

    apiKey = None
    userId = 140321

    @staticmethod
    def init():
        if not Turing.apiKey:
            Turing.apiKey = Configure.get("turing", "API_KEY")

    @staticmethod
    def ask(question):
        Turing.init()
        return Turing.v1(question)

    @staticmethod
    def v1(question):
        response = requests.post("http://www.tuling123.com/openapi/api", data={
            "key": Turing.apiKey,
            "info": question,
            "userid": Turing.userId}
        )
        return response.json()

    @staticmethod
    def v2( question):

        data =  {
            "reqType": 0,
            "perception": {
                "inputText": {
                    "text": question
                },
                "selfInfo": {
                    "location": {
                        "province": "山东省",
                        "city": "诸城市",
                        "street": "密州街道"
                    }
                }
            },
            "userInfo": {
                "apiKey": Turing.apiKey,
                "userId": "140321"

            }
        }

        response = requests.post("http://openapi.tuling123.com/openapi/api/v2", data = data)
        return response.json()
