from django.test import TestCase, Client
from django.urls import reverse
from classroom.models import Notice
from django.contrib.auth.models import User, Group, Permission
import json
from django.core.exceptions import ObjectDoesNotExist

class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Adding group named Student because when user is created it's default group is Student
        Group.objects.create(name="Student")
        cls.client = Client()

        # Users
        cls.user_with_permission = cls.create_user('testuser1', 'testpass1', permission='add_notice')
        cls.user_no_permission = cls.create_user('testuser2', 'testpass2')
        
        # Test Notice
        cls.notice = Notice.objects.create(
            title='Test Notice', 
            content='This is a test notice',
            author=cls.user_with_permission
        )

        # Urls
        cls.list_url = reverse('notice_list')
        cls.create_url = reverse('notice_create')
        cls.delete_url = reverse('notice_delete', kwargs={'pk':1})

    @classmethod
    def create_user(cls, username, password, permission=None):
        user = User.objects.create_user(username=username, password=password)
        if permission:
            perm = Permission.objects.get(codename=permission)
            user.user_permissions.add(perm)
        return user


    def test_notice_list_authenticated(self):

        self.client.login(username='testuser2', password='testpass2')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom/notice_list.html')         # for render
        self.assertContains(response, text='Test Notice')
        # text = The string you expect in the response content


    def test_notice_list_unauthenticated(self):
        response = self.client.get(self.list_url)
        # print('For unauthenticated User:',response)
        self.assertEqual(response.status_code, 302)        # for redirect
        self.assertTrue(response.url.startswith('/accounts/login/'))

    
    def test_notice_create_without_permission(self):
        self.client.login(username='testuser2', password='testpass2')
        response = self.client.get(self.create_url)
        # print(response)
        self.assertEqual(response.status_code, 403)

    
    def test_notice_create_with_permission(self):
        self.client.login(username='testuser1', password='testpass1')
        data = {
            'title': 'New notice', 
            'content': 'This is a new notice'
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notice_list'))
        self.assertTrue(Notice.objects.filter(title='New notice').exists())


    def test_notice_create_unauthenticated(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 403)
        # self.assertTrue(response.url.startswith('/accounts/login/'))

    
    def test_notice_delete_without_permission(self):
        self.client.login(username='testuser2', password='testpass2')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 403)
        
    
    def test_notice_delete_with_permission(self):
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.get(self.delete_url)
        notice = Notice.objects.first()
        # print(notice.author)
        if notice.author == 'testuser1' or notice.author.has_perm('delte_notice'):
            notice.delete()
            self.assertEqual(Notice.objects.count(), 0)
        else:
            self.assertEqual(response.status_code, 403)


    def test_notice_delete_unauthenticated(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 403)
        # self.assertTrue(response.url.startswith('/accounts/login/'))