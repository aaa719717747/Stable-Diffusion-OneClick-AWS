import threading
import time
import oss2
import random


class OSSUploader:
    def __init__(self, access_key_id, access_key_secret, endpoint, bucket_name):
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)

    def upload_file(self):
        # 读取文件内容
        with open('output_txt2img.png', 'rb') as f:
            content = f.read()

        random_num = random.randint(1, 9999)
        m_key = f"{random_num}_output.png"
        # 上传文件到 OSS
        result = self.bucket.put_object(m_key, content)

        # 获取文件的 URL 地址
        url = self.bucket.sign_url('GET', m_key, 60)  # 这里的 60 表示 URL 的有效时间，单位为秒

        # 开启线程接收客户端发送的消息
        threading.Thread(target=self.delete_file, args=(m_key,)).start()

        return url

    def delete_file(self, key):
        # 延时 10 秒钟
        time.sleep(10)

        # 删除文件
        self.bucket.delete_object(key)
