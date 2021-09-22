from django.contrib import admin
from stresslessapi.models import AppUser, Comment, Motivation, PostReaction, Post, Priority, Reaction, Reflection, Resource


# Register your models here.
admin.site.register(AppUser)
admin.site.register(Comment)
admin.site.register(Motivation)
admin.site.register(PostReaction)
admin.site.register(Post)
admin.site.register(Priority)
admin.site.register(Reaction)
admin.site.register(Reflection)
admin.site.register(Resource)
