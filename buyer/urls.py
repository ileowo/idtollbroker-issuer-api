from django.urls import path

from . import views

urlpatterns = [
    path('tender', views.list_tenders),
    path('tender/<int:tender_id>/', views.get_tender),
    path('tender/<int:tender_id>/publish-tender', views.publish_tender),
    path('qualification-documents',views.get_qualification_documents),
    path('v2/tenders', views.v2_list_tenders),
    path('v2/tender/<int:tender_id>/', views.v2_get_tender),
]