from zope.interface import Interface

class ISkin(Interface):
    """ A layer specific to this product.
    this layer is registered using browserlayer.xml in the package 
    default GenericSetup profile
    """

class ISimpleAddButtons(Interface):
    """Marker interface that tells when to use simple add buttons"""
