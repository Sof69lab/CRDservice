from django.urls import path
from formapp import views

urlpatterns = [
    # path("", views.HomeView.as_view(), name='home'),
    path("", views.home, name='home'),
    path("homeGIP/<int:id>/", views.homeGIP, name='homeGIP'),
    path("infoGIP/<int:id>/", views.infoGIP, name='reestInfo'),
    path("fileManage/<int:id>/", views.fileManage, name='fileManage'),
    path("deleteFile/<int:id>", views.delete_file, name='deleteFile'),
    path("deleteAll/<int:id>", views.delete_all, name='deleteAll'),
    path("uploadFile/<int:id>", views.upload_file, name='uploadFile'),
    path("new_reestr/", views.newReestr, name='newReestr'),
    path("gip/<int:id>/", views.gip, name='GIP'),
    path("boss/<int:id>/", views.boss, name='boss'),
    path("boss2/<int:id>/", views.boss2, name='boss2'),
    path("gip2/<int:id>/", views.gip2, name='gip2'),
    path("final/<int:id>/", views.final, name='final'),
    path("close/<int:id>/", views.close, name='close'),
    path("employee/<int:id>/", views.employee, name='employee'),
]
