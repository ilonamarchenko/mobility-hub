from django.db import models
from django.contrib.auth.models import User
from django import forms
from django_countries.fields import CountryField

class University(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.country})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    home_university = models.CharField(max_length=100, blank=True, null=True)
    mobility_university = models.CharField(max_length=100, blank=True, null=True)
    biography = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class HomeUniversity(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

class MobilityUniversity(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    HASHTAG_CHOICES = [
        ('academic', 'Academic Advice'),
        ('housing', 'Housing'),
        ('culture', 'Cultural Experience'),
        ('custom', 'Other'),
    ]

    EXCHANGE_PROGRAM_CHOICES = [
        ('Erasmus+', 'Erasmus+'),
        ('DAAD', 'DAAD'),
        ('Fulbright', 'Fulbright'),
        ('MEVLANA', 'Mevlana'),
        ('Other', 'Other'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    hashtag_choice = models.CharField(max_length=20, choices=HASHTAG_CHOICES)
    custom_hashtag = models.CharField(max_length=50, blank=True)

    university = models.CharField(max_length=100)
    country = CountryField()
    exchange_program = models.CharField(max_length=100, choices=EXCHANGE_PROGRAM_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_display_hashtag(self):
        return self.custom_hashtag if self.hashtag_choice == 'custom' else dict(self.HASHTAG_CHOICES)[self.hashtag_choice]

    def __str__(self):
        return self.title

    def clean(self):
        if self.hashtag_choice == 'custom' and not self.custom_hashtag:
            raise forms.ValidationError("Please provide a custom hashtag.")

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_moderated = models.BooleanField(default=False)


class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


class SearchLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('reviewed', 'Reviewed'),
        ('closed', 'Closed')
    ], default='open')

