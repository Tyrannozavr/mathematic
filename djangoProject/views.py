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
    request.session.modified = True
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
        all_colors = request.session.get('all_colors')
        number = int(request.session.get('number'))
        previous_result = request.session.get('previous_result')
        print('train', answer, number, previous_result)
        if answer == 'yes':
            request.session['number_color'][number-1] = [previous_result]
            if all_colors.count(previous_result) > 5:
                all_colors.remove(previous_result)
        else:
            if len(request.session.get('number_color')[number-1]) > 1:
                print('requirement: ', len(request.session.get('number_color')[number-1]) > 1)
                try:
                    print('delete', number-1, request.session.get('number_color')[number-1])
                    request.session['number_color'][number-1].remove(previous_result)
                    if len(request.session.get('number_color')) == 1:
                        if all_colors.count(previous_result) > 5:
                            all_colors.remove(previous_result)
                    print(request.session.get('number_color')[number-1])
                except AttributeError:
                    print('it is color not found')
            else:
                print('only one option left')
        return redirect('/box')
    # request.session['number_color'] = 1
    # print('test', request.session['probably_blue'])
    number = int(request.session.get('number'))
    # blue = request.session.get('blue')
    # green = request.session.get('green')
    # red = request.session.get('red')
    probably_blue = request.session.get('probably_blue')
    probably_green = request.session.get('probably_green')
    probably_red = request.session.get('probably_red')
    all_color = request.session.get('all_colors')
    # request.session['number_color'][0] = [0, 1, 2]
    number_color = request.session.get('number_color')[number-1]
    result = []
    colors = {
        0: probably_blue,
        1: probably_green,
        2: probably_red
    }
    for i in number_color:
        color_prob = 1 / len(colors[i]) * all_color.count(i)
        result.extend([i for j in range(round(color_prob*100))])
    print('number', number, 'variants: ', number_color)
    # print(result.count(0), result.count(1), result.count(2))
    predict = random.choice(result)
    request.session['previous_result'] = predict
    # print(all_color.count(0))
    return predict

def box(request):
    message = ''
    accuracy = ''
    colors = {
        0: 'blue',
        1: 'green',
        2: 'red',
    }
    if request.POST:
        if request.session.get('first', True):
            request.session['first'] = True
        # print(request.POST.get('number'))
        new_number = request.POST.get('number')
        if new_number == '':
            print('zero')
            if request.session.get('number', False):
                return redirect('/box')
            # elif not request.session.get('number'):
            #     print('not')
            #     return redirect('box')
            else:
                new_number = request.session.get('number')
        else:
            print('post', request.POST)
            new_number = request.session.get('number')
            # new_number = int(new_number)
        # if new_number:
        #     new_number = int(new_number)
        # else:
        #     return redirect('/box')
        if new_number is not None:
            request.session['number'] = new_number
        answer = request.POST.get('answer', False)
        print('answer', answer)
        if answer:
            predict_color(request, train=True, answer=answer)
            message = ''
        else:
            if len(request.session.get('number_color')[new_number-1]) == 1:
                accuracy = '1'
                message = f'The thing {new_number} is {colors[predict_color(request)]}'
            else:
                accuracy = ''
                message = f'The thing {new_number} is {colors[predict_color(request)]}?'
    return render(request, 'box.html', context={'message': message, 'accuracy': accuracy})
