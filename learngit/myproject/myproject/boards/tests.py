from django.test import TestCase
from django.urls import reverse#Django 2.0 remove django.core.urlresolvers
from django.urls import resolve
from .views import home


class HomeTest(TestCase):
    def test_home_view_code(self):  #查看主页的状态码 断言是否是200
        url=reverse('home')
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_home_url_resolve_home_view(self):
        '''
        Django uses it to match a
        requested URL with a list
        of URLs listed in the urls.py
        module
        '''
        view=resolve('/')
        self.assertEqual(view.func,home)