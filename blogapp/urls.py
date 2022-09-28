from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.home, name='home'),
    path('category/<category_id>', views.category_posts, name='category_posts'),
    path('subscribe/<category_id>' , views.subscribe , name='subscribe'),
    path('post/<p_id>', views.post_details , name='post'),
    path('addpost/', views.AddPost , name='add_post'),
    path('deletepost/<p_id>', views.DeletePost , name='delete_post'),
    path('like/<p_id>', views.like , name='like'),
    path('dislike/<p_id>', views.dislike , name='dislike'),
    path('deletecomment/<c_id>', views.DeleteComment , name='delete_comment'),
    path('editpost/<p_id>', views.EditPost , name='edit_post'),
    path('unsubscribe/<category_id>' , views.unsubscribe , name='unsubscribe'),
    path('login/',views.loginUser , name='login'),
    path('logout/',views.logoutUser , name='logout'),
    path('signup/',views.signupUser , name='signup'),
    path('myadmin/<path_dir>',views.to_django_admin, name='to_django_admin'),
    path('allusers/',views.allUsers , name='all_users'),
    path('promote/<user_id>',views.promoteUser , name='promote'),
    path('lock/<user_id>', views.lockUser , name='lock'),
    path('unlock/<user_id>', views.unlockUser , name='unlock')
]