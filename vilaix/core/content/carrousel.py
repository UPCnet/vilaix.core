"""Definition of the Carrousel contenttype
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.Archetypes.atapi import *

from vilaix.core.interfaces import ICarrousel
from vilaix.core.config import PROJECTNAME

CarrouselSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    ImageField(
        name='Imatge',
        widget=ImageField._properties['widget'](
            label='Image',
            label_msgid='lbl_Imatge',
            i18n_domain='vilaix.core',
        ),
        storage=AttributeStorage(),
    ),
    StringField(
        name='URLdesti',
        widget=StringField._properties['widget'](
            label='Urldesti',
            description="You must include http:// at the beginning to make an external link",            
            label_msgid='lbl_UrlDesti',
            description_msgid='lbl_HelpDescription',            
            i18n_domain='vilaix.core',
        ),
    ),
    BooleanField(
        name='Obrirennovafinestra',
        widget=BooleanField._properties['widget'](
            label='Open in a new window',
            label_msgid='lbl_ObrirEnFinestraNova',
            i18n_domain='vilaix.core',
        ),
    ),


))


CarrouselSchema['title'].storage = atapi.AnnotationStorage()
CarrouselSchema['description'].storage = atapi.AnnotationStorage()
# Hide default category option
CarrouselSchema['subject'].widget.visible = {'view': 'invisible', 'edit':'invisible'}
CarrouselSchema['relatedItems'].widget.visible = False
CarrouselSchema['language'].widget.visible = False

schemata.finalizeATCTSchema(CarrouselSchema, moveDiscussion=False)



class Carrousel(base.ATCTContent):
    """Description of the Example Type"""
    implements(ICarrousel)

    meta_type = "Carrousel"
    schema = CarrouselSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')


atapi.registerType(Carrousel, PROJECTNAME)
