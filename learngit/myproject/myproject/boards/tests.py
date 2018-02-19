from django.test import TestCase
from django.urls import reverse#Django 2.0 remove django.core.urlresolvers
from django.urls import resolve
from .views import home,board_topics
from  .models import Board


class HomeTest(TestCase):

    def setUp(self):
        self.board=Board.objects.create(name='Django',description='Django board')
        url=reverse('home')
        self.response = self.client.get(url)
        # print(self.response)

    def test_home_view_code(self):  #查看主页的状态码 断言是否是200
        # url=reverse('home')
        # response=self.client.get(url)
        self.assertEqual(self.response.status_code,200)

    def test_home_url_resolve_home_view(self):
        '''
        Django uses it to match a
        requested URL with a list
        of URLs listed in the urls.py
        module
        '''
        view=resolve('/')
        self.assertEqual(view.func,home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url=reverse('board_topics',kwargs={'pk':self.board.pk})
        self.assertContains(self.response,'href="{0}"'.format(board_topics_url))  #response body has the text href="/boards/1/"


class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        # print(url)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics',kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        homepage_url=reverse('home')
        # print(homepage_url)
        self.assertContains(response,'href="{0}"'.format(homepage_url))

