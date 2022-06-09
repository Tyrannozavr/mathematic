import random

from django.shortcuts import render, redirect

def solve(a, b, c):
    a, b, c = int(a), int(b), int(c)
    D = b**2 - 4 * a * c
    if D < 0:
        return '- has no solutions'
    elif D == 0:
        return f'= {-b / (2 * a)}'
    else:
        x1 = (-b - D**(1/2)) / (2 * a)
        x2 = (-b + D**(1/2)) / (2 * a)
        return f'= {x1} or {x2}'

def index(request):
    # request.session.modified = True
    a, b, c, = request.session.get('a', 'a'), request.session.get('b', 'b'), request.session.get('c', 'c')
    answer = ''
    # if request.session['variables']:
    if request.session.get('variables', False):
        unknown_variables = request.session.get('variables')
    else:
        unknown_variables = ['a', 'b', 'c']
        request.session['variables'] = ['a', 'b', 'c']
    if unknown_variables[0] == 'full':
        answer = solve(a, b, c)
        message = ''
    else:
        message = f"please, change variables: {', '.join(unknown_variables)}"
    content = {
        'a': a,
        'b': b,
        'c': c,
        'message': message,
        'answer': answer}
    if request.POST:
        a = request.POST.get('a', None)
        b = request.POST.get('b', None)
        c = request.POST.get('c', None)
        if a:
            request.session['a'] = a
            try:
                unknown_variables.remove('a')
            except ValueError:
                print('remove a')
        if b:
            request.session['b'] = b
            try:
                unknown_variables.remove('b')
            except ValueError:
                print('remove b')
        if c:
            request.session['c'] = c
            try:
                unknown_variables.remove('c')
            except ValueError:
                print('remove c')

        if len(request.session.get('variables')) == 0:
            request.session['variables'] = ['full']
        return redirect('/')
    if len(unknown_variables) > 1:
        content['message'] = f"please, change variables: {', '.join(unknown_variables)}"
    elif unknown_variables[0] != 'full':
        content['message'] = f"please, change variable: {', '.join(unknown_variables)}"
    else:
        content['message'] = ''
    # request.session['variables'] = request.session['variables']
    return render(request, 'index.html', content)

def clear(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return redirect('/')

def predict_color(number):
    blue = 0
    green = 0
    red = 0
    return random.choice(['1', '2', '3'])

def box(request):
    message = ''
    if request.POST:
        number = request.POST.get('number')
        message = f'You color is {predict_color(number)}?'
        print(number)
        if request.POST.get('answer'):
            message = ''
    return render(request, 'box.html', context={'message': message})
