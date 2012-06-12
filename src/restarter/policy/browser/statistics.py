# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
import pprint


class StatisticsView(BrowserView):
    def __call__(self):
        tool = getToolByName(self.context, 'portal_stats')
        return "<pre>%s</pre>" % pprint.pformat(tool.getStats())
