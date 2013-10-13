import pytest
import webtest


@pytest.fixture
def app():
    from pyramid.config import Configurator
    from pyramid.authentication import AuthTktAuthenticationPolicy
    from pyramid.authorization import ACLAuthorizationPolicy
    from pyramid.security import Allow, remember, authenticated_userid
    def index(request):
        from rebecca.menu import get_menu
        menu = get_menu(request, 'system')
        return {"system_menu": [
            (m.display_name, m.url)
            for m in menu.menu_items
        ]}

    def login(request):
        if request.method == 'POST':
            username = request.params['username']
            headers = remember(request, username)
            request.response.headerlist.extend(headers)
        return {'username': authenticated_userid(request)}

    class RootResource(object):
        def __init__(self, request):
            self.request = request

        __acl__ = [
            (Allow, 'testing-user', 'testing-permission'),
        ]

    config = Configurator(root_factory=RootResource)
    config.set_authentication_policy(AuthTktAuthenticationPolicy("secret"))
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.include("rebecca.menu")
    config.add_route('top', '/')
    config.add_route('login', '/login')
    config.add_route('menu1', '/menus/menu1')
    config.add_route('menu2', '/menus/menu2')
    config.add_route('menu3', '/menus/menu3')
    config.add_route('menu4', '/menus/menu4')
    config.add_route_menu(menu_name="system", route_name="menu1", display_name="system menu item1")
    config.add_route_menu(menu_name="system", route_name="menu2", display_name="system menu item2")
    config.add_route_menu(menu_name="system", route_name="menu3", display_name="system menu item3", permission="testing-permission")
    config.add_route_menu(menu_name="system", route_name="menu4", display_name="system menu item4", permission="dummy-permission")
    config.add_view(index, route_name="top", renderer="json")
    config.add_view(login, route_name="login", renderer="json")
    app = config.make_wsgi_app()
    return webtest.TestApp(app)


def test_no_permission(app):
    res = app.get('/')

    assert res.json == {'system_menu': [['system menu item1', 'http://localhost/menus/menu1'],
                                        ['system menu item2', 'http://localhost/menus/menu2']]}

def test_with_permission(app):
    res = app.post('/login', params={'username': 'testing-user'})
    res = app.get('/login')
    assert res.json == {'username': 'testing-user'}

    res = app.get('/')

    assert res.json == {'system_menu': [['system menu item1', 'http://localhost/menus/menu1'],
                                        ['system menu item2', 'http://localhost/menus/menu2'],
                                        ['system menu item3', 'http://localhost/menus/menu3'],
                                        ]}
