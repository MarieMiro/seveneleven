from django.urls import path
from .views import index
from .views import other_page
from .views import BBLoginView
from .views import profile
from .views import ProfileEditView
from .views import PasswordEditView
from .views import RegisterView, RegisterDoneView
from .views import user_activate
from .views import ProfileDeleteView
from .views import rubric_bbs
from .views import bb_detail
from .views import profile_bb_add
from .views import profile_bb_edit, profile_bb_delete
from .views import mail_filters
from django.contrib.auth.views import LogoutView

app_name = 'main'
urlpatterns = [
    path('accounts/activate/<str:sign>/', user_activate, name='activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(),
      name='register_done'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/password/edit/', PasswordEditView.as_view(),
        name='password_edit'),
    path('accounts/profile/delete/', ProfileDeleteView.as_view(),
        name='profile_delete'),
    path('accounts/profile/edit/', ProfileEditView.as_view(),
        name='profile_edit'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('accounts/profile/edit/<int:pk>/', profile_bb_edit,
         name='profile_bb_edit'),
    path('accounts/profile/delete/<int:pk>/', profile_bb_delete,
         name='profile_bb_delete'),

    path('accounts/profile/add/', profile_bb_add, name='profile_bb_add'),
    path('<int:rubric_pk>/<int:pk>/', bb_detail, name='bb_detail'),
    path('<int:pk>/', rubric_bbs, name='rubric_bbs'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
    path('accounts/mail/filters/', mail_filters, name='mail_filters'),
]