from email import contentmanager
from tkinter import font
from turtle import title
from unicodedata import category, name
from django.shortcuts import render,redirect
from django.views.generic import View
from .models import Post,Category
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(View):
    def get(self, request, *args, **kwargs ):
        post_data = Post.objects.order_by("-id")
        latest_data = Post.objects.all()[:5]
        return render(request, "app/index.html",{
            "post_data":post_data,
            "latest_data":latest_data
        })

class PostDetailView(View):
    def get(self, request, *args, **kwargs ):
        post_data = Post.objects.get(id=self.kwargs["pk"])
        latest_data = Post.objects.all()[:5]
        return render(request, "app/post_detail.html",{
            "post_data":post_data,
            "latest_data":latest_data
        })

class CreatePostView(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        form = PostForm(request.POST or None)
        return render(request,"app/post_form.html",{
            "form": form
        })
        
    def post(self, request, *args, **kwargs ):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post()
            post_data.auther = request.user
            post_data.title = form.cleaned_data["title"]
            post_data.subtitle = form.cleaned_data["subtitle"]
            category = form.cleaned_data["category"]
            category_data = Category.objects.get(name=category)
            post_data.category = category_data
            post_data.content = form.cleaned_data["content"]
            if request.FILES:
                post_data.image = request.FILES.get("image")
            post_data.save()
            return redirect("post_detail", post_data.id)

        return render(request,"app/post_form.html",{
             "form": form
        })

class PostEditView(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs["pk"])
        form = PostForm(
            request.POST or None,
            initial={
                "title"  : post_data.title,
                "subtitle":post_data.title,
                "content": post_data.content,
                "image"  : post_data.image,
                "category":post_data.category
            }
        )
        return render(request,"app/post_form.html",{
            "form": form
        })

    def post(self, request, *args, **kwargs ):

        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs["pk"])
            post_data.title = form.cleaned_data["title"]
            post_data.subtitle = form.cleaned_data["subtitle"]
            category = form.cleaned_data["category"]
            category_data = Category.objects.get(name=category)
            post_data.category = category_data
            post_data.content = form.cleaned_data["content"]
            if request.FILES:
                post_data.image = request.FILES.get("image")
            post_data.save()
            return redirect("/")

        return render(request,"app/post_form.html",{    
             "form": form
        })

class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs["pk"])
        print("取得します")
        return render(request,"app/post_delete.html",{
             "post_data": post_data
        })

    def post(self, request, *args, **kwargs ):
        print("削除します。")
        post_data = Post.objects.get(id=self.kwargs["pk"])
        post_data.delete()
        return redirect("index")

class CategoryView(View):
    def get(self,request,*args, **kwargs):
        category_data = Category.objects.get(name=self.kwargs["category"])
        post_data = Post.objects.order_by("-id").filter(category = category_data)
        latest_data = Post.objects.all()[:5]
        return render(request,"app/index.html",{
            "post_data":post_data,
            "latest_data":latest_data
        })
       