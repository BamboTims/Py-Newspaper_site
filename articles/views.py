from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from .models import Article


# Create your views here.
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_list.html"


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "article_detail.html"


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ("title", "body")
    template_name = "article_edit.html"

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(CreateView, LoginRequiredMixin):
    model = Article
    template_name = "article_new.html"
    fields = ("title", "body")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
