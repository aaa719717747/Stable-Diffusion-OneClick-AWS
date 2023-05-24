import openai
import os
from tiktoken import Tokenizer, TokenCount


class ChatGPT:
    def __init__(self):
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        #
        # openai.proxy = "10.22.1.78:9999"
        # openai.proxy = "192.168.101.12:12307"
        self.history = []
        self.Tokens = 0
        self.tokenizer = Tokenizer()

    # 默认输入的信息中，包含场景，人物，动物，植物，颜色，建筑物那么我们将会直接提取然后出图
    import json

    def count_tokens(self, text):
        token_count = TokenCount()
        token_count.add_tokens(self.tokenizer.tokenize(text))
        return token_count.num_tokens

    # 切换剧本
    def changedscript_gpt(self):
        self.history.clear()
        self.Tokens = 0
        return "clear"

    def request_gpt_quesion(self, user_Input):
        self.history.append(f'user:{user_Input}')
        self.Tokens += self.count_tokens(user_Input)

        while self.Tokens >= 4000:
            oldest_msg = self.history.pop(-2)
            self.Tokens -= self.count_tokens(oldest_msg)

        print(f'Tokens:{self.Tokens}')
        result = "".join(str(value) for value in self.history)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": result}]
        )

        s = response['choices']

        # 获取第一个响应对象
        response_obj = s[0]
        # 获取 "content" 的值
        content = response_obj["message"]["content"]
        self.history.append(f'ai:{content}')

        return content
