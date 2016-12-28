from django import forms

from .models import MultipleChoiceAnswer, TrueFalseAnswer, Quiz, Question,MultipleChoiceQuestion


class QuizForm(forms.ModelForm):
	class Meta:
		model = Quiz
		fields = ['title', 'instruction']



# MultiChoiceInlineAnswer = forms.inlineformset_factory(
# 	Question,
# 	MultipleChoiceQuestion,
# 	MultipleChoiceAnswer,
# 	fields=('correct', 'text'),
# 	max_num=4,
# 	extra=3,
# )


# class MultiChoiceInlineAnswer():


class MultipleAnswerForm(forms.ModelForm):
	class Meta:
		model = MultipleChoiceAnswer
		fields = ['correct', 'text']

class MultiChoiceQuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['text']

MultipleAnswerFormSet = forms.modelformset_factory(
	MultipleChoiceAnswer,
	form=MultipleAnswerForm,
	max_num=4
)



class TrueFalseQuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['text']

# MultipleAnswerFormSet = forms.modelformset_factory(
# 	MultipleChoiceAnswer,
# 	form=MultipleAnswerForm
# )

class TrueFalseAnswerForm(forms.ModelForm):
	class Meta:
		model = TrueFalseAnswer
		fields = ['correct',]

# TrueFalseAnswerFormSet = forms.modelformset_factory(
# 	TrueFalseAnswer,
# 	form=TrueFalseAnswerForm

# )