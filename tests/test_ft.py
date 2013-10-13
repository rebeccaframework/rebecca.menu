import pytest
import webtest


@pytest.fixture
def app():
    from pyramid.config import Configurator
    def index(request):
        from rebecca.menu import get_menu
        menu = get_menu(request, 'system')
        return {"system_menu": [
            (m.display_name, m.url)
            for m in menu.menu_items
        ]}

    config = Configurator()
    config.include("rebecca.menu")
    config.add_route('top', '/')
    config.add_route('menu1', '/menus/menu1')
    config.add_route('menu2', '/menus/menu2')
    config.add_route_menu(menu_name="system", route_name="menu1", display_name="system menu item1")
    config.add_route_menu(menu_name="system", route_name="menu2", display_name="system menu item2")
    config.add_view(index, route_name="top", renderer="json")
    app = config.make_wsgi_app()
    return webtest.TestApp(app)


def test_ft(app):
    res = app.get('/')

    assert res.json == {'system_menu': [['system menu item1', 'http://localhost/menus/menu1'],
                                        ['system menu item2', 'http://localhost/menus/menu2']]}
