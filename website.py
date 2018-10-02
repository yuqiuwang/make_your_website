# -*- coding: utf-8 -*-
"""
Author  : yuqiuwang
Mail    : yuqiuwang929@gmail.com
Website : https://www.yuqiulearn.cn
Created : 2018/8/2 14:52
"""

import os
import re
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import random
import time

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))
import run_mysql
import config


def cut_pages(page_index, page_type):
    if re.findall('[a-z]{2}\d+', page_index):
        m = re.findall('([a-z]{2})(\d+)', page_index)[0]
        tags, pages = m
        if tags == "al":
            results = run_mysql.main("find_data", "all", " ", " ")
        elif re.findall('^[a-z]{2}$', tags):
            results = run_mysql.main("find_data", "one", "TAG", tags)
    else:
        m = re.findall('(.+?)(\d+)', page_index)[0]
        tags, pages = m
        results = run_mysql.main("find_data", "ctn", "TEXT", tags)
    new_results = []
    page_infos = []
    results.reverse()  # 反向 记录靠前的排在最后
    for idx, result in enumerate(results):
        if idx % config.WebConfig.items_page == 0:
            new_results.append([])
            page_infos.append("/%s/%s%d" % (page_type, tags, (idx / config.WebConfig.items_page)))
        new_results[-1].append(result)
    results = new_results[int(pages)]
    for x in range(0, len(results)):
        # 截取前三行
        tmp_line = "\n".join(results[x][3].split("\n")[:4])
        results[x][3] = tmp_line.replace("<p>", "").replace("</p>", "").replace("<h2>", "").replace("</h2>", "") + "..."
    return results, pages, page_infos


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/index", IndexHandler),
            (r"/blog/(.*)", PageHandler),
            (r"/entry/(.*)", EntryHandler),
            (r"/tool/(.*)", ToolHandler),
            (r"/query", SearchHandler),
            (r"/query/(.*)", SearchHandler),
            (r"/touch", TouchHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=False,
            )
        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')

class TouchHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('touch.html')

class SearchHandler(tornado.web.RequestHandler):

    def get(self, page_index):
        try:
            results, pages, page_infos = cut_pages(page_index, "query")
            self.render('blog_title.html', entrys=results, page_num=int(pages), page_infos=page_infos)
        except:
            self.redirect("/index")

    def post(self):
        query = self.get_argument('query')
        query = query + "0"
        self.redirect("/query/" + query)


class PageHandler(tornado.web.RequestHandler):

    def get(self, page_index):
        if re.findall('[a-z]{2}\d+', page_index):
            results, pages, page_infos = cut_pages(page_index, "blog")
            self.render('blog_title.html', entrys=results, page_num=int(pages), page_infos=page_infos)
        else:
            raise tornado.web.HTTPError(404)


class EntryHandler(tornado.web.RequestHandler):

    def get(self, entry_index):
        try:
            entry = run_mysql.main("find_data", "one", "name_id", entry_index)
            self.render('blog.html', entrys=entry[0])
        except:
            raise tornado.web.HTTPError(404)


class ToolHandler(tornado.web.RequestHandler):

    def get(self, draw_type):
        self.render('tool.html', draw_type=draw_type, state="not_draw", save_name="None")

    def post(self, draw_type):
        save_type = self.get_argument('save-type')
        #color = self.get_argument('color')
        submit = self.get_argument('submit')
        if draw_type == "heatmap":
            color = self.get_argument('color')
            if not color:
                color = "RdYlBu_r"
        if draw_type == "K_means":
            clusters = self.get_argument('clusters')
            if not clusters:
                clusters = 2
            clusters = int(clusters)
        if not save_type:
            save_type = "png"
        if submit:
            upload_path = os.path.join(os.path.dirname(__file__), 'static', 'files')  # 文件的暂存路径
            file_metas = self.request.files.get('file', None)  # 提取表单中‘name’为‘file’的文件元数据
            if not file_metas:
                raise tornado.web.HTTPError(404)
            for meta in file_metas:
                filename = meta['filename']
                current_time = time.strftime('%Y%m%d', time.localtime(time.time()))
                filename = current_time+str(random.randint(0, 10000000))+"."+filename.split(".")[-1]
                file_path = os.path.join(upload_path, filename)
                with open(file_path, 'wb') as up:
                    up.write(meta['body'])
        if os.path.exists(file_path):
            if draw_type == "heatmap":
                drawing_cls = config.DrawingConfig(file_path, save_type, color)
                drawing_cls.heatmap
            elif draw_type == "pca":
                drawing_cls = config.DrawingConfig(file_path, save_type)
                drawing_cls.pca
            elif draw_type == "K_means":
                drawing_cls = config.DrawingConfig(file_path, save_type="png", color="non", clusters=clusters)
                drawing_cls.K_means
        if draw_type == "K_means":
            save_type = "zip"
            file_path = file_path.replace(".xlsx","").replace(".txt","").replace(".csv","")
        if os.path.exists(file_path+"."+save_type):
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition', 'attachment; filename=' + filename+"."+save_type)
            with open(file_path+"."+save_type, 'rb') as f:
                while True:
                    data = f.read()
                    if not data:
                        break
                    self.write(data)
            #self.render('tool.html', draw_type="heatmap", state="draw", file_name=filename + "." + save_type)
            self.finish()


def main():
    define("port", default=8080, help="run on the given port", type=int)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    #http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
