from django.shortcuts import render


def index(request):
    unknown_variables = ['a', 'b', 'c']
    message = f"please, change variables: {', '.join(unknown_variables)}"
    content = {
        'a': 'a',
        'b': 'b',
        'c': 'c',
        'message': message,
    }
    if request.POST:
        a = request.POST.get('a', None)
        b = request.POST.get('b', None)
        c = request.POST.get('c', None)
        if a:
            content['a'] = a
            unknown_variables.remove('a')
            content['message'] = f"please, change variables: {', '.join(unknown_variables)}"
        if b:
            content['b'] = b
            unknown_variables.remove('b')
            content['message'] = f"please, change variables: {', '.join(unknown_variables)}"
        if c:
            content['c'] = c
            unknown_variables.remove('c')
            content['message'] = f"please, change variables: {', '.join(unknown_variables)}"
        return render(request, 'index.html', content)
    return render(request, 'index.html', content)
