from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import JSONField  

class CustomUser(AbstractUser):
    profile_picture = models.URLField(max_length=250, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_requested = models.BooleanField(default=False)
    bookmarks = models.JSONField(default=list, blank=True)
    library = models.JSONField(default=list, blank=True)
    following = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.username}"

    def add_bookmark(self, slug):
        if slug not in self.bookmarks:
            self.bookmarks.append(slug)
            self.save()

    def remove_bookmark(self, slug):
        if slug in self.bookmarks:
            self.bookmarks.remove(slug)
            self.save()

    def get_bookmarks(self):
        return self.bookmarks

    def add_library(self, slug):
        if slug not in self.librarys:
            self.library.append(slug)
            self.save()

    def remove_library(self, slug):
        if slug in self.library:
            self.library.remove(slug)
            self.save()

    def get_library(self):
        return self.library

    def add_following(self, slug):
        if slug not in self.following:
            self.following.append(slug)
            self.save()

    def remove_following(self, slug):
        if slug in self.following:
            self.following.remove(slug)
            self.save()

    def get_following(self):
        return self.following
