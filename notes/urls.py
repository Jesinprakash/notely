
from django.urls import path

from notes import views

from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns=[

    path('register/',views.UserCreationView.as_view()),

    path('task/',views.TaskCreateListView.as_view()),

    path('task/<int:pk>/',views.TaskRetrieveUpdateDeleteView.as_view()),

    path('task/summary',views.TaskSummaryApi.as_view()),

    path('category/',views.CategoryListView.as_view()),

    path('token/',ObtainAuthToken.as_view()),

    
    
    
]