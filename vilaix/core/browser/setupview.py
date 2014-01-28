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
import pkg_resources

from zope.interface import alsoProvides 
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs
from Products.CMFPlone.utils import _createObjectByType

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_DXCT = False
else:
    HAS_DXCT = True
    from plone.dexterity.utils import createContentInContainer


# from serveiesports.theme.portlets.queryportlet import Assignment as QueryPortletAssignment
# from serveiesports.theme.portlets.utils import setupQueryPortlet, setPortletAssignment

class setupHomePage(grok.View):
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')
    grok.name("setup-portlets")

    def render(self):
        portal = getSite()
        frontpage = portal['front-page']

         # Add portlets programatically
        from vilaix.theme.portlets.noticiaDestacada import Assignment as noticiaDestacadaAssignment 
        from vilaix.theme.portlets.news import Assignment as noticiaAssignment 
        from vilaix.theme.portlets.bannersportlet import Assignment as bannersVilaixAssignment
        from vilaix.theme.portlets.agendaVilaix import Assignment as agendaVilaixAssignment
        from vilaix.theme.portlets.navigationfixed import Assignment as navigationfixedAssignment
        from plone.app.event.portlets.portlet_calendar import Assignment as calendarAssignment
        

        target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager1', context=frontpage)
        target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        target_manager_assignments['navigationfixed'] = navigationfixedAssignment(root='/menu-lateral')
        target_manager_assignments['bannersVilaix'] = bannersVilaixAssignment(content='/material-multimedia/banners/banners_esquerra')     
  

        target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager2', context=frontpage)
        target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        target_manager_assignments['noticiaDestacada'] = noticiaDestacadaAssignment()        
  

        target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager3', context=frontpage)
        target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        target_manager_assignments['noticies'] = noticiaAssignment()
        
        target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager6', context=frontpage)
        target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        target_manager_assignments['bannersVilaix'] = bannersVilaixAssignment(content='/material-multimedia/banners/banners_dreta')
        
        target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager7', context=frontpage)
        target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        target_manager_assignments['agendaVilaix'] = agendaVilaixAssignment() 

        target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager10', context=frontpage)
        target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        target_manager_assignments['calendari'] = calendarAssignment(state='published')

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

        return 'Done.'

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

    def newCollection(self, context, newid, title, query=None):
        collection = self.createOrGetObject(context, newid, title, u'Collection')
        if query is not None:            
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

        urltool = getToolByName(portal, 'portal_url')        
        portal_catalog = getToolByName(portal, 'portal_catalog')
        path = urltool.getPortalPath() 
        workflowTool = getToolByName(portal, "portal_workflow")
        pl = getToolByName(portal, 'portal_languages')

        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                            path = path + '/noticies')
        if obj.actual_result_count == 0:
            noticies = self.newFolder(portal, 'noticies', 'Noticies')
            noticies.description = 'Noticies del lloc'
            noticies.exclude_from_nav = True
            self.publish(noticies)

            noticies_destacades = self.newCollection(noticies, 'noticies-destacades', u'Noticies Destacades', query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'News Item']},
                                                                                                                       {u'i': u'review_state', u'o': u'plone.app.querystring.operation.selection.is', u'v': u'published'},
                                                                                                                       {u'i': u'destacat', u'o': u'plone.app.querystring.operation.boolean.isTrue', u'v': u'Sí'}])
            self.publish(noticies_destacades)

            noticies = self.newCollection(noticies, 'noticies', u'Noticies', query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'News Item']},
                                                                                      {u'i': u'review_state', u'o': u'plone.app.querystring.operation.selection.is', u'v': u'published'}])
            self.publish(noticies)

        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                            path = path + '/esdeveniments')
        if obj.actual_result_count == 0:
            esdeveniments = self.newFolder(portal, 'esdeveniments', 'Esdeveniments')
            esdeveniments.description = 'Esdeveniments del lloc'
            esdeveniments.exclude_from_nav = True
            self.publish(esdeveniments)

            esdeveniments = self.newCollection(esdeveniments, 'esdeveniments', u'Esdeveniments', query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'Event']},
                                                                                                          {u'i': u'review_state', u'o': u'plone.app.querystring.operation.selection.is', u'v': u'published'}])
            
            self.publish(esdeveniments)          
                     
        #Menú principal
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                            path = path + '/menu-principal')
        if obj.actual_result_count == 0:      
            menu_principal = self.newFolder(portal, 'menu-principal', u'Menú principal')
            menu_principal.language = pl.getDefaultLanguage()
            menu_principal.exclude_from_nav = True
            self.publish(menu_principal)
            alsoProvides(menu_principal, IHideFromBreadcrumbs)
            menu_principal.reindexObject()

            ajuntament = self.newFolder(menu_principal, 'ajuntament', u'Ajuntament')
            ajuntament.language = pl.getDefaultLanguage()       
            self.publish(ajuntament)
            ajuntament.reindexObject()   
            
            informacio_municipal = self.newFolder(menu_principal, 'informacio-municipal', u'Informació Municipal')
            informacio_municipal.language = pl.getDefaultLanguage()       
            self.publish(informacio_municipal)
            informacio_municipal.reindexObject()     

            seu_electronica = self.newFolder(menu_principal, 'seu-electronica', u'Seu electrònica')
            seu_electronica.language = pl.getDefaultLanguage()       
            self.publish(seu_electronica) 
            seu_electronica.reindexObject()    
            
            guia_de_la_ciutat = self.newFolder(menu_principal, 'guia-de-la-ciutat', u'Guia de la ciutat')
            guia_de_la_ciutat.language = pl.getDefaultLanguage()       
            self.publish(guia_de_la_ciutat)
            guia_de_la_ciutat.reindexObject()    
        
            
            borsa_de_treball = self.newFolder(menu_principal, 'borsa-de-treball', u'Borsa de treball')
            borsa_de_treball.language = pl.getDefaultLanguage()       
            self.publish(borsa_de_treball)
            borsa_de_treball.reindexObject()    


        #Menú Lateral       
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                            path = path + '/menu-lateral')
        if obj.actual_result_count == 0:
            menu_lateral = self.newFolder(portal, 'menu-lateral', u'Menú lateral')
            menu_lateral.language = pl.getDefaultLanguage()
            menu_lateral.exclude_from_nav = True
            self.publish(menu_lateral)
            alsoProvides(menu_lateral, IHideFromBreadcrumbs)
            menu_lateral.reindexObject()

            la_ciutat_per_temes = self.newFolder(menu_lateral, 'la-ciutat-per-temes', u'La ciutat per temes')
            la_ciutat_per_temes.language = pl.getDefaultLanguage()       
            self.publish(la_ciutat_per_temes)
            la_ciutat_per_temes.reindexObject() 
            
            la_ciutat_per_les_persones = self.newFolder(menu_lateral, 'la-ciutat-per-les-persones', u'La ciutat i les persones')
            la_ciutat_per_les_persones.language = pl.getDefaultLanguage()       
            self.publish(la_ciutat_per_les_persones)
            la_ciutat_per_les_persones.reindexObject()  

            la_ciutat_en_xifres = self.newFolder(menu_lateral, 'la-ciutat-en-xifres', u'La ciutat en xifres')
            la_ciutat_en_xifres.language = pl.getDefaultLanguage()       
            self.publish(la_ciutat_en_xifres)
            la_ciutat_en_xifres.reindexObject()

            la_ciutat_per_districtes = self.newFolder(menu_lateral, 'la-ciutat-per-districtes', u'La ciutat per districtes')
            la_ciutat_per_districtes.language = pl.getDefaultLanguage()       
            self.publish(la_ciutat_per_districtes)
            la_ciutat_per_districtes.reindexObject()

        
        #Material multimèdia
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                            path = path + '/material-multimedia')
        if obj.actual_result_count == 0:
            material_multimedia = self.newFolder(portal, 'material-multimedia', u'Material multimèdia')
            material_multimedia.language = pl.getDefaultLanguage()
            material_multimedia.exclude_from_nav = True
            self.publish(material_multimedia)       
            material_multimedia.reindexObject()
   
        #Slider
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                            path = path + '/material-multimedia/sliders')
        if obj.actual_result_count == 0:            
            res = portal_catalog.searchResults(id = 'material-multimedia')
            if res:
                material_multimedia = res[0].getObject()
            slider = self.newFolder(material_multimedia, 'sliders', u'Sliders')
            slider.language = pl.getDefaultLanguage()
            slider.exclude_from_nav = True
            self.publish(slider)       
            slider.reindexObject()

        #Banners
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                            path = path + '/material-multimedia/banners')
        if obj.actual_result_count == 0:     
            res = portal_catalog.searchResults(id = 'material-multimedia')
            if res:
                material_multimedia = res[0].getObject()     
            banners = self.newFolder(material_multimedia, 'banners', u'Banners')
            banners.language = pl.getDefaultLanguage()
            banners.exclude_from_nav = True
            self.publish(banners)       
            banners.reindexObject()
      
        #Carrousel
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                            path = path + '/material-multimedia/carroussel')
        if obj.actual_result_count == 0:  
            res = portal_catalog.searchResults(id = 'material-multimedia')
            if res:
                material_multimedia = res[0].getObject()         
            carroussel = self.newFolder(material_multimedia, 'carroussel', u'Carroussel')
            carroussel.language = pl.getDefaultLanguage()
            carroussel.exclude_from_nav = True
            self.publish(carroussel)       
            carroussel.reindexObject()

        #Imatges Capçalera
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                            path = path + '/material-multimedia/imatges-capcalera')
        if obj.actual_result_count == 0: 
            res = portal_catalog.searchResults(id = 'material-multimedia')
            if res:
                material_multimedia = res[0].getObject()          
            imatges_capcalera = self.newFolder(material_multimedia, 'imatges-capcalera', u'Imatges capçalera')
            imatges_capcalera.language = pl.getDefaultLanguage()
            imatges_capcalera.exclude_from_nav = True
            self.publish(imatges_capcalera)       
            imatges_capcalera.reindexObject()    

        #Banners dreta
        obj = portal_catalog.searchResults(portal_type = 'BannerContainer',
                                                path = path + '/material-multimedia/banners/banners_dreta')
        if obj.actual_result_count == 0:
            _createObjectByType('BannerContainer', banners, 'banners_dreta')  
            banners['banners_dreta'].setExcludeFromNav(True)
            banners['banners_dreta'].setTitle('Banners-dreta')
            banners['banners_dreta'].reindexObject()
            workflowTool.doActionFor(banners.banners_dreta, "publish")  


        #Banners esquerra
        obj = portal_catalog.searchResults(portal_type = 'BannerContainer',
                                                path = path + '/material-multimedia/banners/banners_esquerra')
        if obj.actual_result_count == 0:
            _createObjectByType('BannerContainer', banners, 'banners_esquerra')  
            banners['banners_esquerra'].setExcludeFromNav(True)
            banners['banners_esquerra'].setTitle('Banners-esquerra')
            banners['banners_esquerra'].reindexObject()
            workflowTool.doActionFor(banners.banners_esquerra, "publish")          
                
       
        #Documents
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                           path = path + '/documents')
        if obj.actual_result_count == 0:                                
            documents = self.newFolder(portal, 'documents', u'Documents')
            documents.language = pl.getDefaultLanguage()
            documents.exclude_from_nav = True
            self.publish(documents)       
            documents.reindexObject()    

        #Directori equipaments
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                           path = path + '/directori-equipaments')
        if obj.actual_result_count == 0:    
            directori_equipaments = self.newFolder(portal, 'directori-equipaments', u'Directori equipaments')
            directori_equipaments.language = pl.getDefaultLanguage()
            directori_equipaments.exclude_from_nav = True
            self.publish(directori_equipaments)       
            directori_equipaments.reindexObject()    

    
        #Tràmits
        obj = portal_catalog.searchResults(portal_type = 'Folder',
                                           path = path + '/tramits')
        if obj.actual_result_count == 0:    
            tramits = self.newFolder(portal, 'tramits', u'Tràmits')
            tramits.language = pl.getDefaultLanguage()
            tramits.exclude_from_nav = True
            self.publish(tramits)       
            tramits.reindexObject()    


        # # Add portlets programatically
        # from vilaix.theme.portlets.noticiaDestacada import Assignment as noticiaDestacadaAssignment 
        # from vilaix.theme.portlets.news import Assignment as noticiaAssignment 
        # from vilaix.theme.portlets.bannersportlet import Assignment as bannersVilaixAssignment
        # from vilaix.theme.portlets.agendaVilaix import Assignment as agendaVilaixAssignment
        # from vilaix.theme.portlets.navigationfixed import Assignment as navigationfixedAssignment
        # from plone.app.event.portlets.portlet_calendar import Assignment as calendarAssignment
        

        # target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager1', context=frontpage)
        # target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        # target_manager_assignments['navigationfixed'] = navigationfixedAssignment(root='/menu-lateral')
        # target_manager_assignments['bannersVilaix'] = bannersVilaixAssignment(content='/material-multimedia/banners/banners_esquerra')     
  

        # target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager2', context=frontpage)
        # target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        # target_manager_assignments['noticiaDestacada'] = noticiaDestacadaAssignment()        
  

        # target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager3', context=frontpage)
        # target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        # target_manager_assignments['noticies'] = noticiaAssignment()
        
        # target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager6', context=frontpage)
        # target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        # target_manager_assignments['bannersVilaix'] = bannersVilaixAssignment(content='/material-multimedia/banners/banners_dreta')
        
        # target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager7', context=frontpage)
        # target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        # target_manager_assignments['agendaVilaix'] = agendaVilaixAssignment() 

        # target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager10', context=frontpage)
        # target_manager_assignments = getMultiAdapter((frontpage, target_manager), IPortletAssignmentMapping)
        # target_manager_assignments['calendari'] = calendarAssignment(state='published')

        # portletManager = getUtility(IPortletManager, 'genweb.portlets.HomePortletManager3')
        # spanstorage = getMultiAdapter((frontpage, portletManager), ISpanStorage)
        # spanstorage.span = '8'

        # portletManager = getUtility(IPortletManager, 'genweb.portlets.HomePortletManager6')
        # spanstorage = getMultiAdapter((frontpage, portletManager), ISpanStorage)
        # spanstorage.span = '4'

        # portletManager = getUtility(IPortletManager, 'genweb.portlets.HomePortletManager7')
        # spanstorage = getMultiAdapter((frontpage, portletManager), ISpanStorage)
        # spanstorage.span = '8'

        # portletManager = getUtility(IPortletManager, 'genweb.portlets.HomePortletManager10')
        # spanstorage = getMultiAdapter((frontpage, portletManager), ISpanStorage)
        # spanstorage.span = '4'    
        
                   
        return 'Created'
