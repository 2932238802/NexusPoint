import json 
from django.http import JsonResponse 
from django.shortcuts import render

def index(request):
    """
    应用首页
    """
    context = ''
    
    
    try:
        data = json.loads(request.body)
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON body'}, status=400)

    return render(request, 'Login/index.html', context)
