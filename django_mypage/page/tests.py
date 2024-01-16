from django.test import SimpleTestCase
# from django.urls import resolve
# from views import another_page, index
# import django_mypage.page.views


class AnotherPageTest(SimpleTestCase):

    def test_index_status_code(self):
        response = self.client.get('/index/anotherpage/')
        self.assertEqual(response.status_code, 200)

    def test_index_template(self):
        response = self.client.get('/index/anotherpage/')
        self.assertTemplateUsed(response, 'page/anotherpage.html')
    #
    # def test_home_page_url_resolves_homepage_view(self):
    #     view = resolve('/')
    #     self.assertEqual(view.func, homepage)