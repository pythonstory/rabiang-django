from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.test.client import Client

from .models import Post


class PostTest(TestCase):
    def test_create_post(self):
        # store the password to login later
        password = 'mypassword'

        admin = User.objects.create_superuser('admin', 'admin@test.com',
                                              password)

        c = Client()

        # You'll need to log him in before you can send requests through the client
        c.login(username=admin.username, password=password)

        post = Post()

        post.title = 'My first post'
        post.slug = 'my-first-post'
        post.body = 'This is my first blog post'
        post.author = admin

        post.save()

        post1 = get_object_or_404(Post, title='My first post')

        self.assertEquals(post1.title, post.title)
