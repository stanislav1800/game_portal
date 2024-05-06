from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Bulletin, Category, Profile, BulletinToCategory, Response
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from .forms import BulletinForm, ResponseForm
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives



# Create your views here.
class BulletinsList(ListView):
    model = Bulletin
    ordering = '-date'
    template_name = 'bulletins.html'
    context_object_name = 'bulletins'
    paginate_by = 10

class BulletinDetail(DetailView):
    model = Bulletin
    template_name = 'bulletin.html'
    context_object_name = 'bulletin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['response_form'] = ResponseForm()
        return context


class BulletinCreate(LoginRequiredMixin, CreateView):
    context_object_name = 'Bulletin'
    permission_required = 'bulletin_board.add_post'
    form_class = BulletinForm
    model = Bulletin
    template_name = 'bulletin_create.html'
    success_url = reverse_lazy('bulletin')

    def form_valid(self, form):
        bulletin = form.save(commit=False)
        user = self.request.user
        profile, created = Profile.objects.get_or_create(user=user)
        bulletin.author = profile
        bulletin.save()
        self.create_bulletin_categories(bulletin, form.cleaned_data['category'])
        return redirect('bulletins')

    def create_bulletin_categories(self, bulletin, categories):
        for category in categories:
            BulletinToCategory.objects.create(bulletin=bulletin, category=category)




class BulletinUpdate(LoginRequiredMixin, UpdateView):
    permission_required = 'bulletin_board.change_post'
    form_class = BulletinForm
    model = Bulletin
    template_name = 'bulletin_edit.html'
    success_url = reverse_lazy('bulletins')

    def form_valid(self, form):
        bulletin = form.save(commit=False)
        bulletin.save()
        BulletinToCategory.objects.filter(bulletin=bulletin).delete()
        for category in form.cleaned_data['category']:
            BulletinToCategory.objects.create(bulletin=bulletin, category=category)
        return redirect('bulletins')


class BulletinDelete(LoginRequiredMixin, DeleteView):
    permission_required = 'bulletin_board.delete_post'
    model = Bulletin
    template_name = 'bulletin_delete.html'
    success_url = reverse_lazy('bulletins')

class ResponseCreate(CreateView):
    model = Response
    form_class = ResponseForm
    template_name = 'bulletin.html'

    def form_valid(self, form):
        bulletin = Bulletin.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        profile, created = Profile.objects.get_or_create(user=user)

        # Проверяем, существует ли уже ответ данного пользователя на данное объявление
        if Response.objects.filter(bulletin=bulletin, author=profile).exists():
            return redirect('bulletin', pk=bulletin.pk)

        form.instance.author = profile
        form.instance.bulletin = bulletin
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('bulletin', kwargs={'pk': self.kwargs['pk']})



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

class ResponseListView(ListView):
    model = Response
    template_name = 'your_template.html'

    def get_queryset(self):
        author_id = self.kwargs.get('author_id')
        profile = get_object_or_404(Profile, id=author_id)
        bulletins = Bulletin.objects.filter(author=profile)
        accepted = self.request.GET.get('accepted', None)
        if accepted is not None:
            responses = Response.objects.filter(bulletin__in=bulletins, accepted=accepted)
        else:
            responses = Response.objects.filter(bulletin__in=bulletins)
        return responses

class ResponseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Response
    fields = ['accepted']
    template_name = 'response_update.html'

    def get_success_url(self):
        return reverse('author_response_list', args=[self.request.user.profile.id])

    def test_func(self):
        response = self.get_object()
        return response.bulletin.author.user == self.request.user

class ResponseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Response
    template_name = 'response_delete.html'

    def get_success_url(self):
        return reverse('author_response_list', args=[self.request.user.profile.id])

    def test_func(self):
        response = self.get_object()
        return response.bulletin.author.user == self.request.user

class CategoryListView(ListView):
    model = Bulletin
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Bulletin.objects.filter(category=self.category).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribed'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email =user.email
        subject = 'Здравствуйте! Вы подписались на категорию'
        message = f'Здравствуйте, вы подписались на {category.name}'
        html = render_to_string('subscribe.html',{'category': category, 'message': message})
        msg = EmailMultiAlternatives(subject=subject,
                                     body='',
                                     from_email='stasiklim18@yandex.ru',
                                     to=[email,],)
        msg.attach_alternative(html,'text/html')
        try:
            msg.send()
        except Exception as e:
            print(e)
        return redirect('bulletins')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
    return redirect('bulletins')