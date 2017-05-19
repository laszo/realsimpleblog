import codecs
import ConfigParser
import os
import re

import jinja2
import markdown
import yaml

config = ConfigParser.RawConfigParser()
config.read('config')
blog_title = config.get('Main', 'blog_title')

def get_files(top, ext):
    for dirpath, dirnames, filenames in os.walk(top):
        for fn in filenames:
            if fn.endswith(ext):
                yield os.path.join(dirpath, fn)

def read_file_content(file_path):
    stream = codecs.open(file_path, 'r', encoding='utf8')
    return stream.read()

def write_to_file(content, file_path):
    stream = codecs.open(file_path, "w", encoding="utf-8", errors="xmlcharrefreplace")
    stream.write(content)

def render(template, mkdtxt, **kwargs):
    kwargs['blog_title'] = blog_title
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


def get_out_file_path(in_file_path, out_path, ext):
    out_file_name = in_file_path.split('/')[-1].replace(ext, '.html')
    out_file_path = os.path.join(out_path, out_file_name)
    return out_file_path

def process(item_diretory, out_path, item_template, ext):
    if not os.path.exists(out_path) and out_path:
        os.mkdir(out_path)

    items = get_files(item_diretory, ext)
    for i in items:
        mkdtxt, title = readConfig(read_file_content(i))
        html = render(item_template, mkdtxt, title=title)
        out_file_path = get_out_file_path(i, out_path, ext)
        write_to_file(html, out_file_path)
        yield title, out_file_path

def make_index(posts, pages):
    index_template = read_file_content(config.get('Template', 'index'))
    html = render(index_template, '', postlinks=posts, pagelinks=pages)
    write_to_file(html, 'index.html')

def main():
    post_path = config.get('Main', 'post_path')
    page_path = config.get('Main', 'page_path')
    post_output_path = config.get('Main', 'post_output_path')
    page_output_path = config.get('Main', 'page_output_path')

    ext = config.get('Main', 'file_extention')

    post_template = read_file_content(config.get('Template', 'post'))
    page_template = read_file_content(config.get('Template', 'page'))

    posts = list()
    for post in process(post_path, post_output_path, post_template, ext):
        posts.append(post)

    pages = list()
    for page in process(page_path, page_output_path, page_template, ext):
        pages.append(page)

    # pages.append(('Blog', 'index.html'))
    make_index(posts, pages)

if __name__ == '__main__':
    main()

