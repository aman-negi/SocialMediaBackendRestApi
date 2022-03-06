from sys import get_asyncgen_hooks
from webbrowser import get
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
import jwt 
from datetime import datetime

from .models import User,Follow,Post,Like

# Login the user
class LoginView(APIView):
    
    def post(self,request):
        data=request.data
        
        email = data['email']
        password = data['password']
        try :
            user = User.objects.filter(email=email).first()
            if(user.password == password):
                payload = {
                    "id":user.id,
                }
                token = jwt.encode(payload,'secret',algorithm='HS256')
                # tokenValue = jwt.decode(token,'secret',algorithms=['HS256'])
                response = Response()
                response.set_cookie(key='jwt',value=token,httponly=True)
                response.data={
                    'jwt':token
                }
            else: 
                response = Response()
                response.data = {
                    'error' : "Authentication Failed"
                }
        except:
                response = Response()
                response.data = {
                    'error' : "Authentication Failed"
                }
        return response
    

class FollowUserView(APIView):
    def post(self,request,pk):
        token = request.COOKIES.get('jwt')
        response = Response()
        if not token:
            response.data = {
                'error' : "Unauthenticated"
            }
            return response
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except:
            response.data = {
                'error' : "Unauthenticated"
            }
            return response
        try:
            user = User.objects.filter(id = payload['id']).first()
            follow = User.objects.filter(id = pk).first()
            
        except:
            response.data = {
                'error' : "User doesn't exist"
            }
            return response
        try:
            currentUser = Follow.objects.get(user = user)
        except:
            currentUser = Follow.objects.create(user = user)
        
        try:
            toFollowUser = Follow.objects.get(user = follow)
        except:
            toFollowUser = Follow.objects.create(user = follow)
        
        currentUser.following.add(follow)
        toFollowUser.followedBy.add(user)
        user.no_of_following +=  1
        follow.no_of_follower += 1
        
        currentUser.save()
        toFollowUser.save()
        user.save()
        follow.save()
        response.data = {
                'sucess' : f"User followed the user with id : {pk}"
            }
        return response


class UnfollowUserView(APIView):
    def post(self,request,pk):
        token = request.COOKIES.get('jwt')
        response = Response()
        if not token:
            response.data = {
                'error' : "Unauthenticated"
            }
            return response
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except:
            response.data = {
                'error' : "Unauthenticated"
            }
            return response
        try:
            user = User.objects.filter(id = payload['id']).first()
            follow = User.objects.filter(id = pk).first()
            
        except:
            response.data = {
                'error' : "User doesn't exist"
            }
            return response
        try:
            currentUser = Follow.objects.get(user = user)
        except:
            response.data = {
                'error' : f"User don't follow the user with id : {pk}"
            }
            return response
        
        try:
            toUnfollowUser = Follow.objects.get(user = follow)
        except:
            response.data = {
                'error' : f"User {pk} isn't being followed by the user"
            }
            return response
        
        currentUser.following.remove(follow)
        toUnfollowUser.followedBy.remove(user)
        user.no_of_following -=  1
        follow.no_of_follower -= 1
        
        currentUser.save()
        toUnfollowUser.save()
        user.save()
        follow.save()
        response.data = {
                'sucess' : f"User unfollowed the user with id : {pk}"
            }
        return response


class ProfileView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        response = Response()
        if not token:
            response.data = {
                'error' : "Unauthenticated"
            }
            return response
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except:
            response.data = {
                'error' : "Unauthenticated"
            }
            return response
        
        try:
            user = User.objects.filter(id = payload['id']).first()
        except:
            response.data = {
                'error' : "User doesn't exist"
            }
            return response
        
        response.data = {
            'UserName' : user.name,
            'No of Followers' : user.no_of_follower,
            'No of Following' : user.no_of_following
        }
        return response
    
class CreatePostView(APIView):
    def post(self,request):
        data=request.data
        token = request.COOKIES.get('jwt')
        response = Response()
        if not token:
            response.data = {
                'error' : "Unauthenticated"
            }
            return response
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except:
            response.data = {
                'error' : "Unauthenticated"
            }
            return response
        
        try:
            user = User.objects.filter(id = payload['id']).first()
        except:
            response.data = {
                'error' : "User doesn't exist"
            }
            return response
        
        createPost = Post.objects.create(user = user,title=data['Title'],description =data['Description'],created_time=datetime.now())
        response.data={
            'id' : createPost.id,
            'title' : createPost.title,
            'description' : createPost.description,
            'created_time' : createPost.created_time,
        }
        createPost.save()
        return response

    
class LikePostView(APIView):
    def post(self,request,pk):
        data=request.data
        token = request.COOKIES.get('jwt')
        response = Response()
        if not token:
            response.data = {
                'error' : "Unauthenticated"
            }
            return response
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except:
            response.data = {
                'error' : "Unauthenticated"
            }
            return response
        
        try:
            user = User.objects.filter(id = payload['id']).first()
        except:
            response.data = {
                'error' : "User doesn't exist"
            }
            return response
        
        try: 
            getpost = Post.objects.filter(id = pk).first()
        except:
            response.data = {
                'error' : "Post doesn't exist"
            }
            return response

        try: 
            toLike = Like.objects.filter(post = getpost).first()
        except:
            toLike = Like.objects.create(post = getpost)
        
        getpost.number_of_likes += 1
        toLike.likedBy.add(user)
        
        toLike.save()
        getpost.save()
        
        response.data = {
                'sucess' : f"User liked the post with id : {pk}"
            }
        return response
    
class UnlikePostView(APIView):
    def post(self,request,pk):
        data=request.data
        token = request.COOKIES.get('jwt')
        response = Response()
        if not token:
            response.data = {
                'error' : "Unauthenticated"
            }
            return response
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except:
            response.data = {
                'error' : "Unauthenticated"
            }
            return response
        
        try:
            user = User.objects.filter(id = payload['id']).first()
        except:
            response.data = {
                'error' : "User doesn't exist"
            }
            return response
        
        try: 
            getpost = Post.objects.filter(id = pk).first()
        except:
            response.data = {
                'error' : "Post doesn't exist"
            }
            return response

        try: 
            toLike = Like.objects.filter(post = getpost).first()
        except:
            response.data = {
                'error' : "User haven't liked the post"
            }
            return response

        try: 
            toLike.likedBy.remove(user)
        except:
            response.data = {
                'error' : "User haven't liked the post"
            }
            return response
        
        getpost.number_of_likes -= 1
        
        toLike.save()
        getpost.save()
        
        response.data = {
                'sucess' : f"User unliked the post with id : {pk}"
            }
        return response
    
    
    
class Comment(APIView):
    def post(self,request,pk):
        data=request.data
        token = request.COOKIES.get('jwt')
        response = Response()
        if not token:
            response.data = {
                'error' : "Unauthenticated"
            }
            return response
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except:
            response.data = {
                'error' : "Unauthenticated"
            }
            return response
        
        try:
            user = User.objects.filter(id = payload['id']).first()
        except:
            response.data = {
                'error' : "User unauthenticated or doesn't exist"
            }
            return response
        
        try: 
            getpost = Post.objects.filter(id = pk).first()
        except:
            response.data = {
                'error' : "Post doesn't exist"
            }
            return response
        
        createComment = Post.objects.create(user = user,post=getpost,comment_body =data['Comment'],created_time=datetime.now())
        getpost.number_of_comments += 1
        response.data={
            'id' : createComment.id,
        }
        createComment.save()
        return response


   
class GetPost(APIView):
    def post(self,request,pk):
        response = Response()
  
        try: 
            getpost = Post.objects.filter(id = pk).first()
        except:
            response.data = {
                'error' : "Post doesn't exist"
            }
            return response

        getpost.save()
        
        response.data = {
                'id' : getpost.id,
                'title' : getpost.title,
                'description' : getpost.description,
                'number_of_comments' : getpost.number_of_comments,
                'number_of_likes' : getpost.number_of_likes
            }
        return response
    
class GetAllPost(APIView):
    def post(self,request,pk):
        data=request.data
        token = request.COOKIES.get('jwt')
        response = Response()
        if not token:
            response.data = {
                'error' : "Unauthenticated"
            }
            return response
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except:
            response.data = {
                'error' : "Unauthenticated"
            }
            return response
        
        try:
            user = User.objects.filter(id = payload['id']).first()
        except:
            response.data = {
                'error' : "User doesn't exist"
            }
            return response
        
        try: 
            getpost = Post.objects.all().filter(user = user)
        except:
            response.data = {
                'error' : "No Post of the user"
            }
            return response
        
        response.data = {
            'data' : getpost
        }
        return response

class DeletePost(APIView):
    def post(self,request,pk):
        response = Response()
  
        try: 
            getpost = Post.objects.filter(id = pk).first()
        except:
            response.data = {
                'error' : "Post doesn't exist"
            }
            return response

        getpost.delete()
        
        response.data = {
                'success' :'successfully deleted the post'
            }
        return response