
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q, Avg
from django.views.generic import View, TemplateView, DetailView, ListView, CreateView, UpdateView, FormView
from django.views.generic.edit import DeleteView

from catalog.models import JobPost
from catalog.forms import JobPostRequestForm, JobPostForm



def home_view(request):
    current_time = timezone.now()

    qs = JobPost.objects.order_by('-created_at').distinct()

    if request.POST.get('job_name') or request.POST.get('company_name'):

        q1 = Q(title__icontains=request.POST.get('job_name'))
        q2 = Q(company__name__icontains=request.POST.get('company_name'))

        qs = qs.filter(q1 | q2)

    avg_salary = qs.aggregate(Avg('salary'))['salary__avg']

    context = {
        'current_time': current_time,
        'title' : 'Home Page',
        'welcome' : "<h1>Walcome</h1>",
        'jobs' : qs,
        'avg_salary' : int(str(avg_salary)[:4]),
        'form' : JobPostRequestForm(request.POST or None)
    }

    response = render(request, 'index.html', context=context)
    if request.GET.get('utm_source'):
        sources = request.COOKIES.get('utm_source')
        if sources:
            sources = sources.split(',')
            sources.append(request.GET.get('utm_source'))
            sources = ','.join(sources)
            response.set_cookie('utm_source', sources)
        else:
            response.set_cookie('utm_source', request.GET.get('utm_source'))

    return response



def jobpost_detail(request, pk):
    jobpost = JobPost.objects.get(pk=pk)
    context = {
        'jobpost': jobpost,
    }
    sources = request.COOKIES.get('utm_source')
    sources = sources.split(',')
    context['sources'] = sources
    return render(request, 'jobpost_detail.html', context=context)


class JobPostDetail(View):

    def get_object(self):
        return JobPost.objects.get(pk=self.kwargs['pk'])

    def get_sources(self):
        sources = self.request.COOKIES.get('utm_source')
        sources = sources.split(',')
        return sources

    def get(self, request, *args, **kwargs):
        context = {
            'jobpost': self.get_object(),
            'sources': self.get_sources(),
        }
        return render(request, 'jobpost_detail.html', context=context)


class AboutUs(TemplateView):
    template_name = 'about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About Us'
        return context


class JobPostGenericDetail(DetailView):
    model = JobPost
    template_name = 'jobpost_detail.html'

    def get_sources(self):
        sources = self.request.COOKIES.get('utm_source')
        sources = sources.split(',')
        return sources

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sources'] = self.get_sources() 
        return context


class JobPostList(ListView):
    model = JobPost
    template_name = 'jobpost_list.html'
    #queryset = JobPost.objects.filter(is_active=True)

    def get_queryset(self):
        types = {
            "0" : False,
            "1" : True,
        }
        qs = JobPost.objects.all()
        if self.request.GET.get('types'):
            qs = qs.filter(is_active=types.get(self.request.GET.get('types')))
        return qs

class JobPostCreate(CreateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'jobpost_create.html'

    def get_success_url(self):
        return resolve_url('jobposts')


class JobPostUpdate(UpdateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'jobpost_update.html'

    def get_success_url(self):
        return resolve_url('jobpost_detail', pk=self.kwargs['pk'])


class JobPostDelete(DeleteView):
    model = JobPost
    template_name = 'jobpost_delete.html'
    success_url = '/'

class JobPostRequest(FormView):
    form_class = JobPostRequestForm
    template_name = 'jobpost_create.html'
    
    def form_valid(self, form):
        if not form.errors:
            print(form.cleaned_data)
            return redirect('jobposts')
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))



def change_language(request):
    if request.GET.get('lang') == 'en' or request.GET.get('lang') == 'az':
        path_list = request.META.get('HTTP_REFERER').split('/')
        
        path_list[3] = request.GET.get('lang')
        path = '/'.join(path_list)
     
        response = HttpResponseRedirect(path)
        response.set_cookie('django_language', request.GET['lang'])
    return response