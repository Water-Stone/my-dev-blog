from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import Article, Comment, HashTag
from .forms import ArticleForm, CommentForm, HashTagForm


class Index(View):
    def get(self, request):
        articles = Article.objects.all()
        context = {
            "articles": articles,
            "title": "Articles List"
        }
        return render(request, 'articles/list.html', context)


class Write(LoginRequiredMixin, View):
    def get(self, request):
        form = ArticleForm()
        context = {
            'form': form,
            "title": "Article Write"
        }
        return render(request, 'articles/write.html', context)
    
    def post(self, request):
        form = ArticleForm(request.POST, request.FILES)
        
        if form.is_valid():
            article = form.save(commit=False)
            article.writer = request.user
            article.save()
            return redirect('articles:list')
        
        context = {
            'form': form
        }
        
        return render(request, 'articles/write.html', context)


class Update(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(initial={'title': article.title, 'content': article.content})
        context = {
            'form': form,
            'article': article,
            "title": "Edit"
        }
        return render(request, 'articles/edit.html', context)
    
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(request.POST)
        
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.content = form.cleaned_data['content']
            article.save()
            return redirect('articles:detail', pk=pk)
        
        context = {
            'form': form,
            "title": "Blog"
        }
        
        return render(request, 'articles/edit.html', context)
        

class Delete(View):
    def post(self, request, pk):
        post = get_object_or_404(Article, pk=pk)
        post.delete()
        return redirect('articles:list')


class DetailView(View):
    def get(self, request, pk):
        article = Article.objects.prefetch_related('comment_set', 'hashtag_set').get(pk=pk)
        
        comments = article.comment_set.all()
        hashtags = article.hashtag_set.all()

        comment_form = CommentForm()
        hashtag_form = HashTagForm()
        
        context = {
            "title": "Article",
            'article_id': pk,
            'article_title': article.title,
            'article_writer': article.writer,
            'article_content': article.content,
            'article_img_url' : article.img.url,
            'article_created_at': article.created_at,
            'comments': comments,
            'hashtags': hashtags,
            'comment_form': comment_form,
            'hashtag_form': hashtag_form,
        }
        
        return render(request, 'articles/detail.html', context)


### Comment
class CommentWrite(LoginRequiredMixin, View):
    def post(self, request, pk):
        form = CommentForm(request.POST)
        article = get_object_or_404(Article, pk=pk)

        if form.is_valid():
            content = form.cleaned_data['content']
            writer = request.user

            try:
                comment = Comment.objects.create(article=article, content=content, writer=writer)
            except ObjectDoesNotExist as e:
                print('Post does not exist.', str(e))
            except ValidationError as e:
                print('Valdation error occurred', str(e))
            
            return redirect('articles:detail', pk=pk)
        
        hashtag_form = HashTagForm()
        
        context = {
            "title": "Blog",
            'article_id': pk,
            'comments': article.comment_set.all(),
            'hashtags': article.hashtag_set.all(),
            'comment_form': form,
            'hashtag_form': hashtag_form
        }
        return render(request, 'articles/detail.html', context)


class CommentDelete(View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        
        article_id = comment.article.id

        comment.delete()
        
        return redirect('articles:detail', pk=article_id)


### Tag
class HashTagWrite(LoginRequiredMixin, View):
    def post(self, request, pk):
        form = HashTagForm(request.POST)
        
        article = get_object_or_404(Article, pk=pk)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            writer = request.user

            try:
                hashtag = HashTag.objects.create(article=article, name=name, writer=writer)
            except ObjectDoesNotExist as e:
                print('Article does not exist.', str(e))
            except ValidationError as e:
                print('Valdation error occurred', str(e))

            return redirect('articles:detail', pk=pk)

        comment_form = CommentForm()
        
        context = {
            'title': 'Article',
            'article': article,
            'comments': article.comment_set.all(),
            'hashtags': article.hashtag_set.all(),
            'comment_form': comment_form,
            'hashtag_form': form
        }
        
        return render(request, 'articles/detail.html', context)


class HashTagDelete(View):
    def post(self, request, pk):
        hashtag = get_object_or_404(HashTag, pk=pk)
        article_id = hashtag.article.id

        hashtag.delete()
        
        return redirect('articles:detail', pk=article_id)