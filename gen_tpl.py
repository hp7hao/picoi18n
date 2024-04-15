#coding: utf-8
import re
import os

lang = 'zh_CN'
input_file = 'carts/projects/langtest/langtest.p8'
translation_file = 'carts/projects/langtest/texts.{}.txt'.format(lang)

texts = set()
dictionary = {}
# read lua file
with open(input_file, 'r') as inf:
    lines = inf.readlines()
    flag = False
    for line in lines:
        if '__lua__' in line:
            flag = True
            continue
        if '__gfx__' in line:
            break
        if flag:
            matched = re.findall('_\("(.+?)"', line)
            print(matched)
            if len(matched) > 0:
                for m in matched:
                    texts.add(m)

# generate texts.zh_CN.txt
# delete output file first
translations = {}
if os.path.exists(translation_file):
    with open(translation_file, 'r') as inf:
        lines = inf.readlines()
        for line in lines:
            kv = re.findall('"(.+?)"', line)
            translations[kv[0]] = kv[1]
    os.remove(translation_file)

lines = []
for text in texts:
    v = ""
    if text in translations:
        v = translations[text]
    lines.append('texts["{}"]="{}"\n'.format(text, v))

with open(translation_file, 'w') as outf:
    outf.writelines(lines)