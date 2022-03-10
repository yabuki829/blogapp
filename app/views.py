from email import contentmanager, message
from tkinter import font
from turtle import title
from unicodedata import category, name
import django
from django.conf import settings

from django.shortcuts import render,redirect
from django.views.generic import View
from .models import Post,Category
from .forms import ContactForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from functools import reduce
from operator import and_
from django.core.paginator import Paginator
from django.core.mail import BadHeaderError,EmailMessage
from django.http import HttpResponse
import textwrap


class IndexView(View):
    def get(self, request, *args, **kwargs ):
          # ページネーション
        p = Paginator(Post.objects.order_by("-id"),10)
        page = request.GET.get("page")
        posts = p.get_page(page)

        latest_data = Post.objects.order_by("-id")[:5]
        return render(request, "app/index.html",{
          
            "latest_data":latest_data,
            "posts" : posts
        })

class PostDetailView(View):
    def get(self, request, *args, **kwargs ):
        post_data = Post.objects.get(id=self.kwargs["pk"])
        latest_data = Post.objects.order_by("-id")[:5]
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
                "subtitle":post_data.subtitle,
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
        p = Paginator(post_data,20)
        page = request.GET.get("page")
        posts = p.get_page(page)
        latest_data = Post.objects.order_by("-id")[:5]
        return render(request,"app/index.html",{
            "posts":posts,
            "latest_data":latest_data
        })
       

class SearchView(View):
    def get(self,request,*args,**kwargs):
        post_data = Post.objects.order_by("-id")
        latest_data = Post.objects.order_by("-id")[:5]
        keyword = request.GET.get("keyword")
        print("ok1")
        if keyword:
            excluded_list = set([' ','　'])
            query_list =''
            print("ok2")
            for word in keyword:
                if not word in excluded_list:
                    query_list += word
            query = reduce(and_,[Q(title__icontains=q)| Q(content__icontains=q) for q in query_list])
            post_data = post_data.filter(query)
            p = Paginator(post_data,20)
            page = request.GET.get("page")
            posts = p.get_page(page)

        return render(request,"app/index.html",{
            "keyword" : keyword,
            "posts":posts,
            "latest_data":latest_data
        })

       
class ContactView(View):
    def get(self,request,*args,**kwargs):
        form = ContactForm(request.POST or None)
        return render(request,"app/contact.html",{
            "form":form
        })
    def post(self, request, *args, **kwargs ):
        form = ContactForm(request.POST or None)
        if form.is_valid():
            _name = form.cleaned_data["name"]
            _email = form.cleaned_data["email"]
            _title = form.cleaned_data["title"]
            _message = form.cleaned_data["message"]

            subject = "お問い合わせありがとうございます。"

            contact = textwrap.dedent('''
                {name} 様

                本日から三日以内にご返信いたします。
                少々お待ちください。

                -----------------------------------
                お名前
                {name}

                メール 
                {email}
                
                件名 
                {title}

                メッセージ
                {message}
                -----------------------------------
            ''').format(
                    name= _name,
                    email=_email,
                    title=_title,
                    message=_message
                )
            to_list = [_email]
            bcc_list = [settings.EMAIL_HOST_USER]

            try:
                message=EmailMessage(subject=subject,body=contact,to=to_list,bcc=bcc_list)
                message.send()
            except BadHeaderError :
                return HttpResponse("無効なヘッダーが検出されました。")

            return redirect("index")
        
        return render(request,"app/contact.html",{
                "form" :form
        })
