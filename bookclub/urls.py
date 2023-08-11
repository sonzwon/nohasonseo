from django.urls import path
from bookclub import views

# 회원관리
app_name = 'bookclub'

urlpatterns = [
    path('booklist/', views.book_list , name='book_list'),
]