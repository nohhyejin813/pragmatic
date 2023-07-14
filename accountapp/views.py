from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin

from accountapp.decorators import account_ownership_required
from accountapp.forms import AccountUpdateForm
from articleapp.models import Article

has_ownership = [account_ownership_required, login_required]  # 두개의 데코레이터를 한데 모아 배열로 만듬


# hello_worl 관련 설명은 README파일에서 확인하기

class AccountCreateView(CreateView):  # CRUD 중 C create
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('accountapp:login')  # reverse : 함수형 뷰, reverse_lazy : 클래스형 뷰
    template_name = 'accountapp/create.html'


class AccountDetailView(DetailView, MultipleObjectMixin):
    # CRUD 중에 Read부분. 단, Read가 아닌 detail로 사용. 조회이기 때문에 어떤 모델사용, 정보를 어떻게 시각화할 것인지에 대한 정보만 필요
    model = User
    context_object_name = 'target_user'
    '''
    user는 로그인한 사람 정보인데, 예를들어 인스타그램의 다른 사람 계정을 조회하려는 경우에는 내 정보가 아닌 해당 계정주의 정보를 
    보여줘야하므로, detail페이지에 {{ target_user.username }} 처럼 내정보가 아닌 타겟 유저의 정보를 조회하도록 지정함
    '''
    template_name = 'accountapp/detail.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        object_list = Article.objects.filter(writer=self.get_object())
        return super(AccountDetailView, self).get_context_data(object_list=object_list, **kwargs)


'''
**@method_decorator(has_ownership, 'get') : has_ownership이라는 배열로 묶음으로써 4줄을 2줄로 간단하게 작성 가능

@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post') #일반 function에 사용하는 데코레이터를 메서드에 사용할 수 있도록 변환하는 데코레이터
@method_decorator(account_ownership_required, 'get')
@method_decorator(account_ownership_required, 'post')
#decorators.py : 현재유저가 리퀘스트 유저가 맞는지 본인인증 하기위해 직접 만든 데코레이터. <and self.get_object() == self.request.user:> 이부분
'''


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountUpdateView(UpdateView):  # CRUD 중 U update
    model = User
    context_object_name = 'target_user'
    form_class = AccountUpdateForm
    success_url = reverse_lazy('accountapp:login')  # reverse : 함수형 뷰, reverse_lazy : 클래스형 뷰
    template_name = 'accountapp/update.html'

    '''
    @데코레이터가 대신한 부분들
     def get(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.get_object() == self.request.user:
            #self.request.user.is_authenticated and : 현재 request.user 로그인이 되어있고
            #self.get_object() : self는 updateview를 가리키며, .get_object()는 이 안에서 현재 사용되고 있는 user object의 pk값을 가져옴.
            #그 후에 == self.request.user : 현재 리퀘스트를 보낸 유저와 같은지를 확인함.
            return super().get(*args, **kwargs)
        else:
            return HttpResponseForbidden()

        # return HttpResponseRedirect(reverse('accountapp:login'))
        # 로그인이 되어있으면 기존의 방식으로 하되, 안되어있을 경우 로그인창으로 이동 시킴

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.get_object() == self.request.user:
            return super().post(*args, **kwargs)
        else:
            return HttpResponseForbidden()
    '''
    '''
    @method_decorator(login_required, 'get')
    @method_decorator(login_required, 'post')
    @method_decorator(account_ownership_required, 'get')
    @method_decorator(account_ownership_required, 'post')
    '''


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'
    '''
       def get(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.get_object() == self.request.user:
            return super().get(*args, **kwargs)
        else:
            return HttpResponseForbidden() 
        # 로그인이 되어있으면 기존의 방식으로 하되, 자신의 pk와 다른 pk에 접근 시, 금지된 곳에 접근했다는 페이지를 보여줌

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.get_object() == self.request.user:
            return super().post(*args, **kwargs)
        else:
            return HttpResponseForbidden()
    '''