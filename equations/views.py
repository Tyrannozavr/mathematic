from django.shortcuts import render, redirect


def solve(a, b, c):
    '''
    solve solves quadratic equation
    '''
    a, b, c = int(a), int(b), int(c)
    D = b ** 2 - 4 * a * c
    if D < 0:
        return '- has no solutions'
    elif D == 0:
        return f'= {-b / (2 * a)}'
    else:
        x1 = (-b - D ** (1 / 2)) / (2 * a)
        x2 = (-b + D ** (1 / 2)) / (2 * a)
        return f'= {x1} or {x2}'


def equations(request):
    '''
    responsible to storage values a, b and c, and call solve function after complete definition
    :param request:
    :return:
    '''
    a, b, c, = request.session.get('a', 'a'), request.session.get('b', 'b'), request.session.get('c', 'c')
    answer = ''
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
        return redirect('/equations')
    if len(unknown_variables) > 1:
        content['message'] = f"please, change variables: {', '.join(unknown_variables)}"
    elif unknown_variables[0] != 'full':
        content['message'] = f"please, change variable: {', '.join(unknown_variables)}"
    else:
        content['message'] = ''
    return render(request, 'equations/index.html', content)

