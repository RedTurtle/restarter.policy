import requests

NOTIFY = 'http://localhost:6543'


def order_added(order, event):
    """Every time an order is created - notify company."""
    pass

def company_added(company, event):
    """Every time a company is added - create substructure."""
    products = company[company.invokeFactory('Products','prodotti')]
    products.setTitle(u'Prodotti')
    media = company[company.invokeFactory('Folder','media')]
    media.setTitle(u'Media')
    company.portal_workflow.doActionFor(media,"publish",comment="Published on company creation")
