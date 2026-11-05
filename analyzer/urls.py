from django.urls import path
from . import views

urlpatterns = [

    path(
        'resume/<int:resume_id>/',
        views.analyze_resume,
        name='resume_analysis'
    ),

    path(
        'result/<int:analysis_id>/',
        views.analysis_result,
        name='analysis_result'
    ),

    path(
        'history/',
        views.history,
        name='history'
    ),
]