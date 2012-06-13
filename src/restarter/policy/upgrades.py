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


def upgrade_0004_to_0005(setuptool, logger=None):
    setuptool.runAllImportStepsFromProfile('profile-restarter.policy:upgrade_0004_to_0005')


def upgrade_0005_to_0006(context, logger=None):
    context.runAllImportStepsFromProfile('profile-restarter.policy:upgrade_0005_to_0006')


def upgrade_0006_to_0007(context, logger=None):
    catalog = getToolByName(context, 'portal_catalog')
    catalog.addIndex('city', 'FieldIndex')
    catalog.addIndex('province', 'KeywordIndex')
    catalog.addIndex('product_category', 'KeywordIndex')
    catalog.addIndex('company_type', 'KeywordIndex')
    catalog.addIndex('company_sectore', 'KeywordIndex')
