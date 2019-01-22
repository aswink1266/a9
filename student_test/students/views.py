from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import Test, Question, TestAttempt
from django.urls import reverse_lazy, reverse


class TestList(generic.ListView):
    """
    View for showing the list of test available
    """
    model = Test
    template_name = 'students/test-list.html'
    context_object_name = 'tests'
    queryset = Test.objects.all().order_by('-published_on').select_related('user')


class CreateTest(LoginRequiredMixin, generic.CreateView):
    """
    View for creating new tests.
    """
    model = Test
    fields = ('test_name',)
    template_name = 'students/create-test.html'
    success_url = reverse_lazy('students:test_list')

    def form_valid(self, form):
        """
        Function for overriding the form and saving it.
        :param form: saving a new test object.
        :return: returns to the success page.
        """
        test = form.save(commit=False)
        test.user = self.request.user
        test.save()
        return redirect(self.success_url)


class CreateQuestion(LoginRequiredMixin, generic.CreateView, generic.ListView):
    """
    View for creating the questions in a test.
    """
    model = Question
    fields = ('question', 'answer', 'choice_1', 'choice_2', 'choice_3')
    template_name = 'students/add-question.html'
    context_object_name = 'questions'

    def form_valid(self, form):
        """
        Function for overriding the form and saving it.
        :param form: Saving the question and choices in a test.
        :return: Returns to the success page.
        """
        question = form.save(commit=False)
        test_id = self.kwargs['pk']
        test = Test.objects.get(id=test_id)
        if test.user == self.request.user:
            question.test = test
            question.save()
        return redirect(reverse('students:create_question', kwargs={'pk': test_id}))


class DeleteTest(LoginRequiredMixin, generic.DeleteView):
    """
    View for deleting a test.
    """
    model = Test
    template_name = 'students/delete-TestOrQuestion.html'
    success_url = reverse_lazy('students:test_list')


class TestDetail(generic.DetailView):
    """
    Showing the details of a test in a detail view, which shows both questions and choices
    """
    model = Test
    template_name = 'students/test-detail.html'
    context_object_name = 'test'
    queryset = Test.objects.all().order_by('-published_on').select_related('user')


class DeleteQuestion(generic.DeleteView):
    """
    View for deleting a question in a test
    """
    model = Question
    template_name = 'students/delete-TestOrQuestion.html'
    success_url = reverse_lazy('students:test_list')


class ExamAttemptView(LoginRequiredMixin, generic.View):
    """
    class based view for a student when student attempt a test.
    """
    context_object_name = 'attempt'

    def get(self, request, test_id):
        """
        Function for getting the data from a particular test
        :param request: Request for getting the data
        :param test_id: The id which is passed in the url for getting the data from a particular test
        :return: Either returns to the page showing the question just after starting the exam or
         showing the result of test if user tries to attempt the test again
        """
        test = get_object_or_404(Test, id=test_id)

        test_attempt, created = TestAttempt.objects.get_or_create(test=test, user=request.user)

        if created:
            questions = test.question_set.all().values_list('id', flat=True)
            request.session['questions'] = list(questions)
            questions = request.session['questions']
            current_question_id = questions.pop()
            request.session['current_question'] = current_question_id
            current_question = Question.objects.get(id=current_question_id)
        else:
            if test_attempt.is_active is False:
                return render(request, 'students/result.html', {'marks': test_attempt.marks})
            questions = request.session['questions']
            current_question = Question.objects.get(id=request.session['current_question'])

        return render(request, 'students/exam-attempt.html', {
            'question': current_question,
        })

    def post(self, request, test_id):
        """
        Function for submitting the answer of the question
        :param request: Request for posting the data
        :param test_id: The id which is passed in the url for getting the data from a particular test
        :return: Either returns to the success page after just completing the exam or
         showing the result of test if user tries to attempt the test again
        """
        test = get_object_or_404(Test, id=test_id)
        test_attempt = TestAttempt.objects.get(test=test, user=request.user)
        questions = request.session['questions']
        current_question = Question.objects.get(id=request.session['current_question'])
        answer = request.POST.get('answer')

        if answer == current_question.answer:
            test_attempt.marks = test_attempt.marks + 2
            test_attempt.save()
        else:
            test_attempt.marks = test_attempt.marks - 1
            test_attempt.save()

        if not questions:
            test_attempt.is_active = False
            test_attempt.save()
            return render(request, 'students/result.html', {'marks': test_attempt.marks})

        next_question_id = questions.pop()
        next_question = Question.objects.get(id=next_question_id)
        request.session['questions'] = questions
        request.session['current_question'] = next_question_id
        return render(request, 'students/exam-attempt.html', {
            'question': next_question,
        })


class PerformanceDetails(generic.ListView):
    """
    view for showing a student their performance details of the tests they have attempted.
    """
    model = TestAttempt
    template_name = 'students/performance_details.html'
    context_object_name = 'test_attempt'

    def get_queryset(self):
        """
        to get list of data of a particular user.
        :return: returns the list of data
        """
        queryset = TestAttempt.objects.filter(user=self.request.user).select_related('user', 'test')

        return queryset
