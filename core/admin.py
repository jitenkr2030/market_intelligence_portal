from django.contrib import admin
from .models import *
admin.site.register([Organization,Membership,ResearchItem,ResearchProject,Survey,SurveyQuestion,SurveyResponse,DataSource,Alert,Notification,Report,Conversation,ChatMessage,Subscription])
