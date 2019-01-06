from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.db.models.deletion import ProtectedError
from django.db.models import Count
from .models import Category, Transaction, SELECT_OPERATION
from .forms import CategoryForm, TransactionForm, SignUpForm


def index(request):
    return render(request, 'base.html')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate( username=username, password=raw_password)
            login(request, user)
            return redirect('home')

    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


@login_required
def home(request):
    user = request.user
    categories_list = Category.objects.filter(user=user).annotate(transaction_count=Count('transaction')).order_by('-transaction_count')
    context = {
        'categories_list': categories_list,
    }
    return render(request, 'home.html', context)


@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('home')
        else:
            category = Category()
            category.category = request.POST.get('category')
            category.description = request.POST.get('description')
            context = {
                'form': form,
                'category': category,
            }
            return render(request, 'create_category.html', context)
    else:
        form = CategoryForm()
        context = {
            'form': form,
        }
        return render(request, 'create_category.html', context)


@login_required
def all_categories(request):
    user = request.user
    categories_list = Category.objects.filter(user=user)
    context = {
        'categories_list': categories_list,
    }
    return render(request, 'all_categories.html', context)


@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('home')
        else:
            categories_list=Category.objects.filter(user=request.user)
            transaction = Transaction()
            transaction.category = request.POST.get('category')
            transaction.operation = request.POST.get('operation')
            transaction.sum = request.POST.get('sum')
            transaction.date_operation = request.POST.get('date_operation')
            transaction.description = request.POST.get('description')
            context = {
                'form': form,
                'transaction': transaction,
                'categories_list': categories_list,
                'SELECT_OPERATION': SELECT_OPERATION,
            }
            return render(request, 'create_transaction.html', context)
    else:
        form = TransactionForm()
        categories_list=Category.objects.filter(user=request.user)
        context = {
            'form': form,
            'categories_list': categories_list,
            'SELECT_OPERATION': SELECT_OPERATION,
        }
    return render(request, 'create_transaction.html', context)

@login_required
def log_out(request):
    logout(request)
    return render(request, 'log_out.html')

# Create your views here.
