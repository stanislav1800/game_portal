from django.urls import path
from .views import BulletinsList, BulletinDetail, BulletinCreate, BulletinUpdate, BulletinDelete, ResponseCreate, ResponseListView, IndexView, ResponseUpdateView, ResponseDeleteView, CategoryListView, subscribe, unsubscribe


urlpatterns = [
    path("board/", BulletinsList.as_view(), name='bulletins'),
    path('board/<int:pk>/', BulletinDetail.as_view(), name='bulletin'),
    path('board/create/', BulletinCreate.as_view(), name='bulletin_create'),
    path('board/<int:pk>/edit/', BulletinUpdate.as_view(), name='bulletin_edit'),
    path('board/<int:pk>/delete/', BulletinDelete.as_view(), name='bulletin_delete'),
    path('board/<int:pk>/response/', ResponseCreate.as_view(), name='response_create'),
    path('author/<int:author_id>/responses/', ResponseListView.as_view(), name='author_response_list'),
    path('response/<int:pk>/update/', ResponseUpdateView.as_view(), name='response_update'),
    path('response/<int:pk>/delete/', ResponseDeleteView.as_view(), name='response_delete'),
    path('author/', IndexView.as_view(), name='author_page'),
    path('categories/<int:pk>/', CategoryListView.as_view(), name = 'category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
    ]