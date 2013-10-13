.. contents::

.. image:: https://travis-ci.org/rebeccaframework/rebecca.menu.png?branch=master
   :target: https://travis-ci.org/rebeccaframework/rebecca.menu

Introduction
======================

``rebecca.menu`` is component for `pyramid <http://pypi.python.org/pypi/pyramid>`_, that provides management of menu urls.

Install
--------------------

You can install ``rebecca.menu`` with pip.

::

  $ pip install rebecca.menu


Usage
====================

``rebecca.menu`` provides include hook.::

    config.include('rebecca.menu')

register and use Menu
--------------------------------------------------------

To add menu, use ``add_route_menu`` directive.::

    config.add_route('menu1', '/menus/menu1')
    config.add_route('menu2', '/menus/menu2')
    config.add_route_menu(menu_name="system", route_name="menu1", display_name="system menu item1")

Or use ``route_menu_config`` decorator.::

    @route_menu_config('system')
    class SystemMenu3(object):
        route_name="menu3"
        display_name = "system menu item3"


To get menu, use ``get_menu`` API::

    from rebecca.menu import get_menu

    def menu(request):
        system_menu = get_menu(request, system)
        return dict(menu=system_menu)

``get_menu`` returns the object that provides ``rebecca.menu.interfaces.IMenu``.
``IMenu`` has a property named ``menu_items`` that is list including ``IMenuItem``.

``IMenuItem`` has some property, ``display_name``, ``name`` and ``url``.
Maybe you use menu items in template such as below::

    <ul class="nav">
    %for m in system_menu.menu_items:
        <li><a href="${m.url}">${m.display_name}</a></li>
    %endfor
    </ul>

Permissions
-----------------------------------

Registering menu with permission ::

    @route_menu_config('system')
    class SystemMenu3(object):
        route_name="menu3"
        display_name = "system menu item3"
        permission = 'menu3-permission'

``get_menu`` check permission of request with ``has_permission``,
causes that menu_items includes menu items passed permission check.

Matchdict
----------------------------------------

If route has placeholder, the menu url fills values from ``request.matchdict``.
::

        config.add_route("menu1", 'menus/menu1/{testing_vars}')
        menu_factory.add_item(route_name="menu1", display_name="testing-menu1")

When matchdict has values for ``testing_vars`` as "that-is-testing", menu1's url is "menus/menu1/that-is-testing".
