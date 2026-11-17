import json
from django import forms
from .models import ResearchItem,ResearchProject,Survey,SurveyQuestion,DataSource,Alert,Report,Organization
class StyledForm(forms.ModelForm):
 def __init__(self,*a,**kw):
  super().__init__(*a,**kw)
  for f in self.fields.values(): f.widget.attrs["class"]="form-control"
class ResearchItemForm(StyledForm):
 data_json=forms.CharField(required=False,widget=forms.Textarea(attrs={"rows":5}),help_text="Optional JSON object for module-specific fields.")
 class Meta:
  model=ResearchItem; fields=["title","summary","status","category","geography","source_name","source_url","value","unit","score","tags"]
 def __init__(self,*a,**kw):
  super().__init__(*a,**kw); self.fields["data_json"].initial=json.dumps(getattr(self.instance,"data",{}) or {},indent=2)
 def clean_data_json(self):
  raw=self.cleaned_data.get("data_json","").strip()
  if not raw:return {}
  try:
   v=json.loads(raw)
   if not isinstance(v,dict): raise ValueError()
   return v
  except Exception: raise forms.ValidationError("Enter a valid JSON object.")
class ProjectForm(StyledForm):
 class Meta:
  model=ResearchProject; fields=["name","client_name","objective","status","start_date","due_date","budget","actual_cost","manager"]
  widgets={"start_date":forms.DateInput(attrs={"type":"date"}),"due_date":forms.DateInput(attrs={"type":"date"})}
class SurveyForm(StyledForm):
 class Meta: model=Survey; fields=["title","description","is_active","public_token"]
class QuestionForm(StyledForm):
 class Meta: model=SurveyQuestion; fields=["prompt","question_type","options","required","order"]
class SourceForm(StyledForm):
 class Meta: model=DataSource; fields=["name","source_type","base_url","description","refresh_frequency","active"]
class AlertForm(StyledForm):
 class Meta: model=Alert; fields=["title","keyword","module","threshold","active"]
class ReportForm(StyledForm):
 class Meta: model=Report; fields=["title","report_type","executive_summary","findings","recommendations","status"]
class OrgForm(StyledForm):
 class Meta: model=Organization; fields=["name","slug","website","industry"]
