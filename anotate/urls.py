from django.contrib import admin
from django.urls import path, include
  # Import the home view
from authenticationApp.views import *
from addData.views import *
urlpatterns = [
    path('upload/',upload_file, name='upload_file'),
    path('admin/', admin.site.urls),
    path('', home, name="home"),      # Home page
    path("admin/", admin.site.urls),          # Admin interface
    path('login/', login_page, name='login_page'),    # Login page
    path('register/', register_page, name='register'),  # Correct URL for home page
    path('annotation-download/', download, name='download-csv'), # downlad CSV
    # path('create-annotation/', create_annotation, name='create-annotation'),
    path('random-titles/', random_titles_view, name='random-titles'),
]
