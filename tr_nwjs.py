import os
import re

import json
import requests


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

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    return json.loads(response.text)["target"]


def process_file(scene_id):
    script_file = f"scenes/{scene_id}/script.txt"
    output_file = "data/scripts/data/sceneData.js"

    with open(script_file, "r", encoding="utf-8") as file:
        content = ""
        for line in file:
            if line.strip():
                content += line

    lines = content.split('\n')
    modified_lines = []

    for index, line in enumerate(lines):
        if not re.search(r'<.*>', line):
            parts = line.split('\\n')
            translated_parts = []
            for part in parts:
                if part:
                    translated_parts.append(tranlate(part,"ja2zh"))
                else:
                    translated_parts.append(part)
            print(translated_parts)
            modified_lines.append('\\n'.join(translated_parts))
        else:
            modified_lines.append(line)

    with open(output_file, "r", encoding="utf-8") as file:
        scene_data = json.loads(re.sub(r"sceneData\s*=\s*", "", file.read()))

    scene_data[scene_id]["SCRIPTS"]["PART1"]["SCRIPT"] = modified_lines

    output_content = "sceneData = " + json.dumps(scene_data, ensure_ascii=False, indent=4)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(output_content)

if __name__ == "__main__":
    scene_id = "c100841"  # 输入对应的scene_id
    process_file(scene_id)