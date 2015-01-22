#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import lxml.html
import sys
from slot import slot

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

def fetch(doc, slot):
    ele = locate(doc, slot[0])
    return find(ele, slot[1])

def find(tree, slot):
    def match(node, slot):
        if node.tag == slot[0]:
            for i in slot[1]:
                if slot[1][i] != node.attrib.get(i):
                    return False
        else:
            return False
        return True
    def getURL(node):
        return node.attrib["href"]

    urls = []
    depth = 0
    children = [tree.getchildren()] #a stack which stores all children of the relavent parent
    used = [0] #last used element of children[depth]
    while depth >= 0:
        if used[depth] >= len(children[depth]):
            children.pop()
            used.pop()
            depth -= 1
            continue
        x = children[depth][used[depth]]
        used[depth] += 1
        if match(x, slot[depth]):
            if depth == len(slot)-1:
                urls.append(getURL(x))
            else:
                children.append(x.getchildren())
                used.append(0)
                depth += 1
    return urls

def parse(url, website):
    doc = lxml.html.parse(url).getroot()
    title = doc.head.find("title").text
    return title, fetch(doc.body, slot[website])

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
