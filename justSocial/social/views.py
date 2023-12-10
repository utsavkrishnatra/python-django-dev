from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import View
from .models import Post,Comment,UserProfile
from .forms import PostForm,CommentForm
from django.views.generic.edit import UpdateView,DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.db.models import Q

class PostListView( LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        
        logged_in_user=request.user
        # posts=Post.objects.all().order_by('-created_on')
        posts=Post.objects.all().filter(
            author__profile__followers__in=[logged_in_user.id]
        )
        
        form=PostForm()
        context={
            'post_list':posts,
            'form':form,
        }
        
        return render(request,'post.html',context=context)
        
    def post(self,request,*args, **kwargs):
        posts=Post.objects.all().order_by('-created_on')
        form=PostForm(request.POST)
        
        if(form.is_valid()):
            new_post=form.save(commit=False)
            new_post.author=request.user
            new_post.save()
            
        context={
            'post_list':posts,
            'form':form,
        }
        return render(request,'post.html',context=context)
            
            

class PostDetailView(LoginRequiredMixin,View):
    def get(self,request,pk, *args, **kwargs):
        print("Primary Key:",pk)
        post=Post.objects.get(pk=pk)
        form=CommentForm()
        
        comments=Comment.objects.filter(post=post).order_by('-created_on')
            
        context={
            'post':post,
            'form':form,
            'comments':comments
        }
        
        return render(request,'post_detail.html',context)

    
    def post(self,request,pk,*args, **kwargs):
        post=Post.objects.get(pk=pk)
        form=CommentForm(request.POST)
        
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.author=request.user
            new_comment.post=post
            new_comment.save()
            
            comments=Comment.objects.filter(post=post).order_by('-created_on')
            
            form=CommentForm()
            context={
            'post':post,
            'form':form,
            'comments':comments
            }
            
          
            
        return render(request,'post_detail.html',context)
    
            
        
       
        
        
     

class PostEditView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['body']
    template_name='post_edit.html'
    
    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse_lazy('post_detail',kwargs={'pk':pk})
   
    def test_func(self):
        post=self.get_object()
        return self.request.user== post.author



class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    template_name='post_delete.html'
    success_url=reverse_lazy('post_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Rename the variable from 'object' to 'post'
        context['post'] = self.get_object()
        return context
    
    def test_func(self):
        post=self.get_object()
        return self.request.user== post.author

    
class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Comment
    template_name='comment_delete.html'
    
    def get_success_url(self):
        pk=self.kwargs['post_pk']
        return reverse_lazy('post_detail',kwargs={'pk':pk})
    
    def test_func(self):
        comment=self.get_object()
        return self.request.user == comment.author

    
    
    
class CommentEditView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Comment
    fields=['comment']
    template_name='comment_edit.html'
    
    def get_success_url(self):
        pk=self.kwargs['post_pk']
        return reverse_lazy('post_detail',kwargs={'pk':pk})
    
    def test_func(self):
        comment=self.get_object()
        return self.request.user == comment.author
             
class ProfileView(View):
    def get(self,request,pk,*args, **kwargs):
        
        profile=UserProfile.objects.get(pk=pk)
        user=profile.user
        posts=Post.objects.filter(author=user).order_by('-created_on')
        
        followers=profile.followers.all()
        
        number_of_followers=len(followers)
        
        #does current logged in user follows you?
        isFollowing=False
        for follower in followers:
            if follower == request.user:
                isFollowing=True
        
        context={
            'user':user,
            'profile':profile,
            'posts':posts,
            'number_of_followers':number_of_followers,
            'isFollowing':isFollowing,
            
        }
        
        return render(request,'profile.html',context=context)
        

class ProfileEditView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=UserProfile
    fields=['name','bio','birth_date','location','picture']
    template_name='profile_edit.html'
    
    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse_lazy('profile',kwargs={'pk':pk})
    def test_func(self):
        profile=self.get_object()
        return self.request.user== profile.user
    
    
class AddFollower(LoginRequiredMixin,View):
    def post(self,request,pk,*args, **kwargs):
        profile=UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)
        
        return redirect('profile',pk=profile.pk)
        
class RemoveFollower(LoginRequiredMixin,View):
    def post(self,request,pk, *args, **kwargs):
        profile=UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        
        return redirect('profile',pk=profile.pk)


class UserSearch(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        query=self.request.GET.get("query")
        profileList=UserProfile.objects.filter(
            Q(user__username__icontains=query)
        )
        
        context={
            'profileList':profileList
        }
        return render(request,'search.html',context)