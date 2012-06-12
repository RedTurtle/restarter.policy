# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from zope.interface import implements

from restarter.policy.interfaces import IRestarterConfiguration


class RestarterConfig(BrowserView):

    implements(IRestarterConfiguration)

    def isHomePage(self):
        return True
