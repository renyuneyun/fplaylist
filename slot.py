#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Store slots (patterns) of websites.
This is just a "config" file.
"""

slot = {
        "iqiyi":(
            [
                ("div", {"data-tab-body":"widget-tab-3"}),
                ("div", {"data-widget":"albumlist-render"}),
                ("ul", {"class":"clearfix", "data-albumlist-elem":"cont"}),
                ],
            [
                ("li", {"class":"album_item"}),
                ("a", {}),
                ]
            ),
       }
