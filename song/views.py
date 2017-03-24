from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic import View

from attendance.models import Song


class SongHomeView(View):

    def get(self, request):

        song_list = Song.objects.all().order_by('-no')

        context = {
            'song_list': song_list
        }

        return TemplateResponse(request, 'song/home.html', context)


class SongAddView(View):

    def get(self, request):

        return TemplateResponse(request, 'song/add.html')

    def post(self, request):

        no = request.POST.get('no')
        title = request.POST.get('title')
        author = request.POST.get('author')
        play_time = request.POST.get('play_time')

        song = Song()
        song.no = no
        song.title = title
        song.author = author
        song.play_time = play_time
        song.save()

        return HttpResponseRedirect(reverse('song:home'))


class SongEditView(View):

    def get(self, request, song_no):

        song = Song.objects.get(pk=song_no)

        context = {
            'song': song
        }
        return TemplateResponse(request, 'song/edit.html', context)

    def post(self, request, song_no):

        no = request.POST.get('no')
        title = request.POST.get('title')
        author = request.POST.get('author')
        play_time = request.POST.get('play_time')

        Song.objects.filter(pk=song_no).update(
            no=no, title=title, author=author, play_time=play_time
        )

        return HttpResponseRedirect(reverse('song:home'))