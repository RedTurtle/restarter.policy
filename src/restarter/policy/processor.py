import time
import logging
import datetime
import threading
import transaction
import requests

from itertools import ifilterfalse, tee, ifilter
from cStringIO import StringIO
from Queue import Queue

from App.config import getConfiguration
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName
from ZPublisher.Test import publish_module
from ZODB.POSException import ConflictError

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from .interfaces import IStatsSettings


def partition(pred, iterable):
    """Use a predicate to partition entries into false entries and
    true entries.

    See: http://docs.python.org/dev/library/itertools.html#itertools-recipes.
    """

    t1, t2 = tee(iterable)
    return ifilter(pred, t1), ifilterfalse(pred, t2)


def run(app, args):
    # Adjust root logging handler levels
    level = getConfiguration().eventlog.getLowestHandlerLevel()
    root = logging.getLogger()
    for handler in root.handlers:
        handler.setLevel(level)

    logger = logging.getLogger("restarter.policy")
    logger.setLevel(level)
    logger.info("looking for sites...")

    session = requests.Session(timeout=5)

    tasks = []
    for name, item in app.objectItems():
        if IPloneSiteRoot.providedBy(item):
            try:
                tool = getToolByName(item, 'portal_stats')
            except AttributeError:
                continue

            logger.info("found site '%s'." % name)

            registry = getUtility(IRegistry, context=item)

            try:
                settings = registry.forInterface(IStatsSettings)
            except KeyError:
                logger.warn("settings not available; please reinstall.")
                continue

            tasks.append((tool, settings))

    if not tasks:
        return

    # Enter runloop
    # counter = 0
    while True:
        errors = set()

        for tool, settings in tasks:
            # Synchronize database
            tool._p_jar.sync()

            tool.update()

            transaction.get().note('updated stats')
            try:
                transaction.commit()
            except ConflictError:
                transaction.abort()

        for url in errors:
            logger.warn("error checking: %s." % url)

        time.sleep(settings.interval)

