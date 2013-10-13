.. contents::

.. image:: https://travis-ci.org/rebeccaframework/rebecca.menu.png?branch=master
   :target: https://travis-ci.org/rebeccaframework/rebecca.menu

Introduction
============

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


To add menu, use ``add_route_menu`` directive.::

    config.add_route('menu1', '/menus/menu1')
    config.add_route('menu2', '/menus/menu2')
    config.add_route_menu(menu_name="system", route_name="menu1", display_name="system menu item1")
    config.add_route_menu(menu_name="system", route_name="menu2", display_name="system menu item2")

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
