from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Album,Song,Comment
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.views.generic import View
from .form import UserForm,SongForm,AlbumForm,CommentForm
from django.http import JsonResponse
from django.db.models import Q
#from django.contrib.comments

class IndexView(generic.ListView):
    template_name = 'gaana/index.html'
    context_object_name = 'albums'

    def get_queryset(self):
        return Album.objects.all()

class DetailView(generic.DetailView):
    model = Album
    template_name = 'gaana/detail.html'

class AlbumCreate(CreateView):
    model = Album
    fields = ['artist','album_title','genre','album_logo']

class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('gaana:index')

# class SongCreate(CreateView):
#     model = Song
#     fields =['song_title','song_file']

class UserFormView(View):
    form_class = UserForm
    template_name = 'gaana/registration_form.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            #cleaned data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #returning user object if credentials are true
            user = authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('gaana:index')

        return render(request,self.template_name,{'form':form})

Audio_file_type=['mp3','wav','ogg']
Image_file_type = ['jpg','png','jpeg']

def CreateSong(request,album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        album_songs = album.song_set.all()
        for song in album_songs:
            if song.song_title == form.cleaned_data.get("song_title"):
                context = {'album':album,'form':form,'error_message':'Already in database'}
                return render(request,'gaana/create_song.html',context)
        song = form.save(commit=False)
        song.album = album
        song.song_file = request.FILES['song_file']
        file_type = song.song_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in Audio_file_type:
            context = {'album':album,'form':form,'error_message':'File must be of type mp3,wav,ogg',}
            return render(request,'gaana/create_song.html',context)

        song.save()
        return render(request,'gaana/detail.html',{'album':album})
    context={'album':album,'form':form}
    return render(request,'gaana/create_song.html',context)

class SongDelete(DeleteView):
    model = Song
    success_url = reverse_lazy('gaana/detail.html')

def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'gaana/detail.html', {'album': album})

def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

def songs(request,filter_by):
    if not request.user.is_autenticate():
        return render(request,'gaana/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            user_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                user_songs = user_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            user_songs = []
            return render(request,'gaana:songs',{'song_list':user_songs,'filter_by':filter_by})

def add_comment(request,album_id):
    album = get_object_or_404(Album,pk=album_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        comment_obj = Comment(album=album,content=content)
        comment_obj.save()

        comments = album.comment_set.all()
        context = {"comments":comments,
               "comment_form":form}
        return render(request,'gaana/detail.html',context)
    return render(request,'gaana/detail.html')



def login_user(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                albums = Album.objects.get(user=request.user)
                return render(request,'gaana:index',{'albums':albums})
            else:
                return render(request,'gaana/login.html',{'error_message':'Session time out Please try again'})

        return render(request,'gaana/login.html',{'error_message':'Invalid credentials please try again'})

    return render(request,'gaana/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {'form':form,}
    return render(request,'gaana/login.html',context)

# from django.shortcuts import render,get_object_or_404
# from django.http import HttpResponse,Http404
#
# from .models import Album,Song
#
# def index(request):
#     all_albums = Album.objects.all()
#     context = {
#         'albums':all_albums,
#         'count':all_albums.count()
#     }
#     return render(request,'gaana/index.html',context)
# def detail(request,album_id):
#     album = get_object_or_404(Album,pk=album_id)
#     #or
#     # try:
#     #     album=Album.objects.get(pk=album_id)
#     # except Album.DoesNotExist:
#     #     raise Http404("Album does nt exist")
#     return render(request,'gaana/detail.html',{'album':album})
# def isfavorite(request,album_id):
#     album = get_object_or_404(Album, pk=album_id)
#     try:
#         selected_song = album.song_set.get(pk=request.POST['song'])
#     except (KeyError,Song.DoesNotExist):
#         return render(request,'gaana/detail.html',{'album':album,'error_message':"You did not select a valid song"})
#     else:
#         selected_song.is_favorite=True
#         selected_song.save()
#         return render(request, 'gaana/detail.html', {'album': album})


