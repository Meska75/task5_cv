from django.shortcuts import get_object_or_404, render

from .models import (
    Certificate,
    Experience,
    Profile,
    Project,
    SkillCategory,
    SocialLink,
)


def index_view(request):
    context = {
        'profile': Profile.objects.first(),
        'skill_categories': SkillCategory.objects.prefetch_related('skills').all(),
        'projects': Project.objects.prefetch_related('skills').all(),
        'experiences': Experience.objects.all(),
        'certificates': Certificate.objects.all(),
        'social_links': SocialLink.objects.all(),
    }
    return render(request, 'website/index.html', context)


def project_detail_view(request, slug):
    project = get_object_or_404(Project.objects.prefetch_related('skills'), slug=slug)
    return render(request, 'website/project_detail.html', {
        'project': project,
        'profile': Profile.objects.first(),
    })

def ai_chat_view (request):
    ai_chat_view = {'name': 'محمد اسکندرلو' , 'phone_number' : '+989337315709' , 'email': 'mohammad.eska34@gmail.com'}
    return render(request , 'website/ai_chat_view.html',ai_chat_view)

def decoy_admin_view (request):
    # Friendly decoy for the old /admin/ path. The real admin lives elsewhere.
    return render(request , 'website/decoy_admin.html')