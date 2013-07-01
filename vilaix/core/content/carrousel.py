"""Definition of the Carrousel contenttype
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.Archetypes.atapi import *

from vilaix.core.interfaces import ICarrousel
from vilaix.core.config import PROJECTNAME

from Products.ATVocabularyManager import NamedVocabulary

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

#    atapi.LinesField(
#        name='esplugues_temes',
#        widget=atapi.MultiSelectionWidget(
#                format="select",
#                label = 'Esplugues per temes',
#                description = 'Selecciona les categories a les que pertany aquest element', 
#                label_msgid='temes_label',
#                description_msgid='temes_help',
#                i18n_domain='vilaix.core',
#        ),
#        languageIndependent=True,
#        multiValued=False,
#        schemata="categorization",
#        vocabulary=NamedVocabulary('temes_keywords'),
#        enforceVocabulary = True,
#    ),
#
#    atapi.LinesField(
#        name='esplugues_persones',
#        widget=atapi.MultiSelectionWidget(
#                format="select",
#                label = 'Esplugues per les persones',
#                description = 'Selecciona les categories a les que pertany aquest element',
#                label_msgid='persones_label',       
#                description_msgid='persones_help',
#                i18n_domain='vilaix.core',
#        ),
#        languageIndependent=True,
#        multiValued=False,
#        schemata="categorization",
#        vocabulary=NamedVocabulary('persones_keywords'),
#        enforceVocabulary = True,
#    ),
#
#    atapi.LinesField(
#        name='esplugues_xifres',
#        widget=atapi.MultiSelectionWidget(
#                format="select",
#                label = 'Esplugues per les xifres',
#                description = 'Selecciona les categories a les que pertany aquest element',
#                label_msgid='xifres_label',       
#                description_msgid='xifres_help',                                 
#                i18n_domain='vilaix.core',
#        ),
#        languageIndependent=True,
#        multiValued=False,
#        schemata="categorization",
#        vocabulary=NamedVocabulary('xifres_keywords'),
#        enforceVocabulary = True,
#    ),
#
#    atapi.LinesField(
#        name='esplugues_barris',
#        widget=atapi.MultiSelectionWidget(
#                format="select",
#                label = 'Esplugues per barris', 
#                description = 'Selecciona les categories a les que pertany aquest element',
#                label_msgid='barris_label',       
#                description_msgid='barris_help',                                
#                i18n_domain='vilaix.core',
#        ),
#        languageIndependent=True,
#        multiValued=False,
#        schemata="categorization",
#        vocabulary=NamedVocabulary('barris_keywords'),
#        enforceVocabulary = True,
#    ),

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
