from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .modules import MODULES
class Organization(models.Model):
 name=models.CharField(max_length=180); slug=models.SlugField(unique=True); website=models.URLField(blank=True); industry=models.CharField(max_length=120,blank=True); created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self): return self.name
class Membership(models.Model):
 ROLES=[("owner","Owner"),("admin","Administrator"),("analyst","Research Analyst"),("editor","Editor"),("viewer","Viewer")]
 organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name="memberships"); user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="memberships"); role=models.CharField(max_length=20,choices=ROLES,default="analyst")
 class Meta: unique_together=("organization","user")
class ResearchItem(models.Model):
 MODULES=[(k,v) for k,v in MODULES.items()]; STATUSES=[("draft","Draft"),("active","Active"),("review","In review"),("completed","Completed"),("archived","Archived")]
 organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name="items"); module=models.CharField(max_length=30,choices=MODULES,db_index=True); title=models.CharField(max_length=240); summary=models.TextField(blank=True); status=models.CharField(max_length=20,choices=STATUSES,default="active"); category=models.CharField(max_length=140,blank=True); geography=models.CharField(max_length=140,blank=True); source_name=models.CharField(max_length=180,blank=True); source_url=models.URLField(blank=True); value=models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True); unit=models.CharField(max_length=50,blank=True); score=models.PositiveSmallIntegerField(default=0); tags=models.CharField(max_length=400,blank=True); data=models.JSONField(default=dict,blank=True); owner=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
 class Meta: ordering=["-updated_at"]
 def __str__(self): return self.title
class ResearchProject(models.Model):
 STATUSES=[("planned","Planned"),("in_progress","In progress"),("on_hold","On hold"),("completed","Completed")]
 organization=models.ForeignKey(Organization,on_delete=models.CASCADE); name=models.CharField(max_length=220); client_name=models.CharField(max_length=180,blank=True); objective=models.TextField(blank=True); status=models.CharField(max_length=20,choices=STATUSES,default="planned"); start_date=models.DateField(null=True,blank=True); due_date=models.DateField(null=True,blank=True); budget=models.DecimalField(max_digits=14,decimal_places=2,default=0); actual_cost=models.DecimalField(max_digits=14,decimal_places=2,default=0); manager=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self): return self.name
class Survey(models.Model):
 organization=models.ForeignKey(Organization,on_delete=models.CASCADE); title=models.CharField(max_length=220); description=models.TextField(blank=True); is_active=models.BooleanField(default=True); public_token=models.SlugField(unique=True,max_length=60); created_by=models.ForeignKey(User,on_delete=models.SET_NULL,null=True); created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self): return self.title
class SurveyQuestion(models.Model):
 TYPES=[("text","Text"),("textarea","Long text"),("single","Single choice"),("multiple","Multiple choice"),("rating","Rating 1-5"),("number","Number")]
 survey=models.ForeignKey(Survey,on_delete=models.CASCADE,related_name="questions"); prompt=models.CharField(max_length=500); question_type=models.CharField(max_length=20,choices=TYPES,default="text"); options=models.TextField(blank=True); required=models.BooleanField(default=False); order=models.PositiveIntegerField(default=0)
 class Meta: ordering=["order","id"]
class SurveyResponse(models.Model):
 survey=models.ForeignKey(Survey,on_delete=models.CASCADE,related_name="responses"); respondent=models.CharField(max_length=180,blank=True); answers=models.JSONField(default=dict); submitted_at=models.DateTimeField(auto_now_add=True)
class DataSource(models.Model):
 organization=models.ForeignKey(Organization,on_delete=models.CASCADE); name=models.CharField(max_length=180); source_type=models.CharField(max_length=80,default="Manual"); base_url=models.URLField(blank=True); description=models.TextField(blank=True); refresh_frequency=models.CharField(max_length=80,blank=True); active=models.BooleanField(default=True); last_checked=models.DateTimeField(null=True,blank=True)
 def __str__(self): return self.name
class Alert(models.Model):
 organization=models.ForeignKey(Organization,on_delete=models.CASCADE); title=models.CharField(max_length=220); keyword=models.CharField(max_length=180,blank=True); module=models.CharField(max_length=40,blank=True); threshold=models.CharField(max_length=120,blank=True); active=models.BooleanField(default=True); created_by=models.ForeignKey(User,on_delete=models.SET_NULL,null=True); created_at=models.DateTimeField(auto_now_add=True)
class Notification(models.Model):
 organization=models.ForeignKey(Organization,on_delete=models.CASCADE); user=models.ForeignKey(User,on_delete=models.CASCADE); title=models.CharField(max_length=220); message=models.TextField(blank=True); read=models.BooleanField(default=False); created_at=models.DateTimeField(auto_now_add=True)
class Report(models.Model):
 organization=models.ForeignKey(Organization,on_delete=models.CASCADE); title=models.CharField(max_length=220); report_type=models.CharField(max_length=100,default="Market research"); executive_summary=models.TextField(blank=True); findings=models.TextField(blank=True); recommendations=models.TextField(blank=True); status=models.CharField(max_length=30,default="Draft"); created_by=models.ForeignKey(User,on_delete=models.SET_NULL,null=True); created_at=models.DateTimeField(auto_now_add=True)
class Conversation(models.Model):
 organization=models.ForeignKey(Organization,on_delete=models.CASCADE); user=models.ForeignKey(User,on_delete=models.CASCADE); title=models.CharField(max_length=220,default="Market research chat"); created_at=models.DateTimeField(auto_now_add=True)
class ChatMessage(models.Model):
 conversation=models.ForeignKey(Conversation,on_delete=models.CASCADE,related_name="messages"); role=models.CharField(max_length=20,choices=[("user","User"),("assistant","Assistant")]); content=models.TextField(); created_at=models.DateTimeField(auto_now_add=True)
class Subscription(models.Model):
 PLANS=[("free","Free"),("starter","Starter"),("professional","Professional"),("enterprise","Enterprise")]
 organization=models.OneToOneField(Organization,on_delete=models.CASCADE); plan=models.CharField(max_length=20,choices=PLANS,default="free"); status=models.CharField(max_length=30,default="trial"); started_at=models.DateField(default=timezone.now); renews_at=models.DateField(null=True,blank=True); external_reference=models.CharField(max_length=180,blank=True)
