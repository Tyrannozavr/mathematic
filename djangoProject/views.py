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

def predict_color(request, train = False, answer = None):
    # print(request.session.get('number'))
    # request.session['first'] = True
    if request.session.get('first', False):
        request.session['blue'] = []
        request.session['green'] = []
        request.session['red'] = []
        request.session['probably_blue'] = [i for i in range(100)]
        request.session['probably_green'] = [i for i in range(100)]
        request.session['probably_red'] = [i for i in range(100)]
        all_colors = [0 for i in range(75)] #this is probability blue color
        all_colors.extend([1 for i in range(15)]) #this is probabiliey green color
        all_colors.extend([2 for i in range(10)]) #this is probability red color
        request.session['all_colors'] = all_colors
        request.session['first'] = False
        request.session['number_color'] = [[0, 1, 2] for i in range(1, 101)]
    if train:
        print('train', number, answer)
    # request.session['number_color'] = 1
    print('test', request.session['probably_blue'])
    number = int(request.session.get('number'))
    blue = request.session.get('blue')
    green = request.session.get('green')
    red = request.session.get('red')
    probably_blue = request.session.get('probably_blue')
    probably_green = request.session.get('brobably_green')
    probably_red = request.session.get('probably_red')
    all_color = request.session.get('all_colors')
    number_color = request.session.get('number_color')[number]
    answer = []
    for i in number_color:
        color_prob = 1 / len(probably_blue) * all_color.count(i)
        answer.extend([i for j in range(round(color_prob*100))])
    print(answer)
    # print(probably_red)
    return random.choice(['1', '2', '3'])

def box(request):
    message = ''
    if request.POST:
        if request.session.get('first', True):
            request.session['first'] = True
        new_number = request.POST.get('number')
        if new_number is not None:
            request.session['number'] = new_number

        message = f'You color is {predict_color(request)}?'
        answer = request.POST.get('answer', False)
        if answer:
            predict_color(request, train=True, answer=answer)
            message = ''
    return render(request, 'box.html', context={'message': message})
