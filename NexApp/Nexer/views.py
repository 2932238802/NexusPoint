from django.shortcuts import render

# Create your views here.
def index(request):
    """
    应用首页
    """
    context = {
        'title': '我的应用首页',
        'welcome_message': '欢迎来到我的 Django 示例应用！',
        'year': 2023, 
    }

    return render(request, 'Nexer/index.html', context)
