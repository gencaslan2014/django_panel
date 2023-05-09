from django.urls import path
from polls import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('login_user/', views.login_user, name="login_user"),]


urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)