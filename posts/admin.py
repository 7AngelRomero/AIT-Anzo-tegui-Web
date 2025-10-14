from django.contrib import admin
from .models import Poll, Question, Choice, Response, Answer

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    inlines = [ChoiceInline]

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'is_active', 'has_image', 'image_preview']
    list_filter = ['is_active', 'created_at']
    inlines = [QuestionInline]
    fields = ['title', 'description', 'image', 'image_preview', 'is_active']
    readonly_fields = ['image_preview']
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Tiene Imagen'
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-width: 200px; max-height: 150px; border-radius: 8px;"/>'
        return 'Sin imagen'
    image_preview.allow_tags = True
    image_preview.short_description = 'Vista Previa'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'poll', 'question_type']
    list_filter = ['question_type']
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'question']

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['poll', 'user_ip', 'submitted_at']
    list_filter = ['submitted_at', 'poll']
    search_fields = ['poll__title']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['response', 'question', 'choice', 'text_answer']
    list_filter = ['response__submitted_at', 'response__poll']
    search_fields = ['response__poll__title', 'question__text']