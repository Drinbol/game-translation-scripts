# game-translation-scripts

游戏文本批量翻译脚本：调用彩云小译 API，把游戏文本批量翻译成中文。

## 脚本

| 脚本 | 适用 | 说明 |
|---|---|---|
| `tr_nwjs.py` | NW.js 游戏 | 处理游戏场景 json，按行翻译并回写 |
| `tr_renpy.py` | Ren'Py 游戏 | 处理 .rpy 文本（googletrans 备选） |

## 准备

```bash
pip install requests googletrans
export CAIYUN_TOKEN="你的彩云小译token"   # https://fanyi.caiyunapp.com/ 申请
```

## 使用

```bash
python tr_nwjs.py    # 按脚本内提示处理对应游戏目录
```

## 许可证

MIT
