from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog
from .forms import BlogPost

# Create your views here.
def home(request):
    blogs = Blog.objects 

    #블로그 페이지 3개씩 찍기
    blog_list = Blog.objects.all()
    paginator = Paginator(blog_list, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'home.html', {'blogs':blogs,'posts':posts})

def detail(request, blog_id):
    details = get_object_or_404(Blog, pk = blog_id)

    return render(request, 'detail.html', {'details':details})
 
# new.html의 띄어주는 함수
def new (request):
    return render(request,'new.html')

# 입력받은 내용을 데이터 베이스에 넣어주는 함수
def create(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()     # 객체.deleate() 삭제
    return redirect('/blog/'+str(blog.id))   # redirect : 위에 상황을 처리한훈 해당 URL이동

def blogpost(request):
    # 1. 입력된 내용을 처리하는 기능 POST
    # 2. 빈페이지를 띄어주는 기능 GET
    if request.method == 'POST':
        form = BlogPost(request.POST)
        if form.is_valid():
            post = form.save(commit= False) # 모델 객체를 가져오고 저장은 아직안함
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')

    else :
        form = BlogPost()
        return render(request, 'new.html', {'form':form})