from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .forms import CategorySubscriptionForm
from posts.models import Category, UserCategorySubscription
from django.http import JsonResponse, HttpResponse


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'author').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        premium_group.user_set.add(user)
    return redirect(reverse('profile'))


class SubscriptionView(LoginRequiredMixin, TemplateView):
    form_class = CategorySubscriptionForm  
    template_name = 'profile/partial_subscription_form.html'

    def get(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            categories = [(category.id, category.name) for category in Category.objects.all()]
            form = self.form_class(categories=categories)
            return render(request, 'profile/partial_subscription_form.html', {'form': form})
        return HttpResponse(status=404)

    def post(self, request):
        if request.method == 'POST':
            categories = [(category.id, category.name) for category in Category.objects.all()]
            form = self.form_class(request.POST, categories=categories)
            if form.is_valid():
                category_id = form.cleaned_data['category']
                user = request.user  

                if not UserCategorySubscription.objects.filter(user=user, category_id=category_id).exists():
                    subscription = UserCategorySubscription(user=user, category_id=category_id)
                    subscription.save()
                    return JsonResponse({'success': True, 'message': 'Вы успешно подписались.'})
                else:
                    return JsonResponse({'success': False, 'message': 'Вы уже подписаны на эту категорию.'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})

 