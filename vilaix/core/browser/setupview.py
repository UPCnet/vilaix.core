# -*- coding: utf-8 -*-
import loremipsum
import requests
import re
from random import choice

import transaction
from five import grok
from zope.interface import Interface
from zope.interface import alsoProvides

from Products.CMFCore.utils import getToolByName
from plone.namedfile.file import NamedBlobImage
from plone.app.textfield.value import RichTextValue
from plone.dexterity.utils import createContentInContainer

from genweb.core.interfaces import IHomePage
from Products.CMFPlone.interfaces import IPloneSiteRoot

from zope.component.hooks import getSite
from zope.component import queryUtility
from zope.component import getUtility
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from genweb.portlets.browser.manager import ISpanStorage

from datetime import datetime
# from serveiesports.theme.portlets.queryportlet import Assignment as QueryPortletAssignment
# from serveiesports.theme.portlets.utils import setupQueryPortlet, setPortletAssignment

# class setupHomePage(grok.View):
#     grok.context(IPloneSiteRoot)
#     grok.require('zope2.ViewManagementScreens')
#     grok.name("setup-portlets")

#     def render(self):
#         portal = getSite()
#         frontpage = portal['front-page']
#         # Add portlets programatically
#         # target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager2', context=frontpage)
#         # target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
#         # from vilaix.theme.portlets.noticiaDestacada import Assignment as noticiaDestacadaAssignment        
#         # target_manager_assignments['noticiaDestacada'] = noticiaDestacadaAssignment()
  

#         # target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager3', context=frontpage)
#         # target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
#         # target_manager_assignments['buttons'] = homebuttonbarAssignment()
#         # target_manager_assignments['max'] = maxAssignment()

#         portletManager = getUtility(IPortletManager, 'genweb.portlets.HomePortletManager3')
#         spanstorage = getMultiAdapter((frontpage, portletManager), ISpanStorage)
#         spanstorage.span = '8'

#         portletManager = getUtility(IPortletManager, 'genweb.portlets.HomePortletManager6')
#         spanstorage = getMultiAdapter((frontpage, portletManager), ISpanStorage)
#         spanstorage.span = '4'

#         portletManager = getUtility(IPortletManager, 'genweb.portlets.HomePortletManager7')
#         spanstorage = getMultiAdapter((frontpage, portletManager), ISpanStorage)
#         spanstorage.span = '8'

#         portletManager = getUtility(IPortletManager, 'genweb.portlets.HomePortletManager10')
#         spanstorage = getMultiAdapter((frontpage, portletManager), ISpanStorage)
#         spanstorage.span = '4'

#         # target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager4', context=frontpage)
#         # target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
#         # target_manager_assignments['calendar'] = calendarAssignment()
#         # target_manager_assignments['stats'] = statsAssignment()
#         # target_manager_assignments['econnect'] = econnectAssignment()
#         return 'Done.'

#Setup inicial per crear continguts al genweb Vilaix
class SetupView(grok.View):
    """
    """
    grok.context(Interface)
    grok.require("cmf.ManagePortal")
    grok.name("setup-inicial")

    def createOrGetObject(self, context, newid, title, type_name):
        if newid in context.contentIds():
            obj = context[newid]
        else:
            obj = createContentInContainer(context, type_name, title=title, checkConstrains=False)
            transaction.savepoint()
            if obj.id != newid:
                context.manage_renameObject(obj.id, newid)
            obj.reindexObject()
        return obj

    def newCollection(self, context, newid, title, tag=None):
        collection = self.createOrGetObject(context, newid, title, u'Collection')
        if tag is not None:
            query = [{u'i': u'Subject', u'o': u'plone.app.querystring.operation.selection.is', u'v': [tag, ]}]
            collection.query = query
            collection.reindexObject()
        return collection

    def newFolder(self, context, newid, title, type_name=u'Folder'):
        return self.createOrGetObject(context, newid, title, type_name)

    def getRandomImage(self, w, h, topic=''):
            data = requests.get('http://lorempixel.com/{0}/{1}/{2}'.format(w, h, topic)).content
            image = NamedBlobImage(data=data,
                                   filename=u'image.jpg',
                                   contentType=u'image/jpeg')
            return image

    def createRandomNews(self, context, count):
        print 'creating {0} News Items'.format(count)
        for i in range(count):
            obj = createContentInContainer(context, u'News Item', title=loremipsum.get_sentence(), image=self.getRandomImage(300, 200, u'sports'))
            obj.text = RichTextValue(loremipsum.get_sentence())
            obj.destacat = False            
            self.publish(obj)
            obj.reindexObject()

    def createRandomEvents(self, context, count):
        print 'creating {0} Events'.format(count)
        for i in range(count):
            obj = createContentInContainer(context, u'Event', title=loremipsum.get_sentence())
            obj.description = loremipsum.get_paragraph()
            self.publish(obj)
            obj.reindexObject()

    def createRandomBanners(self, context, count, w, h):
        print 'creating {0} Banners'.format(count)
        for i in range(count):
            obj = createContentInContainer(context, u'BannerEsports', title=loremipsum.get_sentence(), picture=self.getRandomImage(w, h, u'sports'))
            obj.description = loremipsum.get_paragraph()
            obj.url = u'http://www.upc.edu'
            self.publish(obj)
            obj.reindexObject()

    def createRandomDestacats(self, context, count, w, h, subject=[]):
        print 'creating {0} Destacats'.format(count)
        for i in range(count):
            try:
                title = loremipsum.get_sentence()
                title = re.findall('((?:\w+\s+){3})', title)[0]
            except:
                pass
            obj = createContentInContainer(context, u'Destacat', title=title, picture=self.getRandomImage(w, h, u'sports'))
            obj.text = RichTextValue(loremipsum.get_sentence())
            obj.url = u'http://www.upc.edu'
            tag0 = choice(['esports colectius', 'esports d''adversari', 'esports individuals', 'sales d''activitats', 'aules d''aprenentatge'])
            tag1 = choice(['futbol 11', 'futbol 7', 'futbol sala', 'basquet'])
            obj.subject = (tag0, tag1)
            self.publish(obj)
            obj.reindexObject()

    def publish(self, obj):
        workflow_tool = getToolByName(self.context, "portal_workflow")
        try:
            workflow_tool.doActionFor(obj, "publish")
        except:
            pass

    def render(self):
        """
        """
        portal = getSite()
        frontpage = portal['front-page']
        # Add portlets programatically
        # target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager2', context=frontpage)
        # target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        # from vilaix.theme.portlets.noticiaDestacada import Assignment as noticiaDestacadaAssignment        
        # target_manager_assignments['noticiaDestacada'] = noticiaDestacadaAssignment()
  

        # target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager3', context=frontpage)
        # target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        # target_manager_assignments['buttons'] = homebuttonbarAssignment()
        # target_manager_assignments['max'] = maxAssignment()

        portletManager = getUtility(IPortletManager, 'genweb.portlets.HomePortletManager3')
        spanstorage = getMultiAdapter((frontpage, portletManager), ISpanStorage)
        spanstorage.span = '8'

        portletManager = getUtility(IPortletManager, 'genweb.portlets.HomePortletManager6')
        spanstorage = getMultiAdapter((frontpage, portletManager), ISpanStorage)
        spanstorage.span = '4'

        portletManager = getUtility(IPortletManager, 'genweb.portlets.HomePortletManager7')
        spanstorage = getMultiAdapter((frontpage, portletManager), ISpanStorage)
        spanstorage.span = '8'

        portletManager = getUtility(IPortletManager, 'genweb.portlets.HomePortletManager10')
        spanstorage = getMultiAdapter((frontpage, portletManager), ISpanStorage)
        spanstorage.span = '4'


        portal_url = getToolByName(self.context, "portal_url")
        portal = portal_url.getPortalObject()

        # Delete old AT folders
        # if getattr(portal, 'events', None):
        #     if portal.events.__class__.__name__ == 'Folder':
        #         portal.manage_delObjects(['events'])

        # if getattr(portal, 'news', None):
        #     if portal.news.__class__.__name__ == 'Folder':
        #         portal.manage_delObjects(['news'])

        if getattr(portal, 'Members', None):
            if portal.Members.__class__.__name__ == 'Folder':
                portal.manage_delObjects(['Members'])

        # if getattr(portal, 'front-page', None):
        #     if portal['front-page'].__class__.__name__ == 'ATDocument':
        #         portal.manage_delObjects(['front-page'])

        # dummypage = self.createOrGetObject(portal, 'portletshome', 'Portlets placeholder', 'Document')
        # dummypage.setLanguage('ca')
        # dummypage.exclude_from_nav = True
        # self.publish(dummypage)
        #         # Mark the home page
        # if getattr(portal, 'portletshome', False):
        #     alsoProvides(dummypage, IHomePage)
        #     dummypage.reindexObject()

        # noticies = self.newFolder(portal, 'noticies', 'Noticies')
        # noticies.exclude_from_nav = True
        # self.publish(noticies)

        # esdeveniments = self.newFolder(portal, 'agenda', 'Agenda')
        # esdeveniments.exclude_from_nav = True
        # self.publish(esdeveniments)

        # gestio = self.newFolder(portal, 'gestio', u'Gestió')
        # gestio.exclude_from_nav = True

        # homepage = self.newFolder(gestio, 'homepage', u'Gestió elements pàgina principal')
        # accessos = self.newFolder(homepage, 'accessos-rapids', u'Accessos ràpids')
        # publicitat = self.newFolder(homepage, 'publicitat', u'Publicitat')
        # capcalera = self.newFolder(homepage, 'capcalera', u'Imatges capçalera')
        # destacats = self.newFolder(gestio, 'destacats', u'Destacats')

        # social = self.newFolder(homepage, 'xarxes-socials', u'Xarxes socials')
        # descripcio = self.createOrGetObject(homepage, 'descripcio', u'Text peu pàgina principal', type_name='Document')
        # self.publish(descripcio)

        # g_instalacions = self.newFolder(gestio, 'instalacions', u'Instal·lacions', type_name='SyncFolder')
        # g_activitats = self.newFolder(gestio, 'activitats', u'Activitats', type_name='SyncFolder')
        # g_competicions = self.newFolder(gestio, 'competicions', u'Competicions', type_name='SyncFolder')

        # self.publish(g_instalacions)
        # self.publish(g_activitats)
        # self.publish(g_competicions)

        # g_instalacions.url = 'http://puntabarrina.upc.edu/deportes/datos/pregen/xml/instalaciones.xml'
        # g_instalacions.importer = 'upc.serveiesports.content.browser.import.InstalacioImporter'
        # g_instalacions.description = u'Instal·lacions provinents de OMESA'

        # g_activitats.url = 'http://puntabarrina.upc.edu/deportes/datos/pregen/xml/cursos.xml'
        # g_activitats.importer = 'upc.serveiesports.content.browser.import.ActivitatImporter'
        # g_activitats.description = u'Activitats provinents de OMESA'

        # g_competicions.url = 'http://puntabarrina.upc.edu/deportes/datos/pregen/xml/competiciones.xml'
        # g_competicions.importer = 'upc.serveiesports.content.browser.import.CompeticioImporter'
        # g_competicions.description = u'Competicions provinents de OMESA'

        # # ACTIVITATS DIRIGIDES menu and submenus
        # activitats = self.newCollection(portal, 'activitats-dirigides', u'ACTIVITATS DIRIGIDES')
        # self.publish(activitats)

        # # COMPETICIO menu and submenus
        # competicio = self.newCollection(portal, 'competicio', u'COMPETICIÓ')
        # self.publish(competicio)

        # # ACTIVITAT FÍSICA menu and submenus
        # activitat_fisica = self.newCollection(portal, 'activitat-fisica', u'ACTIVITAT FÍSICA')
        # self.publish(activitat_fisica)

        # # COMUNITAT I SERVEIS menu and submenus
        # comunitat = self.newCollection(portal, 'comunitat-i-serveis', u'COMUNITAT I SERVEIS')
        # self.publish(comunitat)

        # # INSTALACIONS menu and submenus
        # instalacions = self.newCollection(portal, 'instalacions', u'INSTAL·LACIONS')
        # self.publish(instalacions)
        # ecol = self.newCollection(instalacions, 'esports-colectius', u'ESPORTS COLECTIUS', u'esports colectius')
        # ecol.description = loremipsum.get_paragraph()
        # ecol.image = self.getRandomImage(300, 200, u'sports')
        # ecol.reindexObject()

        # self.newCollection(instalacions, 'esports-adversaris', u'ESPORTS D''ADVERSARI', u'esports d''adversari')
        # self.newCollection(instalacions, 'esports-individuals', u'ESPORTS INDIVIDUALS', u'esports individuals')
        # self.newCollection(instalacions, 'sales-activitats', u'SALES D''ACTIVITATS', u'sales d''activitats')
        # self.newCollection(instalacions, 'aules-aprenentatge', u'AULES D''APRENENTATGE', u'aules d''aprenentatge')

        # # CAMPUS menu and submenus
        # campus = self.newCollection(portal, 'campus', u'CAMPUS')
        # self.publish(campus)

       
        # # Create DUMMY CONTENT on request
        # if self.request.get('dummy', False):          
        #self.createRandomNews(portal['news'], 5)
        # self.createRandomEvents(portal['events'], 5)
        #     self.createRandomBanners(portal['gestio']['homepage']['accessos-rapids'], 4, w=190, h=40)
        #     self.createRandomBanners(portal['gestio']['homepage']['publicitat'], 4, w=150, h=150)
        #     self.createRandomBanners(portal['gestio']['homepage']['capcalera'], 4, w=978, h=300)
        #     self.createRandomDestacats(portal['gestio']['destacats'], 30, w=330, h=200)

        # #Create homepage portlet assignments

        # assignment = setPortletAssignment(1, dummypage, 'accessos', QueryPortletAssignment)
        # query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'BannerEsports']},
        #          {u'i': u'path', u'o': u'plone.app.querystring.operation.string.path', u'v': u'/gestio/homepage/accessos-rapids'}]
        # setupQueryPortlet(assignment, u'Accessos ràpids', query, 4, False, u"")

        # assignment = setPortletAssignment(1, dummypage, 'publicitat', QueryPortletAssignment)
        # query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'BannerEsports']},
        #          {u'i': u'path', u'o': u'plone.app.querystring.operation.string.path', u'v': u'/gestio/homepage/publicitat'}]
        # setupQueryPortlet(assignment, u'Publicitat', query, 2, False, u"")

        # assignment = setPortletAssignment(2, dummypage, 'destacats', QueryPortletAssignment, span=12)
        # query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'Destacat']},
        #          {u'i': u'path', u'o': u'plone.app.querystring.operation.string.path', u'v': u'/gestio/destacats'}]
        # setupQueryPortlet(assignment, u'Destacats', query, 4, False, u"")

        # assignment = setPortletAssignment(5, dummypage, 'noticies', QueryPortletAssignment, span=6)
        # query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'News Item']},
        #          {u'i': u'path', u'o': u'plone.app.querystring.operation.string.path', u'v': u'/noticies'}]
        # setupQueryPortlet(assignment, u'Notícies', query, 5, False, u"")

        # assignment = setPortletAssignment(6, dummypage, 'agenda', QueryPortletAssignment, span=6)
        # query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'Event']},
        #          {u'i': u'path', u'o': u'plone.app.querystring.operation.string.path', u'v': u'/agenda'}]
        # setupQueryPortlet(assignment, u'Agenda', query, 5, False, u"")

        return 'Created'
