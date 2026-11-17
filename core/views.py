import csv,json,uuid,requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count,Q
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.utils.text import slugify
from .modules import MODULES
from .models import *
from .forms import *
def current_org(user):
 m=Membership.objects.filter(user=user).select_related("organization").first()
 if m:return m.organization
 slug=f"{slugify(user.username) or 'workspace'}-{user.id}"
 org,_=Organization.objects.get_or_create(slug=slug,defaults={"name":f"{user.username}'s Workspace"})
 Membership.objects.get_or_create(organization=org,user=user,defaults={"role":"owner"})
 Subscription.objects.get_or_create(organization=org)
 return org
@login_required
def dashboard(request):
 o=current_org(request.user); qs=ResearchItem.objects.filter(organization=o)
 counts=qs.values("module").annotate(total=Count("id")).order_by("-total")
 return render(request,"core/dashboard.html",{"org":o,"total":qs.count(),"projects":ResearchProject.objects.filter(organization=o).count(),"competitors":qs.filter(module="competitor").count(),"opportunities":qs.filter(module="opportunity").count(),"reports":Report.objects.filter(organization=o).count(),"surveys":Survey.objects.filter(organization=o).count(),"counts":counts,"recent":qs[:10]})
@login_required
def module_list(request,module):
 if module not in MODULES:return redirect("dashboard")
 q=request.GET.get("q",""); status=request.GET.get("status","")
 qs=ResearchItem.objects.filter(organization=current_org(request.user),module=module)
 if q:qs=qs.filter(Q(title__icontains=q)|Q(summary__icontains=q)|Q(category__icontains=q))
 if status:qs=qs.filter(status=status)
 page=Paginator(qs,15).get_page(request.GET.get("page"))
 return render(request,"core/module_list.html",{"module":module,"title":MODULES[module],"description":MODULES[module]+" records and analysis workspace.","page":page,"q":q,"status":status,"statuses":ResearchItem.STATUSES})
@login_required
def item_form(request,module,pk=None):
 if module not in MODULES:return redirect("dashboard")
 o=current_org(request.user); obj=get_object_or_404(ResearchItem,pk=pk,organization=o,module=module) if pk else None
 form=ResearchItemForm(request.POST or None,instance=obj)
 if request.method=="POST" and form.is_valid():
  x=form.save(commit=False);x.organization=o;x.module=module;x.owner=request.user;x.data=form.cleaned_data["data_json"];x.save()
  messages.success(request,"Research record saved.");return redirect("item_detail",pk=x.pk)
 return render(request,"core/form.html",{"form":form,"heading":MODULES[module],"action":"Update" if obj else "Create"})
@login_required
def item_detail(request,pk):
 x=get_object_or_404(ResearchItem,pk=pk,organization=current_org(request.user))
 return render(request,"core/item_detail.html",{"x":x})
@login_required
def item_delete(request,pk):
 x=get_object_or_404(ResearchItem,pk=pk,organization=current_org(request.user));m=x.module
 if request.method=="POST":x.delete();messages.success(request,"Record deleted.")
 return redirect("module_list",module=m)
@login_required
def export_csv(request,module):
 qs=ResearchItem.objects.filter(organization=current_org(request.user),module=module)
 r=HttpResponse(content_type="text/csv");r["Content-Disposition"]=f'attachment; filename="{module}.csv"'
 w=csv.writer(r);w.writerow(["Title","Summary","Status","Category","Geography","Source","Source URL","Value","Unit","Score","Tags","Data"])
 for x in qs:w.writerow([x.title,x.summary,x.status,x.category,x.geography,x.source_name,x.source_url,x.value,x.unit,x.score,x.tags,json.dumps(x.data)])
 return r
@login_required
def import_csv(request,module):
 if request.method=="POST" and request.FILES.get("file"):
  try:
   rows=csv.DictReader(request.FILES["file"].read().decode("utf-8-sig").splitlines());n=0
   for row in rows:
    if not row.get("Title"):continue
    ResearchItem.objects.create(organization=current_org(request.user),module=module,title=row["Title"][:240],summary=row.get("Summary",""),category=row.get("Category",""),geography=row.get("Geography",""),source_name=row.get("Source",""),source_url=row.get("Source URL","") or "",unit=row.get("Unit",""),tags=row.get("Tags",""),owner=request.user);n+=1
   messages.success(request,f"Imported {n} records.")
  except Exception as e:messages.error(request,f"Import failed: {e}")
 return redirect("module_list",module=module)
@login_required
def projects(request):
 return render(request,"core/projects.html",{"rows":ResearchProject.objects.filter(organization=current_org(request.user))})
@login_required
def project_form(request,pk=None):
 o=current_org(request.user);obj=get_object_or_404(ResearchProject,pk=pk,organization=o) if pk else None;f=ProjectForm(request.POST or None,instance=obj)
 if request.method=="POST" and f.is_valid():
  x=f.save(commit=False);x.organization=o;x.save();messages.success(request,"Project saved.");return redirect("projects")
 return render(request,"core/form.html",{"form":f,"heading":"Research project","action":"Save"})
@login_required
def surveys(request):
 return render(request,"core/surveys.html",{"rows":Survey.objects.filter(organization=current_org(request.user)).annotate(n=Count("responses"))})
@login_required
def survey_form(request,pk=None):
 o=current_org(request.user);obj=get_object_or_404(Survey,pk=pk,organization=o) if pk else None;f=SurveyForm(request.POST or None,instance=obj)
 if not obj and not request.POST:f.fields["public_token"].initial=uuid.uuid4().hex[:12]
 if request.method=="POST" and f.is_valid():
  x=f.save(commit=False);x.organization=o;x.created_by=request.user;x.save();return redirect("survey_detail",pk=x.pk)
 return render(request,"core/form.html",{"form":f,"heading":"Survey","action":"Save"})
@login_required
def survey_detail(request,pk):
 s=get_object_or_404(Survey,pk=pk,organization=current_org(request.user))
 return render(request,"core/survey_detail.html",{"s":s})
@login_required
def question_add(request,pk):
 s=get_object_or_404(Survey,pk=pk,organization=current_org(request.user));f=QuestionForm(request.POST or None)
 if request.method=="POST" and f.is_valid():q=f.save(commit=False);q.survey=s;q.save();return redirect("survey_detail",pk=s.pk)
 return render(request,"core/form.html",{"form":f,"heading":"Survey question","action":"Add"})
@login_required
def question_delete(request,pk):
 q=get_object_or_404(SurveyQuestion,pk=pk,survey__organization=current_org(request.user));sid=q.survey_id
 if request.method=="POST":q.delete()
 return redirect("survey_detail",pk=sid)
def public_survey(request,token):
 s=get_object_or_404(Survey,public_token=token,is_active=True)
 if request.method=="POST":
  a={str(q.id):request.POST.get(f"q_{q.id}","") for q in s.questions.all()}
  SurveyResponse.objects.create(survey=s,respondent=request.POST.get("respondent",""),answers=a)
  return render(request,"core/thanks.html",{"s":s})
 return render(request,"core/public_survey.html",{"s":s})
@login_required
def sources(request):
 return render(request,"core/sources.html",{"rows":DataSource.objects.filter(organization=current_org(request.user))})
@login_required
def source_form(request,pk=None):
 o=current_org(request.user);obj=get_object_or_404(DataSource,pk=pk,organization=o) if pk else None;f=SourceForm(request.POST or None,instance=obj)
 if request.method=="POST" and f.is_valid():x=f.save(commit=False);x.organization=o;x.save();return redirect("sources")
 return render(request,"core/form.html",{"form":f,"heading":"Data source","action":"Save"})
@login_required
def alerts(request):
 return render(request,"core/alerts.html",{"rows":Alert.objects.filter(organization=current_org(request.user))})
@login_required
def alert_form(request):
 f=AlertForm(request.POST or None)
 if request.method=="POST" and f.is_valid():x=f.save(commit=False);x.organization=current_org(request.user);x.created_by=request.user;x.save();return redirect("alerts")
 return render(request,"core/form.html",{"form":f,"heading":"Intelligence alert","action":"Create"})
@login_required
def reports(request):
 return render(request,"core/reports.html",{"rows":Report.objects.filter(organization=current_org(request.user))})
@login_required
def report_form(request,pk=None):
 o=current_org(request.user);obj=get_object_or_404(Report,pk=pk,organization=o) if pk else None;f=ReportForm(request.POST or None,instance=obj)
 if request.method=="POST" and f.is_valid():x=f.save(commit=False);x.organization=o;x.created_by=request.user;x.save();return redirect("reports")
 return render(request,"core/form.html",{"form":f,"heading":"Research report","action":"Save"})
@login_required
def report_print(request,pk):
 r=get_object_or_404(Report,pk=pk,organization=current_org(request.user));return render(request,"core/report_print.html",{"r":r})
@login_required
def ai(request):
 answer=""
 if request.method=="POST":
  prompt=request.POST.get("prompt","");o=current_org(request.user)
  context=list(ResearchItem.objects.filter(organization=o).values("title","module","summary")[:25])
  if settings.AI_API_KEY:
   try:
    res=requests.post(settings.AI_API_BASE.rstrip("/")+"/chat/completions",headers={"Authorization":f"Bearer {settings.AI_API_KEY}"},json={"model":settings.AI_MODEL,"messages":[{"role":"system","content":"You are a market research analyst. Separate verified facts from assumptions and never invent sources."},{"role":"user","content":f"Workspace research records: {json.dumps(context)}\nQuestion: {prompt}"}]},timeout=45);res.raise_for_status();answer=res.json()["choices"][0]["message"]["content"]
   except Exception as e:answer=f"AI provider error: {e}"
  else:answer=f"AI is not configured. This is a research framework, not verified market data. For: {prompt}\n\n1. Define geography, period and target segment.\n2. Gather primary and secondary sources.\n3. Compare market size, competitors, pricing and demand.\n4. Triangulate key estimates.\n5. Record source links, assumptions and limitations.\n\nWorkspace records available: {len(context)}"
 return render(request,"core/ai.html",{"answer":answer})
@login_required
def analytics(request):
 o=current_org(request.user);qs=ResearchItem.objects.filter(organization=o)
 return render(request,"core/analytics.html",{"data":list(qs.values("module").annotate(n=Count("id"))),"items":qs[:100],"total":qs.count()})
@login_required
def settings_page(request):
 o=current_org(request.user);f=OrgForm(request.POST or None,instance=o)
 if request.method=="POST" and f.is_valid():f.save();messages.success(request,"Workspace updated.")
 return render(request,"core/settings.html",{"form":f,"members":Membership.objects.filter(organization=o).select_related("user"),"sub":Subscription.objects.filter(organization=o).first()})
