#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import json

class BaseItem():

    @classmethod
    def decode_object(cls, d):
        item = cls()
        item.update(d)
        return item
    def update(self,d):
        self.__dict__.update(d)

class Comment(BaseItem):
    def __init__(self):
        self.userid = 0
        self.workid = 0
        self.ownerid = 0
        self.content = ''

    ##override
    def update(self,d):
        self.userid = int(d.get('userid',0))
        self.ownerid = int(d.get('ownerid', 0))
        self.workid = int(d.get('workid', 0))
        self.content= d.get('content','')
