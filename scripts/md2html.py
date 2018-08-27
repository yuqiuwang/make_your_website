# -*- coding: utf-8 -*-
"""
Author  : yuqiuwang
Mail    : yuqiuwang929@gmail.com
Website : https://www.yuqiulearn.cn
Created : 2018/8/6 9:45
"""

import sys
import markdown
import codecs
import optparse
import os
import run_mysql
import glob


# 用于将md文件转换为html
# 转换好的html录入mysql数据库


def main(name):
    input_file = codecs.open('%s' % (name), mode="r", encoding="utf-8")
    date, tag, head = os.path.split(name)[-1].replace(".md", "").split("_")
    text = input_file.read()
    html = markdown.markdown(text)
    run_mysql.main("insert_table", head, date, html.replace("\"", "\\\"").replace("\'", "\\\'"), tag)


if __name__ == "__main__":
    prog_base = os.path.split(sys.argv[0])[1]
    parser = optparse.OptionParser()
    parser.add_option("-n", "--name", action="store", type="string", dest="file_name",
                      help="the sample path")
    parser.add_option("-p", "--path", action="store", type="string", dest="path_comp",
                      help="the path compile")
    (options, args) = parser.parse_args()
    if options.file_name is None and options.path_comp is None:
        print(prog_base + ": error: missing required command-line argument.")
        parser.print_help()
        sys.exit(0)
    if options.path_comp is None:
        main(options.file_name)
    elif options.file_name is None:
        paths = glob.glob(options.path_comp)
        for path in paths:
            main(path)
    else:
        print(prog_base + ": only need one argument.")
        parser.print_help()
        sys.exit(0)
