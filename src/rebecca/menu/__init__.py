import logging
import venusian
from zope.interface import implementer
from pyramid.security import has_permission
from .interfaces import IMenu, IMenuItem, IMenuFactory

logger = logging.getLogger(__name__)

def includeme(config):
    config.add_directive('add_route_menu', add_route_menu)


def route_menu_config(menu_name):
    def dec(obj):
        def callback(scanner, name, obj):
            add_route_menu(scanner.config, menu_name=menu_name,
                           route_name=obj.route_name,
                           display_name=obj.display_name,
                           permission=(obj.permission
                               if hasattr(obj, 'permission') else None))
        venusian.attach(obj, callback=callback)
        return obj
    return dec

def add_route_menu(config,
                   menu_name,
                   route_name,
                   display_name,
                   permission=None):
    reg = config.registry

    def register():
        factory = reg.queryUtility(IMenuFactory, name=menu_name)
        if factory is None:
            factory = RouteMenuFactory(name=menu_name)
            logger.debug("create menu factory {0}".format(factory))
            reg.registerUtility(factory, IMenuFactory, name=menu_name)
        factory.add_item(route_name, display_name, permission)
        logger.debug("menu item {0}".format(intr))

    discriminator = "rebecca.menu:" + menu_name + ":" + route_name
    intr = config.introspectable(title="Rebecca Menu",
                                 category_name="rebecca.menu",
                                 discriminator=discriminator,
                                 type_name=None)
    intr['menu_name'] = menu_name
    intr['route_name'] = route_name
    intr['display_name'] = display_name
    intr['permission'] = permission
    config.action(discriminator=discriminator,
                  callable=register,
                  introspectables=(intr,))

def get_menu(request, menu_name=""):
    logger.debug("get menu")
    reg = request.registry
    factory = reg.queryUtility(IMenuFactory, name=menu_name)
    if factory is None:
        return None
    assert factory.items
    logger.debug(factory.items)
    return factory(request)

@implementer(IMenuFactory)
class RouteMenuFactory(object):
    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, route_name, display_name, permission=None):
        self.items.append((route_name, display_name, permission))

    def __call__(self, request):

        return Menu(name=self.name,
                    menu_items=[
                        MenuItem(name=route_name,
                                 url=request.route_url(route_name,
                                                       **request.matchdict),
                                 display_name=display_name)
                        for route_name, display_name, permission
                        in self.items
                        if (permission is None
                            or has_permission(permission,
                                              request.context, request))])


@implementer(IMenuItem)
class MenuItem(object):
    def __init__(self, name, url, display_name):
        self.name = name
        self.url = url
        self.display_name = display_name


@implementer(IMenu)
class Menu(object):
    def __init__(self, name, menu_items):
        self.name = name
        self.menu_items = menu_items
