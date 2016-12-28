from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


# Create your models here.

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='quiz_by')
    instruction = models.TextField()
    duration = models.TimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
    	verbose_name_plural = "Quizzes"

    def get_absolute_url(self):
        pass


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='question')
    text = models.TextField()
    # image = models.ImageField(upload_to='quiz_img')
    content_type = models.ForeignKey(ContentType,
                                     related_name='question_type',
                                     limit_choices_to={'model__in': (
                                         'truefalsequestion',
                                         'multiplechoicequestion')})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.text[:50]


class TrueFalseQuestion(models.Model):
    choice = models.CharField(max_length=255, default='truefalse')

    def __str__(self):
    	return 'truefalse {}'.format(self.id)

    def render(self):
    	template_name = 'quiz/quiz_type/true_false.html'
    	return mark_safe(render_to_string(template_name, {'items':self.truefalse}))


class MultipleChoiceQuestion(models.Model):
    choice = models.CharField(max_length=255, default='multiplechoice')

    def __str__(self):
    	return 'multiplechoice {}'.format(self.id)

    def render(self):
    	template_name = 'quiz/quiz_type/multiple_choice.html'
    	return mark_safe(render_to_string(template_name, {'items':self.multiplechoice}))


class MultipleChoiceAnswer(models.Model):
    question = models.ForeignKey(MultipleChoiceQuestion, related_name='multiplechoice')
    correct = models.BooleanField(default=False)
    text = models.CharField(max_length=255)


class TrueFalseAnswer(models.Model):
    question = models.ForeignKey(TrueFalseQuestion, related_name='truefalse')
    correct = models.BooleanField(default=False)
