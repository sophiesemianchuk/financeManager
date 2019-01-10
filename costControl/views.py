from django.shortcuts import render, redirect,  get_object_or_404
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.db.models.deletion import ProtectedError
from django.db.models import Count, Sum
from .models import Category, Transaction, SELECT_OPERATION
from .forms import CategoryForm, TransactionForm, SignUpForm


def index(request):
    return render(request, 'index.html')


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


def get_user_object_or_404(model_class, request, pk):
    queryset = model_class.objects.filter(user=request.user)
    return get_object_or_404(queryset, pk=pk)


@login_required
def edit_category(request, pk):
    category = get_user_object_or_404(Category, request, pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('home')
        else:
            category.category = request.POST.get('category')
            category.description = request.POST.get('description')
            context = {
                'form': form,
                'category': category,
            }
            return render(request, 'create_category.html', context)
    else:
        context = {
            'category': category,
        }
    return render(request, 'create_category.html', context)


@login_required
def delete_category(request, pk):
    category = get_user_object_or_404(Category, request, pk)
    try:
        category.delete()
        messages.success(request, f'You can not delete this category.')
    except ProtectedError:
        messages.error(request, f'You can not delete this category.')
    return redirect('home')


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
def all_transactions(request):
    user = request.user
    categories_list = Category.objects.filter(user=user)
    category_transaction = request.GET.get('category')

    if category_transaction:
        if category_transaction == '0':
            transactions_list = Transaction.objects.filter(user=user)
        else:
            transactions_list = Transaction.objects.filter(user=user).filter(category=category_transaction)
    else:
        transactions_list = Transaction.objects.filter(user=user)
    context = {
        'transactions_list': transactions_list,
        'categories_list': categories_list,
        'category_transaction': category_transaction,
        'SELECT_OPERATION': SELECT_OPERATION,
    }
    return render(request, 'all_transactions.html', context)


@login_required
def edit_transaction(request, pk):
    transaction = get_user_object_or_404(Transaction, request, pk)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.save()
            return redirect('home')
        else:
            categories_list=Category.objects.filter(user=request.user)
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
        categories_list=Category.objects.filter(user=request.user)
        context = {
            'transaction': transaction,
            'categories_list': categories_list,
            'SELECT_OPERATION': SELECT_OPERATION,
        }
        return render(request, 'create_transaction.html', context)


@login_required
def delete_transaction(request, pk):
    transaction = get_user_object_or_404(Transaction, request, pk)
    try:
        transaction.delete()
        messages.success(request, f'You delete this category.')
    except ProtectedError:
        messages.error(request, f'You can not delete this category.')
    return redirect('home')


@login_required
def group_category(request):
    operation = request.POST.get('operation')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    categories_list = Transaction.objects.filter(user=request.user).filter(operation=operation).filter(date_operation__range=[start_date, end_date]).values('category__category').annotate(category_total=Sum('sum'))
    total_sum = Transaction.objects.filter(user=request.user).filter(operation=operation).filter(date_operation__range=[start_date, end_date]).aggregate(Sum('sum'))
    context = {
        'categories_list': categories_list,
        'start_date': start_date,
        'end_date': end_date,
        'total_sum': total_sum,
    }
    return render(request, 'group_category.html', context)


@login_required
def day_by_day(request):
    operation = request.POST.get('operation')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    transactions_list = Transaction.objects.filter(user=request.user).filter(operation=operation).filter(date_operation__range=[start_date, end_date]).order_by('date_operation')
    categories_list = Transaction.objects.filter(user=request.user).filter(operation=operation).filter(date_operation__range=[start_date, end_date]).values('category__category')
    context = {
        'transactions_list': transactions_list,
        'categories_list': categories_list,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'day_by_day.html', context)


@login_required
def report_generator(request):
    if request.method == 'POST':
        if '_group_category' in request.POST:
            return group_category(request)
        elif '_day_by_day' in request.POST:
            return day_by_day(request)
    else:
        context = {
            'SELECT_OPERATION': SELECT_OPERATION,
        }
        return render(request, 'report_generator.html', context)


@login_required
def log_out(request):
    logout(request)
    return render(request, 'log_out.html')

# Create your views here.
