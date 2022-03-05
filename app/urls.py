from django.urls import path,include
from app import views   
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.IndexView.as_view(),name="index"),
    path('post/<int:pk>',views.PostDetailView.as_view(),name="post_detail"),   
    path('post/new',views.CreatePostView.as_view(),name="create_new"),   
    path('post/<int:pk>/edit',views.PostEditView.as_view(),name="post_edit"),   
    path('post/<int:pk>/delete',views.PostDeleteView.as_view(),name="post_delete"),    
    path(r'mdeditor/', include('mdeditor.urls')) # 追加
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

