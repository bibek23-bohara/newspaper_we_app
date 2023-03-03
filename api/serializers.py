from django.contrib.auth.models import User, Group
from rest_framework import serializers
from newspaper_app.models import Tag, Category, Post, Comment


# convert to json string to dictionary and vice-versa


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id',
                   'username',
                   "first_name",
                   "last_name",
                   "email",
                   "groups",
                   "last_login",
                   "date_login",
                     ]
        

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [ "id" ,"name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [ "id" ,"name"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [ "id" ,"name"]



class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj).values()
        return comments

    class Meta:
        model = Post
        fields =["id",
                  "title",
                   'content',
                   "featured_image",
                   "views_count",
                   "status",
                   "published_at",
                   "category",
                   "tag",
                   "author",
                   "comments",
        ]
        extra_kwargs = {
            "published_at":{"read_only":True},
            "author":{"read_only":True},
            "views_count":{"read_only":True},
        }
    def validate(self, data):
        data["author"]= self.context["request"].user
        return data
        
