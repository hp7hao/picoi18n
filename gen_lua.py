#coding: utf-8

import re

from PIL import Image, ImageDraw, ImageFont
from typing import Tuple

class PILFont():
    def __init__(self, font_path: str, font_size: int) -> None:
        self.__font = ImageFont.FreeTypeFont(font_path, font_size)
    
    def render_text(self, text: str, offset: Tuple[int, int] = (0, 0)) -> Image:
        ''' 绘制文本图片
            > text: 待绘制文本
            > offset: 偏移量
        '''
        box = self.__font.getbbox(text)
        print(box)
        __left, __top, right, bottom = self.__font.getbbox(text)
        img = Image.new("1", (right, bottom), color=255)
        img_draw = ImageDraw.Draw(img)
        img_draw.text(offset, text, fill=0, font=self.__font, spacing=0)
        return img
    
    def tohex(self, character: str, offset: Tuple[int, int] = (0, 0)) -> str:
        '''
            character: single chinese character
        '''
        __left, __top, right, bottom = self.__font.getbbox(character)
        if right <= 4:
            width = 4
        else:
            width = 8
        img = Image.new("1", (right, bottom), color=255)
        img_draw = ImageDraw.Draw(img)
        img_draw.text(offset, character, fill=0, font=self.__font, spacing=0)
        hexstr = ''
        for y in range(0, bottom):
            line = ''
            for x in range(0, right):
                pix = img.getpixel((x, y))
                if pix == 0:
                    line += '1'
                else:
                    line += '0'
            print(line)
            if width == 8:
                hexstr += str(hex(int(line, 2)))[2:].zfill(2)
            else:
                hexstr += str(hex(int(line, 2)))[2:]

        if width == 8:
            hexstr = hexstr[::-1].zfill(16)[::-1]
            hexstr = self.cut(hexstr)
        else:
            hexstr = hexstr[::-1].zfill(8)[::-1]
        return hexstr
    
    def cut(self, hexstr):
        ret = ""
        for i in range(0, 16, 2):
            ret += hexstr[i]
        for i in range(1, 16, 2):
            ret += hexstr[i]
        return ret

f = PILFont("carts/projects/tools/guanzhi.ttf", 8)
# 渲染文本
# im = f.render_text("a")
# im.show();
# print('\n' + f.tohex('一', (0, -1)))
# 渲染单个文字，可用于生成字体
# im = f.render_text("一", (0, -1))
# im.show()

def to_hex(text):
  hexstr = ''
  for ch in text:
    hexstr += f.tohex(ch, (0, -1))
  return hexstr

# read all texts
lang = 'zh_CN'
translation_file = 'carts/projects/langtest/texts.{}.txt'.format(lang)
translations = {}
with open(translation_file, 'r') as inf:
  lines = inf.readlines()
  for line in lines:
    if line:
      kv = re.findall('"(.+?)"', line)
      translations[kv[0]] = to_hex(kv[1])
      print(translations[kv[0]])

# save lua files
lua_file = 'carts/projects/langtest/texts.lua'
lines = [
   'lang="{}"'.format(lang),
   'texts={}'
]
for k, v in translations.items():
    lines.append('texts["{}"]="{}"'.format(k, v))

with open(lua_file, 'w') as outf:
    for line in lines:
       outf.write(line)
       outf.write('\n')