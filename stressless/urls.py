"""stressless URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from stresslessapi.views import (
    login_user, register_user, Profile,
    PriorityView, ReflectionView, PostView,
    CommentView, UserView, AppUserView, ResourceView,
    MotivationView, ReactionView, PostReactionView)




router = routers.DefaultRouter(trailing_slash=False)
router.register(r'profile', Profile, 'profile')
router.register(r'priorities', PriorityView, 'priority')
router.register(r'reflections', ReflectionView, 'reflection')
router.register(r'posts', PostView, 'post')
router.register(r'comments', CommentView, 'comment')
router.register(r'reactions', ReactionView, 'reaction')
router.register(r'post_reactions', PostReactionView, 'post_reaction')
router.register(r'users', UserView, 'user')
router.register(r'appusers', AppUserView, 'app_user')
router.register(r'resources', ResourceView, 'resource')
router.register(r'motivation', MotivationView, 'motivation')


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
