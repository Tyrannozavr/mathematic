from django.shortcuts import render, redirect
import random

# def predict(request):
#     return render(request, 'predicts/predict.html')

def initialize_variables(request):
    '''
    initialize variables session
    :param request:
    :return:
    '''
    request.session['blue'] = []
    request.session['green'] = []
    request.session['red'] = []
    request.session['probably_blue'] = [i for i in range(100)]
    request.session['probably_green'] = [i for i in range(100)]
    request.session['probably_red'] = [i for i in range(100)]
    all_colors = [0 for i in range(75)]  # this is probability blue color
    all_colors.extend([1 for i in range(15)])  # this is probabiliey green color
    all_colors.extend([2 for i in range(10)])  # this is probability red color
    request.session['all_colors'] = all_colors
    # request.session['first'] = False
    request.session['number_color'] = [[0, 1, 2] for i in range(1, 101)]

def predict_color(request, train=False, answer=None):
    '''
    :param request: transmints request for receive variables from session
    :param train: start the train of the alhoritm, allow to remember answers and chahge probability predicts
    :param answer: it's parameter for train alhoritm, yes or no, answer user to previous prediction
    :return: number color
    '''
    request.session.modified = True
    # if request.session.get('first', False):
    #     initialize_variables(request)

    if train:
        all_colors = request.session.get('all_colors')
        number = int(request.session.get('number'))
        previous_result = request.session.get('previous_result')
        if answer == 'yes':
            request.session['number_color'][number - 1] = [previous_result]
            if all_colors.count(previous_result) > 5:
                all_colors.remove(previous_result)
        else:
            if len(request.session.get('number_color')[number - 1]) > 1:
                # print('requirement: ', len(request.session.get('number_color')[number - 1]) > 1)
                try:
                    print('delete', number - 1, request.session.get('number_color')[number - 1])
                    request.session['number_color'][number - 1].remove(previous_result)
                    if len(request.session.get('number_color')) == 1:
                        if all_colors.count(previous_result) > 5:
                            all_colors.remove(previous_result)
                    print(request.session.get('number_color')[number - 1])
                except AttributeError:
                    print('it is color not found')
            else:
                print('only one option left')
        return redirect('/box')
    number = int(request.session.get('number'))
    probably_blue = request.session.get('probably_blue')        #contain number of elements, that art potentially may be blue
    probably_green = request.session.get('probably_green')      #it's the same, requrement to calculate probability
    probably_red = request.session.get('probably_red')          # and it
    all_color = request.session.get('all_colors')               #contain all available color
    number_color = request.session.get('number_color')[number - 1] #the colors that are available to the element
    result = []
    colors = {
        0: probably_blue,
        1: probably_green,
        2: probably_red
    }
    for i in number_color:
        color_prob = 1 / len(colors[i]) * all_color.count(i)
        result.extend([i for j in range(round(color_prob * 100))]) #result is list that contains colors count of with depends of probability
    predict = random.choice(result)
    request.session['previous_result'] = predict
    return predict


def predict(request):
    '''
    :param request:
    :return: html page with message, that contains color element
    also starts train
    '''
    message = ''
    accuracy = ''
    colors = {
        0: 'blue',
        1: 'green',
        2: 'red',
    }
    if request.session.get('first', True):
        # print(request.session.get('blue'))
        initialize_variables(request)
        request.session['first'] = False
        # print(request.session.get('blue'))
    if request.POST:
        # if request.session.get('first', True):
        #     print(request.session.get('first', True), 'initialize')
        #     print(request.session.get(''))
        #     request.session['first'] = True
        new_number = request.POST.get('number')
        if new_number == '':
            if request.session.get('number', False):
                return redirect('/box')
            else:
                new_number = request.session.get('number')
        else:
            if new_number is not None:
                new_number = int(new_number)
                request.session['number'] = new_number
            else:
                new_number = request.session.get('number')
        if new_number is not None:
            request.session['number'] = new_number
        answer = request.POST.get('answer', False)
        if answer:
            predict_color(request, train=True, answer=answer)
            message = ''
        else:
            if len(request.session.get('number_color')[new_number - 1]) == 1:
                accuracy = '1'
                message = f'The thing {new_number} is {colors[predict_color(request)]}'
            else:
                accuracy = ''
                message = f'The thing {new_number} is {colors[predict_color(request)]}?'
    return render(request, 'predicts/predict.html', context={'message': message, 'accuracy': accuracy})