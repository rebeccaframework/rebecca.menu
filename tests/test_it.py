import pytest
from testfixtures import compare, Comparison as C
from pyramid import testing
# from rebecca.testing import config


@pytest.fixture
def config(request):
    config = testing.setUp()

    def fin():
        testing.tearDown()

    request.addfinalizer(fin)
    return config


class TestRouteMenuFactory(object):
    @pytest.fixture
    def target(self):
        from rebecca.menu import RouteMenuFactory
        return RouteMenuFactory

    def test_has_permission(self, config, target):
        from rebecca.menu import MenuItem
        config.add_route("menu1", 'menus/menu1')
        config.add_route("menu2", 'menus/menu2')

        config.testing_securitypolicy(userid="testing")

        menu_factory = target(name=testing)
        menu_factory.add_item(route_name="menu1", display_name="testing-menu1")
        menu_factory.add_item(
            route_name="menu2",
            display_name="testing-menu2",
            permission="testing-permission")
        request = testing.DummyRequest()
        result = menu_factory(request)

        compare(
            result.menu_items, [
                C(MenuItem,
                  strict=False,
                  url="http://example.com/menus/menu1",
                  display_name="testing-menu1"),
                C(MenuItem,
                  strict=False,
                  url="http://example.com/menus/menu2",
                  display_name="testing-menu2")
            ])

    def test_without_permission(self, config, target):
        from rebecca.menu import MenuItem
        config.add_route("menu1", 'menus/menu1')
        config.add_route("menu2", 'menus/menu2/')

        config.testing_securitypolicy(userid="testing", permissive=False)

        menu_factory = target(name=testing)
        menu_factory.add_item(route_name="menu1", display_name="testing-menu1")
        menu_factory.add_item(
            route_name="menu2",
            display_name="testing-menu2",
            permission="testing-permission")
        request = testing.DummyRequest()
        result = menu_factory(request)

        compare(
            result.menu_items, [
                C(MenuItem,
                  strict=False,
                  url="http://example.com/menus/menu1",
                  display_name="testing-menu1")
            ])

    def test_matchdict(self, config, target):
        from rebecca.menu import MenuItem
        config.add_route("menu1", 'menus/menu1/{testing_vars}')

        config.testing_securitypolicy(userid="testing", permissive=False)

        menu_factory = target(name=testing)
        menu_factory.add_item(route_name="menu1", display_name="testing-menu1")
        request = testing.DummyRequest(
            matchdict={"testing_vars": "that-is-testing"})
        result = menu_factory(request)

        compare(
            result.menu_items, [
                C(MenuItem,
                  strict=False,
                  url="http://example.com/menus/menu1/that-is-testing",
                  display_name="testing-menu1")
            ])
