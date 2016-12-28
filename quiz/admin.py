from django.contrib import admin
from .models import ( Quiz, Question, TrueFalseQuestion, 
					MultipleChoiceQuestion, MultipleChoiceAnswer, TrueFalseAnswer, )

# Register your models here.

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
	list_display = ['title', 'created', 'duration', 'user']
	list_filter = ['created']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ['quiz', 'text']


class TrueFalseInline(admin.StackedInline):
	model = TrueFalseAnswer


@admin.register(TrueFalseQuestion)
class TrueFalseAdmin(admin.ModelAdmin):
	# list_display = 
	inlines = [TrueFalseInline]


class MultipleChoiceInline(admin.StackedInline):
	model = MultipleChoiceAnswer


@admin.register(MultipleChoiceQuestion)
class MultipleChoiceAdmin(admin.ModelAdmin):
	# list_display = 
	inlines = [MultipleChoiceInline]
