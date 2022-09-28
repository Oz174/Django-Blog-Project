
from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from .forms import * 
from .decorators import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required



#Auth and Admin redirection 

@user_unauthorized
def signupUser(request):
        signup_form = UserSignupForm()
        if request.method == 'POST':
            signup_form = UserSignupForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                user = request.POST.get('username')
                messages.success(request,'Account success for user  ' + user)
                return redirect('login')
        context = {'signup_form': signup_form}
        return render(request, 'blogapp/signup.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

def to_django_admin(request,path_dir):
    if path_dir == "":
        return HttpResponseRedirect('http://127.0.0.1:8000/admin/')
    elif path_dir=="posts":
        return HttpResponseRedirect('http://127.0.0.1:8000/admin/blogapp/post/')
    elif path_dir=="categories":
        return HttpResponseRedirect('http://127.0.0.1:8000/admin/blogapp/category/')
    elif path_dir=="users":
        return HttpResponseRedirect('http://127.0.0.1:8000/admin/auth/user/')

def loginUser(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        psw = request.POST.get('password')
        user = authenticate(username=name, password=psw)
        if user:
                login(request, user)
                if user.is_active:
                    if request.GET.get('next') is not None:
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect('home')
                else:
                    admin = User.objects.filter(is_superuser=True, is_active=True).first()
                    messages.info(request, 'You have been blocked by an admin please contact us @ this email : ' + admin.email)    
        else:
                messages.info(request, 'Incorrect Username or Password')
    return render(request, 'blogapp/login.html')

def home(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(posts, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if 'search' in request.GET:
        search_term = request.GET.get('search',None)
        if search_term is not None:
            search_result = Post.objects.all().filter(content__icontains=search_term )
            paginator = Paginator(search_result, 3) 
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'blogapp/overviews.html', {'categories':categories , 'page_obj':page_obj})
        else:
            return HttpResponse("No Posts Found")
    else:
        context = {'categories':categories , 'page_obj':page_obj}
        return render(request, 'blogapp/home.html', context)

@login_required(login_url='login')
def subscribe(request , category_id):
    category = Category.objects.get(id=category_id)
    user = request.user
    category.users.add(user)
    #sending email 
    send_mail('Welcome to the Category', 'You have successfully subscribed to the ' + category.cname + ' category', settings.EMAIL_HOST_USER, [user.email])
    return redirect('home') 

@login_required(login_url='login')
def unsubscribe(request , category_id):
    category = Category.objects.get(id=category_id)
    user = request.user
    category.users.remove(user)
    #sending email 
    send_mail('We Heard you unsubscribed !', 'You have successfully unsubscribed from the ' + category.cname + ' category', settings.EMAIL_HOST_USER, [user.email])
    return redirect('home') 


def category_posts(request, category_id):
    categories = Category.objects.all()
    posts = Post.objects.filter(category=category_id)
    if posts is None: 
        return HttpResponse('No posts founded Here')
    paginator = Paginator(posts, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    category_name = Category.objects.get(id=category_id).cname
    if 'search' in request.GET:
        search_term = request.GET.get('search',None)
        if search_term is not None:
            search_result = Post.objects.all().filter(content__icontains=search_term )
            paginator = Paginator(search_result, 3) 
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'blogapp/overviews.html', {'categories':categories , 'page_obj':page_obj})
        else:
            return HttpResponse("No Posts Found")
    context = {'page_obj':page_obj , 'categ_name':category_name , 'categories':categories}
    return render(request,'blogapp/category_posts.html',context)


#Who's the poster ? How do I get him
@login_required(login_url='login')
def AddPost(request):
        form = PostsForm()
        context = {"form": form}
        if request.method == "POST":
            form = PostsForm(request.POST,request.FILES)
            if form.is_valid():
                post = form.save(commit = False)
                post.author = request.user
                post.save()
                return redirect('home')
        else:
            return render(request, 'blogapp/addpost.html', context)
        return redirect('home')

@login_required(login_url='login')
def EditPost(request,p_id):
    post = Post.objects.get(pk=p_id)
    form = PostsForm(instance=post)
    context = {'form':form}
    if request.method == "POST":
            form = PostsForm(request.POST,request.FILES,instance=post)
            if form.is_valid():
                form.save()
                return post_details(request,p_id)
    else:
            return render(request, 'blogapp/editpost.html', context)

@login_required(login_url='login')
def DeletePost(request,p_id):
    post = Post.objects.get(pk=p_id)
    post.delete()
    return redirect('home')


def AddComment(request):
    c_form  = CommentForm()
    if request.method == "POST":
        c_form = CommentForm(request.POST)
    return c_form

@login_required(login_url='login')
def DeleteComment(request,c_id):
    comment = Comment.objects.get(pk=c_id)
    p_id = comment.post_id.id
    comment.delete()
    return redirect('post',p_id=p_id)

@login_required(login_url='login')
def like(request,p_id):
    post=Post.objects.get(pk=p_id)
    try:
        go = Likes.objects.get(post_id=p_id,liker_id=request.user.id)
    except Likes.DoesNotExist:
        go = None

    if go is None: 
        Likes.objects.create(post_id=post,liker_id=request.user,like_or_dislike=True)
    else:
        go.delete()
        Likes.objects.create(post_id=post,liker_id=request.user,like_or_dislike=True)
    return  redirect('post',p_id=p_id)

#auto_delete
@login_required(login_url='login')
def dislike(request,p_id):
    post=Post.objects.get(pk=p_id)
    try:
        go = Likes.objects.get(post_id=p_id,liker_id=request.user.id)
    except Likes.DoesNotExist:
        go = None

    if go is None: 
        Likes.objects.create(post_id=post,liker_id=request.user,like_or_dislike=False)
    else:
        go.delete()
        Likes.objects.create(post_id=post,liker_id=request.user,like_or_dislike=False)
    #auto-deletion    
    if Likes.objects.filter(post_id=p_id , like_or_dislike=False).count() == 10:
        post = Post.objects.get(pk=p_id)
        post.delete()
        messages.info(request,'Post ' + p_id + ' has been deleted for having more than 10 dislikes')
        return redirect('home')
    else: 
        return redirect('post',p_id=p_id)

def post_details(request, p_id):
    post = Post.objects.get(pk = p_id)
    categories = Category.objects.all()
    comments = Comment.objects.filter(post_id = p_id)
    likes = Likes.objects.filter(post_id=p_id , like_or_dislike=True).count()
    dislikes = Likes.objects.filter(post_id=p_id , like_or_dislike=False).count()
    post.Tag = post.content.partition("#")[2] or post.Tag
    c_form = AddComment(request)
    parent_obj = None
    try:
        parent_id = int(request.POST.get("parent_id"))
    except:
        parent_id= None
    if parent_id is not None:
        parent_qs = Comment.objects.filter(id=parent_id)
        if parent_qs.exists() and parent_qs.count()==1 :
            parent_obj = parent_qs.first()

    if c_form.is_valid():
        temp_comment = c_form.save(commit=False)
        temp_comment.commented_by = request.user
        temp_comment.post_id = post 
        temp_comment.parent = parent_obj
        temp_comment.save()
        c_form = CommentForm()
    
    if 'search' in request.GET:
        search_term = request.GET.get('search',None)
        if search_term is not None:
            search_result = Post.objects.all().filter(content__icontains=search_term ) 
            return render(request, 'blogapp/overviews.html', {'posts' : search_result , 'categories':categories})
        else:
            return HttpResponse("No Posts Found")

    context = {'post':post , 'categories':categories , 'comments':comments , 'likes':likes , 'dislikes':dislikes , 'c_form':c_form}
    return render(request,'blogapp/postdetails.html',context)
    #need to import likes and dislikes and comments 


@only_admins
def allUsers (request):
    paginator = Paginator(User.objects.all().order_by('username'), 15) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'blogapp/users_dashboard.html',{'page_obj':page_obj})


@only_admins
def promoteUser(request,user_id):
    u = User.objects.get(pk=user_id)
    u.is_staff = True
    u.is_superuser = True
    u.save()
    return redirect('all_users')


@only_admins
def lockUser(request,user_id):
    u = User.objects.get(pk=user_id)
    u.is_active = False
    u.save()
    return redirect('all_users')

@only_admins
def unlockUser(request , user_id):
   u = User.objects.get(pk=user_id)
   u.is_active = True
   u.save()
   return redirect('all_users')

   
