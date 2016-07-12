from django.conf.urls import include, url

from .views import *

urlpatterns = [
    url(r'^0802c8786a09ae44a56a072d9d9a5e5da3172747df3d39e915/', MessengerInterface.as_view()),
    url(r'^32h3jk543kl4h32k4v3b44h5jbm33354s234i32ae3454543pl/', BotInterface.as_view()),
]