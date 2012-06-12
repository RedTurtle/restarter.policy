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

def add_story_ct(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('restarter.policy')

    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'typeinfo')
    logger.info("CompanyStory added.")

def add_employee_role(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('restarter.policy')

    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'rolemap')
    logger.info("New employee role added.")

    catalog = getToolByName(context, 'portal_catalog')
    catalog.addIndex('company_employees', 'KeywordIndex')




