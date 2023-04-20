import os
import re
import json

import openai


class ChatGPT:
    def __init__(self):
        self.result = ""
        openai.api_key = "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"
        #
        # openai.proxy = "10.22.1.78:9999"
        # openai.proxy = "192.168.101.12:12307"
        self.history = []

    def pre_command_begin(self):
        self.pre_prompts = []

        self.txtcontent = open('prompt.txt', encoding='utf-8')
        self.promptSdTip = self.txtcontent.read()
        self.txtcontent1 = open('prompt_1.txt', encoding='utf-8')
        self.promptSdTip1 = self.txtcontent1.read()
        self.txtcontent2 = open('prompt_2.txt', encoding='utf-8')
        self.promptSdTip2 = self.txtcontent2.read()
        self.pre_prompts.append(self.promptSdTip)
        self.pre_prompts.append(self.promptSdTip1)
        self.pre_prompts.append(self.promptSdTip2)
        self.index_prompt = 0

        for client in range(3):
            responese = self.request_gpt_quesion(self.pre_prompts[self.index_prompt])
            if responese:
                self.history.append(self.pre_prompts[self.index_prompt])
                self.index_prompt += 1

        print("预处理完毕！")

    # 默认输入的信息中，包含场景，人物，动物，植物，颜色，建筑物那么我们将会直接提取然后出图
    import json

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
        print(f"AI:{content}")
        # self.history.append({"role": "ai", "content": content})
        self.history.append(f'旁白:[{content}]')
        if len(self.history) >= 15:
            self.history.pop(9)

        print(f'最新的历史:{self.history}')
        return content
