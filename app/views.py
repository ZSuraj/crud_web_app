from django.shortcuts import render, redirect
from app.models import *
from django.forms import ModelForm
from django import forms
from bs4 import BeautifulSoup
import requests

# Create your views here.
def home(req):
    title = "Welcome to DJANGO"
    posts = Post.objects.all()
    return render(req, 'home.html', {'posts': posts})

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['url', 'body']
        labels = {
            'body' : 'Caption',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a caption...', 'class': 'font1 text-4xl'}),
            'url': forms.TextInput(attrs={'placeholder': 'Add url'})
        }

def post_create(req):
    form = PostCreateForm()

    if req.method == "POST":
        form = PostCreateForm(req.POST)
        if form.is_valid():
            post = form.save(commit=False)
            website = requests.get(form.data['url'])
            source_code = BeautifulSoup(website.text, 'html.parser')
            find_image = source_code.select('meta[content^="https://live.staticflickr.com/"]')
            if find_image and find_image[0]:
                image = find_image[0]['content']
                post.image = image

            find_title = source_code.select('h1.photo-title')
            if find_title and find_title[0]:
                title = find_title[0].text.strip()
                post.title = title

            find_artist = source_code.select('a.owner_name')
            if find_artist and find_artist[0]:
                artist = find_artist[0].text.strip()
                post.artist = artist

            post.save()
            return redirect("home")
    return render(req, 'post_create.html', { 'form': form })
