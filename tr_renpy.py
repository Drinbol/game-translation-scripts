from googletrans import Translator
import os
import tempfile
import json
import requests
import re

def tranlate(source, direction):
    url = "http://api.interpreter.caiyunai.com/v1/translator"

    # 从环境变量读取彩云小译 token（https://fanyi.caiyunapp.com/ 申请）
    token = os.environ.get("CAIYUN_TOKEN", "")

    payload = {
        "source": source,
        "trans_type": direction,
        "request_id": "demo",
        "detect": True,
    }

    headers = {
        "content-type": "application/json",
        "x-authorization": "token " + token,
    }

    response = requests.request(
        "POST", url, data=json.dumps(payload), headers=headers)

    return json.loads(response.text)["target"]


# 配置
input_directory = "hscene"  # 原始游戏文件的文件夹
input_file = "amaterasu_03.rpy"  # 原始日语文本文件名


'''
# 创建一个临时文件用于存储修改后的内容
with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False) as temp_f:
    with open(os.path.join(input_directory, input_file), "r", encoding="utf-8") as f_in:
        translation_flag = False
        for line in f_in:
            if line.startswith("    # \"") and line.endswith("\"\n"):
                print(line)
                original_text = line.strip("# \"\n")
                translated = tranlate(original_text, "ja2zh")
                temp_f.write(f'    # "{translated}"\n')
            elif line.startswith("    \"") and line.endswith("\"\n"):
                temp_f.write(f'"{translated}"\n')
                print(translated)
            else:
                temp_f.write(line)
'''

temp_f = tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False)
with open(os.path.join(input_directory, input_file), "r", encoding="utf-8") as f_in:
    translation_flag = False
    for line in f_in:
        if line.startswith("    # \"") and line.endswith("\"\n"):
            speaker, content = re.findall(r'"(.*?)"', line)
            translated_text = tranlate(content, "ja2zh")
            print(content)
            print(translated_text)
            temp_f.write(f'    # "{speaker}" "{translated_text}"\n')
        elif line.startswith("    \"") and line.endswith("\"\n"):
            speaker, content = re.findall(r'"(.*?)"', line)
            temp_f.write(f'    "{speaker}" "{translated_text}"\n')
        else:
            temp_f.write(line)
temp_f.close()
# 将修改后的内容覆盖到原文件中
with open(os.path.join(input_directory, input_file), "w", encoding="utf-8") as f_out:
    with open(temp_f.name, "r", encoding="utf-8") as temp_f_read:
        f_out.write(temp_f_read.read())

# 删除临时文件
temp_f.close()
os.unlink(temp_f.name)
