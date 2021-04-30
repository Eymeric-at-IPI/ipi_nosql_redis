from django.http import HttpRequest
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from redischat.views import page_index


class TestUrlIndex(SimpleTestCase):

    def test_url_index_exist(self):
        """
        test_url_index_exist Fail if index route status_code != 200
        """
        url = reverse('index')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_url_index_is_resolved(self):
        """
        test_url_index_is_resolved Fail if index route doesn't match views.index
        """
        url = reverse('index')
        found = resolve(url)
        self.assertEquals(found.func, page_index)

    # TODO :
    # def test_view_uses_correct_template(self):
    #     response = self.client.get(reverse('index'))
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'page_index')

    # TODO :
    # def test_url_slug_is_resolved(self):
    #     """
    #     test_url_index_is_resolved() returns False if index route doesn't match views.index
    #     """
    #     url = reverse('index', args=['slug', 1])
    #     print(url)
    #     self.assertEquals(resolve(url).func, page_index)

    # TODO :
    # def test_home_page_returns_correct_html(self):
    #     request = HttpRequest()
    #     response = page_index(request)
    #     html = response.content.decode('utf8')
    #     self.assertTrue(html.startswith('<html>'))
    #     self.assertIn('<title>To-Do lists</title>', html)
    #     self.assertTrue(html.endswith('</html>'))

    # TODO :
    # inscription
    # connexion
    # profil
    # liste d'amie
    # detail ami
    # liste conversation
    # detail conversation



