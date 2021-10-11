from django.urls import path

from . import views


urlpatterns = [
    path("", views.home_view, name="home"),
    path("posts/", views.JobPostList.as_view(), name="jobposts"),
    path('jobpost/<int:pk>/', views.JobPostGenericDetail.as_view(), name='jobpost_detail'),
    path('create/', views.JobPostCreate.as_view(), name='jobpost_create'),
    path('create/request/', views.JobPostRequest.as_view(), name='jobpost_request'),
    path('update/<int:pk>/', views.JobPostUpdate.as_view(), name='jobpost_update'),
    path('delete/<int:pk>/', views.JobPostDelete.as_view(), name='jobpost_delete'), 
    path('set_language/', views.change_language, name='set_language'),
]