from django.shortcuts import render

from rest_framework.response import Response

from rest_framework import generics

from notes.serialzers import UserSerializer,TaskSerializer

from notes.models import User,Task

from rest_framework import authentication,permissions

from notes.permissions import OwnerOnly

from rest_framework.views import APIView

from django.db.models import Count


class UserCreationView(generics.CreateAPIView):

    serializer_class=UserSerializer

class TaskCreateListView(generics.ListCreateAPIView):

    
    serializer_class=TaskSerializer

    queryset=Task.objects.all()

    # authentication_classes=[authentication.BasicAuthentication]   #this authentication used for basic authentication here we pass password and username


    authentication_classes=[authentication.TokenAuthentication]      #this authentication used for token_authentication  here we pass token

    permission_classes=[permissions.IsAuthenticated]

    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):

        qs = Task.objects.filter(owner=self.request.user) #to override to get entire task

        if "category" in self.request.query_params:

            category_value=self.request.query_params.get("category")

            qs=qs.filter(category=category_value)

        if "priority" in self.request.query_params:

            priority_value=self.request.query_params.get("priority")

            qs=qs.filter(priority=priority_value)



        return qs




    

class TaskRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):

    queryset=Task.objects.all()

    serializer_class=TaskSerializer

    # authentication_classes=[authentication.BasicAuthentication]  #this authentication used for basic authentication here we pass password and username


    authentication_classes=[authentication.TokenAuthentication]     #this authentication used for token_authentication  here we pass token

    permission_classes=[OwnerOnly]


class TaskSummaryApi(APIView):

    permission_classes=[permissions.IsAuthenticated]

    # authentication_classes=[authentication.BasicAuthentication] #this authentication used for basic authentication here we pass password and username

    authentication_classes=[authentication.TokenAuthentication]  #this authentication used for token_authentication  here we pass token

    def get(self,request,*args,**kwargs):

        qs=Task.objects.filter(owner=request.user)

        category_summary=qs.values("category").annotate(count=Count('category'))

        status_summary=qs.values("status").annotate(count=Count('status'))

        priority_summary=qs.values("priority").annotate(count=Count('priority'))

        task_count=qs.count()

        print(category_summary)

        context={
            "category_summary":category_summary,

            "status_summary":status_summary,

            "priority_summary":priority_summary,

            "total_count":task_count
        }

        return Response(data=context)
    

class CategoryListView(APIView):

    def get(self,request,*args,**kwargs):

        categories=Task.category_choices

        st={cat for tp in categories for cat in tp}

        return Response(data=st)


            
