from django.urls import path
from . import views as v
urlpatterns=[
path("",v.dashboard,name="dashboard"),
path("m/<slug:module>/",v.module_list,name="module_list"),path("m/<slug:module>/new/",v.item_form,name="item_create"),path("m/<slug:module>/<int:pk>/edit/",v.item_form,name="item_edit"),path("m/<slug:module>/export/",v.export_csv,name="export_csv"),path("m/<slug:module>/import/",v.import_csv,name="import_csv"),path("item/<int:pk>/",v.item_detail,name="item_detail"),path("item/<int:pk>/delete/",v.item_delete,name="item_delete"),
path("projects/",v.projects,name="projects"),path("projects/new/",v.project_form,name="project_create"),path("projects/<int:pk>/edit/",v.project_form,name="project_edit"),
path("surveys/",v.surveys,name="surveys"),path("surveys/new/",v.survey_form,name="survey_create"),path("surveys/<int:pk>/",v.survey_detail,name="survey_detail"),path("surveys/<int:pk>/edit/",v.survey_form,name="survey_edit"),path("surveys/<int:pk>/questions/new/",v.question_add,name="question_add"),path("questions/<int:pk>/delete/",v.question_delete,name="question_delete"),path("s/<slug:token>/",v.public_survey,name="public_survey"),
path("sources/",v.sources,name="sources"),path("sources/new/",v.source_form,name="source_create"),path("sources/<int:pk>/edit/",v.source_form,name="source_edit"),path("alerts/",v.alerts,name="alerts"),path("alerts/new/",v.alert_form,name="alert_create"),
path("reports/",v.reports,name="reports"),path("reports/new/",v.report_form,name="report_create"),path("reports/<int:pk>/edit/",v.report_form,name="report_edit"),path("reports/<int:pk>/print/",v.report_print,name="report_print"),
path("ai/",v.ai,name="ai"),path("analytics/",v.analytics,name="analytics"),path("settings/",v.settings_page,name="settings")]
