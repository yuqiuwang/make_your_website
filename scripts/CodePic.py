# -*- coding: utf-8 -*-
"""
Author  : yuqiuwang
Mail    : yuqiuwang929@gmail.com
Website : https://www.yuqiulearn.cn
Created : 2018/10/17 11:28
"""


from PIL import Image


class CodePic:

    def __init__(self, data_path, save_type="txt"):
        self.my_codes = '''@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''
        self.data_path = data_path
        self.save_type = save_type

    def trans_pic(self, img):
        img = img.convert("L")
        out_pic = []
        for y in range(0, img.size[1]):
            out_pic.append("")
            for x in range(0, img.size[0]):
                gray = img.getpixel((x, y))
                out_pic[-1] += self.my_codes[int(((len(self.my_codes)-1)*gray)/256)]
        return "\r\n".join(out_pic)+"\r\n"

    def file_handle(self, data_path, outfile):
        f = open(data_path, 'rb')
        img = Image.open(f)

        if img.size[1] > 400:
            img = img.resize((int(img.size[0] * 0.075), int(img.size[1] * 0.04)))#调整图片大小
        elif img.size[1] > 40:
            img = img.resize((int(img.size[0] * 0.75), int(img.size[1] * 0.4)))
        else:
            pass

        with open(outfile, 'w+') as fi:
            fi.write(self.trans_pic(img))

        f.close()

    def main(self):
        return self.file_handle(self.data_path, self.data_path+"."+self.save_type)
