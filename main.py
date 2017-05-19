# -*- coding: utf-8 -*-
__author__ = 'laszo'
import os
import re
import yaml
import codecs
import markdown
import jinja2
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config')
blog_title = config.get('Main', 'blog_title')

def get_files(top, ext):
    for dirpath, dirnames, filenames in os.walk(top):
        for fn in filenames:
            if fn.endswith(ext):
                yield os.path.join(dirpath, fn)

def foo():
    post_path = config.get('Main', 'post_path')
    page_path = config.get('Main', 'page_path')
    ext = config.get('Main', 'file_extention')
    post_template = read_file_content(config.get('Template', 'post'))
    page_template = read_file_content(config.get('Template', 'page'))

    posts = get_files(post_path, ext)
    pages = get_files(page_path, ext)

    for po in posts:
        mkdtxt, title = readConfig(read_file_content(po))
        html = render(post_template, mkdtxt, title=title)
        outfile = po.replace(ext, '.html')
        write_to_file(html, outfile)

def read_file_content(file_path):
    stream = codecs.open(file_path, 'r', encoding='utf8')
    return stream.read()

def write_to_file(content, file_path):
    stream = codecs.open(file_path, "w", encoding="utf-8", errors="xmlcharrefreplace")
    stream.write(content)

def render(template, mkdtxt, **kwargs):
    kwargs['content'] = markdown.markdown(mkdtxt)
    html = jinja2.Template(template).render(kwargs)
    return html

def readConfig(text):
    get_header = re.compile(r'---[\s\S]*?---')
    header = get_header.findall(text)[0]
    content = text.replace(header, '', 1)
    header = header.replace('---', '')
    post_info = yaml.load(header)
    title = ''
    for item in post_info:
        if item.upper() == 'title'.upper():
            title = post_info[item]
    return content, title

def createPost(post):
    text = codecs.open(contentpath + post, 'r', encoding='utf8').read()
    mkdtxt, title = readConfig(text)
    content = markdown.markdown(mkdtxt)
    t = codecs.open(postTemplatePath, 'r', encoding='utf8').read()
    html = Template(t).render(content=content, title=title, blogtitle=blogtitle)

    outfile = outpath + os.path.splitext(post)[0] + '.html'
    output_file = codecs.open(outfile, "w", encoding="utf-8", errors="xmlcharrefreplace")
    output_file.write(html)
    return outfile, title


def createPage(page, pagelinks):
    text = codecs.open(pagespath + page, 'r', encoding='utf8').read()
    mkdtxt, title = readConfig(text)
    content = markdown.markdown(mkdtxt)
    t = codecs.open(pageTemplatePath, 'r', encoding='utf8').read()
    html = Template(t).render(content=content, title=title, blogtitle=blogtitle, pagelinks=pagelinks)

    outfile = os.path.splitext(page)[0] + '.html'
    output_file = codecs.open(outfile, "w", encoding="utf-8", errors="xmlcharrefreplace")
    output_file.write(html)
    return outfile, title




def createIndex(postlinks, pagelinks):
    t = codecs.open(indexTemplatePath, 'r', encoding='utf8').read()
    html = Template(t).render(postlinks=postlinks, pagelinks=pagelinks, title=blogtitle)

    outfile = 'index.html'
    output_file = codecs.open(outfile, "w", encoding="utf-8", errors="xmlcharrefreplace")
    output_file.write(html)


def main():
    posts = os.listdir(contentpath)
    posts.reverse()
    postlinks = []
    for p in posts:
        if os.path.isfile(contentpath+p):
            url, title = createPost(p)
            postlinks.append({'title':title, 'url':url})
    pagefiles = os.listdir(pagespath)
    temp_links = []
    for p in pagefiles:
        text = codecs.open(pagespath + p, 'r', encoding='utf8').read()
        mkdtxt, title = readConfig(text)
        outfile = os.path.splitext(p)[0] + '.html'
        temp_links.append({'title':title, 'url':url})
    pagelinks = []
    for p in pagefiles:
        url, title = createPage(p, temp_links)
        pagelinks.append({'title':title, 'url':url})

    createIndex(postlinks, pagelinks)


if __name__ == '__main__':
    # main()
    # set_default_config()
    read_config('config')
