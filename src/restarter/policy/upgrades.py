import logging
from Products.CMFCore.utils import getToolByName

PROFILE_ID='profile-restarter.policy:default'


def add_assc_roles(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('restarter.policy')

    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'rolemap')
    logger.info("New assoc role added.")