# -*- coding:utf-8 -*-
from zope.interface import Interface, Attribute


class IMenuFactory(Interface):
    name = Attribute(u"")

    def __call__(request):
        """ create menu
        """

class IMenu(Interface):
    name = Attribute(u"")
    menu_items = Attribute(u"")


class IMenuItem(Interface):
    name = Attribute(u"")
    display_name = Attribute(u"")
    url = Attribute(u"")
