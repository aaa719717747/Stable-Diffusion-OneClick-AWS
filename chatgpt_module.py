import openai
import os


class ChatGPT:
    def __init__(self):
        self.result = ""
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        #
        # openai.proxy = "10.22.1.78:9999"
        # openai.proxy = "192.168.101.12:12307"
        self.history = []

    # 默认输入的信息中，包含场景，人物，动物，植物，颜色，建筑物那么我们将会直接提取然后出图
    import json

    # 切换剧本
    def changedscript_gpt(self, scriptcontent):
        self.history.clear()
        return self.request_gpt_quesion(scriptcontent)

    def request_gpt_quesion(self, user_Input):
        # self.history.append({"role": "user", "content": user_Input})
        self.history.append(f'玩家:[{user_Input}]')
        self.result = ""
        self.result = "".join(str(value) for value in self.history)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": self.result}]
        )

        s = response['choices']

        # 获取第一个响应对象
        response_obj = s[0]
        # 获取 "content" 的值
        content = response_obj["message"]["content"]
        # self.history.append({"role": "ai", "content": content})
        self.history.append(f'旁白:[{content}]')
        if len(self.history) >= 15:
            self.history.pop(9)

        return content
