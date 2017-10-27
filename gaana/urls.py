from django.conf.urls import url
from .import views

app_name = 'gaana'
urlpatterns = [
    #/music/
    url(r'^$', views.IndexView.as_view(),name='index'),
    url(r'^login_user/$', views.login_user, name='login'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    #/music/7142/
    #url(r'^(?P<album_id>[0-9]+)/$',views.DetailView.as_view(),name='detail'),
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(),name='detail'),

    #/music/7142/favorite/
    #url(r'^(?P<album_id>[0-9]+)/favorite/$',views.isfavorite,name='favorite'),
    url(r'album/add/$',views.AlbumCreate.as_view(),name="album-add"),

    url(r'album/(?P<pk>[0-9]+)/$',views.AlbumUpdate.as_view(),name="album-update"),

    url(r'album/(?P<pk>[0-9]+)/delete/$',views.AlbumDelete.as_view(),name="album-delete"),

    url(r'album/(?P<album_id>[0-9]+)/delete/(?P<song_id>[0-9]+)/$',views.delete_song,name="delete_song"),

    url(r'^register/$',views.UserFormView.as_view(),name='register'),

    url(r'^(?P<album_id>[0-9]+)/create_song/$', views.CreateSong, name='create_song'),

    url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),

    #url(r'^(?P<filter_by>[a-zA_Z]+)/songs/$',views.songs(),name='songs')


]