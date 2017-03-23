import re

def splitText(text, maxBytes):
  text = re.sub(r"\n+", "\n", text)
  # every chinese char == 3 bytes
  maxChineseChar = maxBytes // 3 + 1
  idx = 0
  parts = []
  while idx < len(text):
    parts.append(text[idx : (idx + maxChineseChar)])
    idx += maxChineseChar
  return parts

tex = """
既然发出祝福的人可以从网上复制一条段子，甚至可能是随手复制七大姑八大姨群发给TA自己的段子，然后在微信群发助手全选联系人，往里面一粘贴点击发送就成功地搞定了所有过去的一年里爱过帮助过鼓励过同舟共济过的亲朋好友们。



那我为什么不可以用类似的方式去搞定企图用群发来搞定我的人呢？

不过我也不是批评群发祝福这种行为，敷衍确实是敷衍了一点，多少也算一份心意。

可是收到祝福的我就很尴尬了，假如我不回显得我不近人情，我要是手动回复了，很明显是我吃亏了，可能一整天的精力都要耗在回复祝福上。并且我也不愿意做那种群发祝福敷衍我的亲朋好友的那种人。

有没有既不浪费时间又能保持礼貌和客套的办法呢？
好歹也算是学过两年编程的人，其实只需要12行Python代码，就可以让你的微信拥有自动回复功能了，并且还能够自动判断消息种类和内容，只回复新年祝福相关的消息。

首先确保你安装好了Python和Python的包管理工具pip
感谢知友们的支持，更新一个进阶版，可以自动获取好友的备注名，并且从祝福语API里随机抽取祝福词进行定制的回复，并且会记录回复过的好友，不会因为重复自动回复露馅。
"""

ll = splitText(tex, 1024)
print(len(ll))
print(ll[0])