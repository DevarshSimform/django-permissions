# from django.test import SimpleTestCase
# from django.urls import reverse, resolve
# from classroom.views import *
# from django.contrib.auth.views import LoginView, LogoutView

# class TestUrls(SimpleTestCase):

#     def test_list_url_resoles(self):
#         url = reverse('notice_list')
#         print(resolve(url))
#         self.assertEqual(resolve(url).func, notice_list)     
    
#     def test_create_url_resoles(self):
#         url = reverse('notice_create')
#         self.assertEqual(resolve(url).func, notice_create)  

#     def test_group_url_resolves(self):
#         url = reverse('groups')
#         self.assertEqual(resolve(url).func, groups)  

#     def test_assign_url_resolves(self):
#         url = reverse('assign_notice')
#         self.assertEqual(resolve(url).func, assign_notice) 


#     # pass kwargs for parameters in url
        
#     def test_update_url_resolves(self):
#         url = reverse('notice_update', kwargs={'pk': 2})
#         self.assertEqual(resolve(url).func, notice_update) 

#     def test_delete_url_resolves(self):
#         url = reverse('notice_delete', kwargs={'pk': 1})
#         self.assertEqual(resolve(url).func, notice_delete)

#     def test_register_url_resolves(self):
#         url = reverse('register')
#         self.assertEqual(resolve(url).func, register)


#     # for class based views

#     def test_login_url_resolves(self):
#         url = reverse('login')
#         self.assertEqual(resolve(url).func.view_class, LoginView)

#     def test_logout_url_resolves(self):
#         url = reverse('logout')
#         self.assertEqual(resolve(url).func.view_class, LogoutView)
