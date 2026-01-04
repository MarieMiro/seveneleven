from django.urls import path
from .views import bbs, BbDetailView, comments

urlpatterns = [
    path('bbs/<int:pk>/comments/', comments, name='api_bb_comments'),
    path('bbs/<int:pk>/', BbDetailView.as_view(), name='api_bb_detail'),
    path('bbs/', bbs, name='api_bbs'),
]

from django.urls import path
from .views import bbs, BbDetailView, comments

urlpatterns = [
    path('bbs/<int:pk>/comments/', comments, name='api_bb_comments'),
    path('bbs/<int:pk>/', BbDetailView.as_view(), name='api_bb_detail'),
    path('bbs/', bbs, name='api_bbs'),
]

