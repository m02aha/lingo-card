from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name='home'),
     path('translate/',views.queryTranslation,name='translate'),
     path('revise/',views.cards_revision,name='revise'),
     path('status-change/',views.status_change,name='status_change'),
    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),
  
]
# Serve media files during development

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)