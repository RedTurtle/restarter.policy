import time
import logging
import transaction

from App.config import getConfiguration
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName
from ZODB.POSException import ConflictError

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from .interfaces import IStatsSettings


def run(app, args):
    # Adjust root logging handler levels
    level = getConfiguration().eventlog.getLowestHandlerLevel()
    root = logging.getLogger()
    for handler in root.handlers:
        handler.setLevel(level)

    logger = logging.getLogger("restarter.policy")
    logger.setLevel(level)
    logger.info("looking for sites...")

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
    while True:
        for tool, settings in tasks:
            # Synchronize database
            tool._p_jar.sync()
            if tool.update():
                transaction.get().note('updated stats')
                try:
                    transaction.commit()
                except ConflictError:
                    logger.warn('transaction aborted')
                    transaction.abort()
        time.sleep(settings.interval)

