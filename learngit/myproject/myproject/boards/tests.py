from django.test import TestCase
from django.urls import reverse#Django 2.0 remove django.core.urlresolvers
from django.urls import resolve
from .views import home,board_topics,new_topic
from  .models import Board ,Post ,Topic
from django.contrib.auth.models import User
from .forms import NewTopicForm

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

    # def test_board_topics_view_contains_link_back_to_homepage(self):
    #     board_topics_url = reverse('board_topics',kwargs={'pk': 1})
    #     response = self.client.get(board_topics_url)
    #     homepage_url=reverse('home')
    #     # print(homepage_url)
    #     self.assertContains(response,'href="{0}"'.format(homepage_url))

    def test_board_topics_view_contains_navigation_links(self):  #replace above one
        board_topics_url=reverse('board_topics',kwargs={'pk':1})
        homepage_url=reverse('home')#board list
        new_topic_url=reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        User.objects.create_user(username='john', email="jonh@deo.com" ,password='123')

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic',kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic',kwargs={'pk': 99})
        response= self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view=resolve('/boards/1/new/')   #从url方法中获取url_name
        self.assertEquals(view.func, new_topic) #判断方法是否相等

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url=reverse('new_topic',kwargs={'pk':1})
        board_topics_url=reverse('board_topics',kwargs={'pk':1})
        response=self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_csrf(self):  #检查防御
        url = reverse('new_topic',kwargs={'pk':1})
        response=self.client.get(url)
        self.assertContains(response,'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self): #检查postdata
        url = reverse('new_topic',kwargs={'pk':1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url,data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data_empty_fields(self):
        url = reverse('new_topic', kwargs={'pk':1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url,data)
        self.assertEquals(response.status_code,200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        url=reverse('new_topic', kwargs={'pk': 1})
        response=self.client.get(url)
        form=response.context.get('form')
        self.assertIsInstance(form,NewTopicForm)

    def test_new_topic_invalid_post_data(self):
        url=reverse('new_topic', kwargs={'pk': 1})
        response=self.client.post(url,{})
        form=response.context.get('form')
        self.assertEquals(response.status_code,200)
        self.assertTrue(form.errors)