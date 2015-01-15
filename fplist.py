#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import lxml.html
import sys

def locate(doc, slot):
    """
    Locate the HTML tree to the smallist subtree which is iterable and 
    contains all the wanted informations (eg. URLs).
    """
    dep = 0
    for ele in doc.iter():
        if ele.tag == slot[dep][0]:
            attr = ele.attrib
            flag = True
            for i in slot[dep][1]:
                if slot[dep][1][i] != attr.get(i):
                    flag = False
                    break
            if flag:
                dep += 1
        if dep == len(slot):
            return ele

def fetch_iqiyi(doc, slot):
    ele = locate(doc, slot)
    lis = ele.getchildren()
    urls = []
    for i in lis:
        if i.tag == "li" and i.attrib.get("class") == "album_item":
            url = i.getchildren()[0].attrib.get("href")
            urls.append(url)
    return urls

def parse(url, website):
    slots = {
            "iqiyi":(
                ("div", {"data-tab-body":"widget-tab-3"}),
                ("div", {"data-widget":"albumlist-render"}),
                ("ul", {"class":"clearfix", "data-albumlist-elem":"cont"})),
           }
    doc = lxml.html.parse(url).getroot()
    title = doc.head.find("title").text
    return title, globals()["fetch_"+website](doc.body, slots[website])

def main(url, website):
    title, urls = parse(url, website)
    print(title)
    for a in urls:
        print(a, end=' ')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Useage: "+sys.argv[0]+" url website-name")
    else:
        main(sys.argv[1], sys.argv[2])
