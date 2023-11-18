from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic

from .models import Topic, TopicComment

from .forms import TopicCommentForm


class ForumListView(generic.ListView):
    model = Topic
    template_name = "topic/forum.html"


class TopicDetailView(generic.DetailView):
    model = Topic
    template_name = "topic/topic.html"

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        context['form'] = TopicCommentForm()
        context['comments'] = TopicComment.objects.filter(topic=slug)[::-1]
        return context

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        form = TopicCommentForm(request.POST)
        topic = get_object_or_404(Topic, slug=slug)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.topic = topic.slug
            form.save()
            redirect_url = reverse('topic-detail', kwargs={'slug': slug})
            return redirect(redirect_url)
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
