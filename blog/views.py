from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
from django.contrib.auth.models import User
from .forms import PostForm, SignUpForm, ProfileForm, UserForm, CommentForm, ContactForm
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth import login


def home(request):
    posts = Post.objects.order_by('-date_published')
    #posts = Post.objects.filter(date_published__lte=timezone.now()).order_by('date_published')
    return render(request, 'blog/home.html', {'posts': posts})


def about(request):
    return render(request, 'blog/about.html', {})


def session_timeout_view(request):
    return render(request, 'blog/sessiontimeout.html', {})


def contact_view(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['X19122951@student.ncirl.ie'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, f'Success! Thank you for your message.')
            return redirect('contact')
    return render(request, 'blog/contact.html', {'form': form})


def blog_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post.html', {'post': post})


def post_author(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/author_profile.html', {'post': post})


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.date_published = timezone.now()
            post.save()
            messages.success(request, f'Your post was created successfully!')
            return redirect('blog-post', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("<h1>Permission denied!!</h1>")
    else:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                # post.published_date = timezone.now()
                post.save()
                messages.success(request, f'Your post was edited successfully!')
                return redirect('blog-post', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def blog_draft(request):
    posts = Post.objects.filter(date_published__isnull=True).order_by('date_created')
    return render(request, 'blog/drafts.html', {'posts': posts})


@login_required
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    messages.success(request, f'Your post was published successfully!')
    return redirect('blog-post', pk=pk)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("<h1>Permission denied</h1>")
    else:
        post.delete()
        messages.success(request, f'Your post was deleted successfully!')
        return redirect('blog-home')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.country = form.cleaned_data.get('country')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = f'Activate your {current_site} account.'
            message = render_to_string('blog/account_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(mail_subject, message)
            messages.success(request, f'Your account has been created, check your email to activate your account !')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, f'Thanks for verifying your email, your account is now active.')
        return redirect('blog-home')
    else:
        messages.success(request, f'Invalid verification link.')
        return redirect('blog-home')


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'blog/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment was successfully added')
            return redirect('blog-post', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})