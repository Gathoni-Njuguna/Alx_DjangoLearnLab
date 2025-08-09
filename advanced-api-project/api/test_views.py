# api/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Book, Tag, Rating
import json

User = get_user_model()

class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass'
        )
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='otherpass'
        )
        
        # Create tags
        self.positive_tag = Tag.objects.create(vote='positive')
        self.negative_tag = Tag.objects.create(vote='negative')
        
        # Create books
        self.book1 = Book.objects.create(
            title='Django Basics',
            description='Intro to Django',
            created_by=self.user
        )
        self.book1.tags.add(self.positive_tag)
        
        self.book2 = Book.objects.create(
            title='Advanced Python',
            description='Deep dive into Python',
            created_by=self.other_user
        )
        self.book2.tags.add(self.negative_tag)
        
        # Create ratings
        Rating.objects.create(
            tag=self.positive_tag,
            score=4,
            comment='Good resource',
            created_by=self.user
        )
        Rating.objects.create(
            tag=self.negative_tag,
            score=2,
            comment='Needs improvement',
            created_by=self.other_user
        )