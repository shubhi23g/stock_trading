from django.urls import include, re_path
from .views import *

urlpatterns = [
    re_path(r"^upload-file/$", upload_csv, name='upload_csv'),
    re_path(r"^stock-result/$",stock_result,name='stock_result'),
    re_path(r"^post-user/$",post_user,name='post_user'),
    re_path(r"^get-user-profile",get_user_profile,name='get_user_profile'),
]
