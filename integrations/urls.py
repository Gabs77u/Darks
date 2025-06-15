from django.urls import path
from .api_base import (
    VPNStatusAPI,
    UserListAPI,
    UserDetailAPI,
    UserSearchAPI,
    UserFilterStatusAPI,
)

urlpatterns = [
    path("api/vpn/", VPNStatusAPI.as_view(), name="vpn-status"),
    path("api/users/", UserListAPI.as_view(), name="user-list"),
    path("api/users/<int:user_id>/", UserDetailAPI.as_view(), name="user-detail"),
    path("api/users/search/", UserSearchAPI.as_view(), name="user-search"),
    path("api/users/filter/", UserFilterStatusAPI.as_view(), name="user-filter-status"),
]
