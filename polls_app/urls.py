from django.urls import path
from . import views


app_name = 'polls_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('polls/', views.PollsView.as_view(), name='polls'),
    path('polls/poll/<int:pk>/', views.PollView.as_view(), name='poll'),
    path('polls/text_poll/<int:pk>/', views.text_poll, name='text_poll'),  # FIXME: merge with 'poll'
    path('polls/<int:pk>/make_vote/', views.make_vote, name='make_vote'),
    path('polls/<int:pk>/make_text_vote/', views.make_text_vote, name='make_text_vote'),
    path('polls/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('polls/completed/', views.CompletedPollsView.as_view(), name='completed'),
]
