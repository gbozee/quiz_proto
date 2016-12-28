from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse

from .models import (Quiz, Question,
                     TrueFalseQuestion,
                     MultipleChoiceQuestion,
                     MultipleChoiceAnswer,
                     TrueFalseAnswer)
from .forms import (MultipleAnswerForm, MultipleAnswerFormSet,
                    TrueFalseAnswerForm,
                    QuizForm, MultiChoiceQuestionForm,
                    TrueFalseQuestionForm)
# Create your views here.


def index(request):
    quizzes = Quiz.objects.all()

    return render(request, 'quiz/list.html', {'quizzes': quizzes})


def quiz_detail(request, quiz_id=None):
    # store both questions id and answer
    answers = {}
    # store all attempted question
    all_questions = []

    # check if quiz id is set else redirect
    if quiz_id:
        quiz = get_object_or_404(Quiz, id=quiz_id)
    elif request.method == 'POST':
        # set quiz id from post data
        c_quiz_id = int(request.POST['q1'])
        quiz = get_object_or_404(Quiz, id=c_quiz_id)
    else:
        pass
        # redirect to home

    # used to compile correct answers
    for que in quiz.question.all():
        # store up question id
        all_questions.append(que.id)

        # check if question is true or false
        if que.content_object.choice == 'truefalse':
            for m in que.content_object.truefalse.all():
                answers[que.id] = str(m.correct)
        elif que.content_object.choice == 'multiplechoice':
            for t in que.content_object.multiplechoice.all():
                if t.correct == True:
                    answers[que.id] = t.text
    print(answers)
    # print(all_questions)

    # if form is posted do question validation
    if request.method == 'POST':
        score = 0
        user_value = request.POST.dict()

        # extra quiz id and csrf from post result
        del user_value['q1']
        del user_value['csrfmiddlewaretoken']
        user_value = {int(key): str(value)
                      for key, value in user_value.items()}
        print(user_value)
        for user_value_key, user_value_data in user_value.items():
            for answer_key, answer_data in answers.items():
                print(user_value_key, user_value_data, answer_data, answer_key)
                if user_value_key == answer_key and user_value_data == answer_data:
                    score += 1
                    break

        print('Your Score is ', score)

        return render(request, 'quiz/result.html', {'score': score})

        # form = request.POST('')
    return render(request, 'quiz/detail.html', {'quiz': quiz})


def create_quiz(request):
    form_class = QuizForm()

    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            if 'addmultichoice' in request.POST:
                return redirect('create_question', quiz_id=form.id, que_type='mc')

            if 'addtruefalse' in request.POST:
                return redirect('create_question', quiz_id=form.id, que_type='tf')

            print(request.POST)
            return redirect(reverse('index'))
        # return render(request, '')
    return render(request, 'quiz/create_quiz.html', {'form': form_class})


def create_question(request, quiz_id, que_type):
    # the question type must be first
    # then use the question type id and it content type to create the question
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if que_type == 'mc':
        que_form_class = MultiChoiceQuestionForm()
        ans_form_class = MultipleAnswerFormSet()
    else:
        que_form_class = TrueFalseQuestionForm()
        ans_form_class = TrueFalseAnswerForm()

    if request.method == 'POST':
        if que_type == 'mc':
            que_form_class = MultiChoiceQuestionForm(data=request.POST)
            ans_form_class = MultipleAnswerFormSet(data=request.POST)
        else:
            que_form_class = TrueFalseQuestionForm(data=request.POST)
            ans_form_class = TrueFalseAnswerForm(data=request.POST)
        if que_form_class.is_valid() and ans_form_class.is_valid():
            que_form = que_form_class.save(commit=False)
            ans_form = ans_form_class.save(commit=False)

            if quiz_id:
				# you just created a form what are you doing withit 
                if que_type == 'mc':
                    form_class = MultiChoiceQuestionForm
                else:
                    form_class = TrueFalseQuestionForm
            else:
                form.user = request.user
                form = QuizForm(request.POST)
                import pdb
                pdb.set_trace()
                if form.is_valid():
                    form.save()

            # print(request.POST)
            # return redirect(reverse('index'))
        # return render(request, '')
    return render(request, 'quiz/create_question.html', {'que_form': que_form_class,
                                                         'ans_form': ans_form_class})
