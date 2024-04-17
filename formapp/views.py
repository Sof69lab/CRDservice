from django.shortcuts import render
from formapp.forms import BossForm1, GIPform, GIPform2, FinalForm, CloseForm, emplForm, ReestrForm, workDays, FileForm
from formapp.models import reestr, reestInfo, files
from django.shortcuts import redirect
from django.db.models import Q
import xlsxwriter
from datetime import datetime
from win32comext.shell import shell, shellcon
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import numpy as np
import tkinter as tk
from tkinter import filedialog

def dataFormat(s):
    months = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06', 'июля': '07',
               'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'}
    i = 0
    day = ''
    while s[i] in '0123456789 ' and i < len(s):
        if s[i] != ' ':
            day += s[i]
        i += 1
    if len(day) < 2:
        day = '0'+day
    month = ''
    while s[i] != ' ':
        month += s[i]
        i += 1
    month = months[month]
    year = ''
    i += 1
    while s[i] in '0123456789':
        year += s[i]
        i += 1
    return day+'.'+month+'.'+year

def dateDBformat(d):
    if d is not None:
        if d.month < 10:
            month = '0'+str(d.month)
        else:
            month = str(d.month)
        return str(d.day)+'.'+month+'.'+str(d.year)
    else:
        return '     '

def shortName(s):
    i = 0
    while s[i] != ' ':
        i += 1
    newS = s[0:i+2]
    i += 1
    while s[i] != ' ':
        i += 1
    newS += '.'+s[i+1]+'.'
    return newS

def select_dir():
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    return filedialog.askdirectory(parent=root)

def xlslxCreate(request, userRole='ГИП'):
    date = datetime.now()
    path = select_dir()
    name = "\реестр_" + str(request.POST.get("project_dogovor"))[4:9] + str(request.POST.get("num_reestr")) + "_" + str(
        date.hour) + '-' + str(date.minute) + '-' + str(date.second) + '_' + str(date.day) + '-' + str(
        date.month) + '-' + str(date.year) + '.xlsx'
    if (userRole == 'ГИП'):
        remarks = reestr.objects.filter(reestrID=request.POST.get("id"))
    elif (userRole == 'Руководитель'):
        remarks = reestr.objects.filter((Q(reestrID=request.POST.get("id")) & Q(responsibleTrouble_name=request.user)))
    else:
        remarks = reestr.objects.filter((Q(reestrID=request.POST.get("id")) & Q(executor_name=request.user)))
    workbook = xlsxwriter.Workbook(path + name)
    worksheet = workbook.add_worksheet()
    worksheet.hide_gridlines(2)

    cell_format1 = workbook.add_format({'bold': True,  # заголовок
                                        'font_size': 28,
                                        'font_name': 'Times New Roman',
                                        'align': 'center',
                                        'valign': 'vcenter'})
    cell_format1wrap = workbook.add_format({'bold': True,  # заголовок с переносом
                                            'font_size': 28,
                                            'font_name': 'Times New Roman',
                                            'align': 'center',
                                            'valign': 'vcenter',
                                            'text_wrap': True})
    cell_format2 = workbook.add_format({'bold': True,  # шапка таблицы
                                        'font_size': 20,
                                        'font_name': 'Times New Roman',
                                        'align': 'center',
                                        'valign': 'vcenter',
                                        'border': 1,
                                        'bg_color': '#DDEBF7'})
    cell_format2wrap = workbook.add_format({'bold': True,  # шапка таблицы с переносом
                                            'font_size': 20,
                                            'font_name': 'Times New Roman',
                                            'align': 'center',
                                            'valign': 'vcenter',
                                            'border': 1,
                                            'bg_color': '#DDEBF7',
                                            'text_wrap': True})
    cell_format3 = workbook.add_format({'bold': True,  # шапка таблицы с номерами
                                        'italic': True,
                                        'font_size': 20,
                                        'font_name': 'Times New Roman',
                                        'align': 'center',
                                        'valign': 'vcenter',
                                        'border': 1})
    cell_format4 = workbook.add_format({'font_size': 20,  # замечания
                                        'font_name': 'Times New Roman',
                                        'align': 'center',
                                        'valign': 'vcenter',
                                        'border': 1})
    cell_format4left = workbook.add_format({'font_size': 20,  # замечания по левому краю
                                            'font_name': 'Times New Roman',
                                            'align': 'left',
                                            'valign': 'vcenter',
                                            'border': 1,
                                            'text_wrap': True})
    cell_format4wrap = workbook.add_format({'font_size': 20,  # замечания c переносом
                                            'font_name': 'Times New Roman',
                                            'align': 'center',
                                            'valign': 'vcenter',
                                            'border': 1,
                                            'text_wrap': True})
    cell_format5 = workbook.add_format({'font_size': 24,  # подписи
                                        'font_name': 'Times New Roman',
                                        'align': 'left',
                                        'valign': 'bottom'})
    # заголовок
    worksheet.merge_range("C3:T3", "Реестр выявленных несоответствий № " + request.POST.get("project_dogovor")[
                                                                           4:9] + request.POST.get("num_reestr"),
                          cell_format1)
    worksheet.merge_range("C4:T4", "Наименование проекта: Договор № " + request.POST.get("project_dogovor") + " от " +
                          dataFormat(request.POST.get("project_date_contract")) + ' "' + request.POST.get(
        "project_name") + '"', cell_format1wrap)
    worksheet.merge_range("C5:T5", "(Рецензент : " + request.POST.get("project_reviewer") + "; исх. № " +
                          request.POST.get("out_mail_num") + " от " + request.POST.get("out_mail_date") + "; вх. № " +
                          request.POST.get("in_mail_num") + " от " + request.POST.get("in_mail_date") + ")",
                          cell_format1)
    # шапка
    worksheet.set_column('A:A', 8.33)
    worksheet.merge_range("A7:A8", " № ", cell_format2)
    worksheet.set_column('B:B', 24.56)
    worksheet.merge_range("B7:B8", " № замечания ", cell_format2)
    worksheet.set_column('C:C', 96.22)
    worksheet.merge_range("C7:C8", "Наименование замечания", cell_format2)
    worksheet.set_column('D:D', 63.78)
    worksheet.merge_range("D7:D8", "Обоснование", cell_format2)
    worksheet.set_column('E:E', 24.78)
    worksheet.merge_range("E7:E8", "Обозначение раздела в проекте", cell_format2wrap)
    worksheet.set_column('F:F', 28.33)
    worksheet.merge_range("F7:F8", "Наименование раздела", cell_format2wrap)
    worksheet.set_column('G:G', 29.33)
    worksheet.merge_range("G7:G8", "Ответственный за устранение замечания (начальник подразделения)", cell_format2wrap)
    worksheet.set_column('H:H', 29.89)
    worksheet.merge_range("H7:H8", "Исполнитель, допустивший замечание", cell_format2wrap)
    worksheet.set_column('I:I', 29.89)
    worksheet.merge_range("I7:I8", "Исполнитель, ответственный за устранение замечания", cell_format2wrap)
    worksheet.set_column('J:O', 25.33)
    worksheet.merge_range("J7:K7", "Дата предоставления ответов на замечания", cell_format2wrap)
    worksheet.merge_range("L7:M7", "Срок внесения корректировок", cell_format2wrap)
    worksheet.merge_range("N7:O7", "Трудозатраты, дн. (на устранение замечания)", cell_format2wrap)
    for i in range(9, 15):
        if i % 2 == 0:
            worksheet.write(7, i, "Факт", cell_format2)
        else:
            worksheet.write(7, i, "План", cell_format2)
    worksheet.set_column('P:P', 63.67)
    worksheet.merge_range("P7:P8", "Комментарии", cell_format2)
    worksheet.set_column('Q:Q', 63.56)
    worksheet.merge_range("Q7:Q8", "Ответы на замечания", cell_format2)
    worksheet.set_column('R:R', 38.33)
    worksheet.merge_range("R7:R8",
                          "Ссылка в технической документации (том, книга, раздел, стр.лист) на внесённые изменения",
                          cell_format2wrap)
    worksheet.set_column('S:S', 37.22)
    worksheet.merge_range("S7:S8", "Отметка о снятии замечания, дата", cell_format2wrap)
    worksheet.set_column('T:U', 34.33)
    worksheet.merge_range("T7:T8", "Значимость замечания", cell_format2wrap)
    worksheet.merge_range("U7:U8", "Коренная причина", cell_format2)
    # нумерация столбцов
    nums = ['1', '1.1', '2', '2.1', '3', '4', '5', '6', '6.1', '7', '8', '9', '10', '10.1', '10.2', '10.3', '11', '12',
            '13', '14', '15']
    for i in range(len(nums)):
        worksheet.write(8, i, nums[i], cell_format3)
    # замечания
    boss = []
    employers = []
    for i in range(len(remarks)):
        if remarks[i].responsibleTrouble_name is not None:
            boss.append(remarks[i].responsibleTrouble_name.id)
        if remarks[i].executor_name is not None:
            employers.append(remarks[i].executor_name.id)
        worksheet.write(9 + i, 0, str(i + 1), cell_format4)
        worksheet.write(9 + i, 1, remarks[i].num_remark, cell_format4)
        worksheet.write(9 + i, 2, remarks[i].remark_name, cell_format4left)
        worksheet.write(9 + i, 3, remarks[i].rational, cell_format4left)
        worksheet.write(9 + i, 4, remarks[i].designation_name, cell_format4wrap)
        worksheet.write(9 + i, 5, remarks[i].section_name, cell_format4wrap)
        if remarks[i].responsibleTrouble_name is not None:
            worksheet.write(9 + i, 6, shortName(str(remarks[i].responsibleTrouble_name)), cell_format4)
        else:
            worksheet.write(9 + i, 6, '', cell_format4)
        if remarks[i].executor_fail_name is not None:
            worksheet.write(9 + i, 7, shortName(str(remarks[i].executor_fail_name)), cell_format4)
        else:
            worksheet.write(9 + i, 7, '', cell_format4)
        if remarks[i].executor_name is not None:
            worksheet.write(9 + i, 8, shortName(str(remarks[i].executor_name)), cell_format4)
        else:
            worksheet.write(9 + i, 8, '', cell_format4)
        worksheet.write(9 + i, 9, dateDBformat(remarks[i].answer_date_plan), cell_format4)
        worksheet.write(9 + i, 10, dateDBformat(remarks[i].answer_date_fact), cell_format4)
        worksheet.write(9 + i, 11, dateDBformat(remarks[i].answer_deadline_correct_plan), cell_format4)
        worksheet.write(9 + i, 12, dateDBformat(remarks[i].answer_deadline_correct_fact), cell_format4)
        worksheet.write(9 + i, 13, remarks[i].labor_costs_plan, cell_format4)
        worksheet.write(9 + i, 14, remarks[i].labor_costs_fact, cell_format4)
        worksheet.write(9 + i, 15, remarks[i].comment, cell_format4left)
        worksheet.write(9 + i, 16, remarks[i].answer_remark, cell_format4left)
        worksheet.write(9 + i, 17, remarks[i].link_tech_name, cell_format4wrap)
        worksheet.write(9 + i, 18, dateDBformat(remarks[i].cancel_remark), cell_format4)
        worksheet.write(9 + i, 19, remarks[i].total_importance, cell_format4)
        worksheet.write(9 + i, 20, remarks[i].root_cause_list, cell_format4)
    k = 12 + len(remarks)
    worksheet.write(k, 2, '"ЗНАЧИМОСТЬ ЗАМЕЧАНИЙ И КОРЕННЫЕ ПРИЧИНЫ СОГЛАСОВАЛ":', cell_format5)
    worksheet.write(k, 7, 'Заказчик: ' + request.POST.get("customer"), cell_format5)
    worksheet.write(k, 17, '"СНЯТИЕ ЗАМЕЧАНИЙ ПОДТВЕРЖДАЮ":', cell_format5)
    k += 2
    worksheet.write(k, 2, "Главный инженер проекта " + shortName(request.POST.get("gip")) + "    (дата)", cell_format5)
    worksheet.write(k, 17, 'Главный инженер проекта  ________________    (дата)', cell_format5)
    k += 3
    worksheet.write(k, 2, '"ЗНАЧИМОСТЬ ЗАМЕЧАНИЙ  И КОРЕННЫЕ ПРИЧИНЫ ОПРЕДЕЛИЛ":', cell_format5)
    k += 1
    worksheet.write(k, 17, '"ОТВЕТЫ НА  ЗАМЕЧАНИЯ ПРЕДСТАВИЛ":', cell_format5)
    k += 1
    boss = np.unique(np.array(boss))
    for i in range(len(boss)):
        worksheet.write(k, 2, 'Начальник отдела ___________________(дата)', cell_format5)
        k += 1
        worksheet.write(k, 17, 'Начальник отдела ________________(дата)', cell_format5)
        k += 1
    worksheet.write(k, 2, '"С ОЦЕНКОЙ  ЗНАЧИМОСТИ ЗАМЕЧАНИЙ ОЗНАКОМЛЕН":', cell_format5)
    k += 2
    worksheet.write(k, 2, 'ИСПОЛНИТЕЛИ:', cell_format5)
    employers = np.unique(np.array(employers))
    for i in range(len(employers)):
        k += 1
        worksheet.write(k, 2, '_____________________    (дата)', cell_format5)
    worksheet.autofit()
    workbook.close()

def home(request):
    group = ''
    info = []
    if request.user.groups.filter(name='ГИП').exists():
        group = 'ГИП'
        reestrs = reestInfo.objects.filter(gip=request.user)
        for r in reestrs:
            remarks = len(reestr.objects.filter(reestrID=r.id))
            customer = len(reestr.objects.filter((Q(reestrID=r.id) & Q(total_importance='В компетенции Заказчика'))))
            signific = len(reestr.objects.filter((Q(reestrID=r.id) & Q(total_importance='Существенное'))))
            insignific = len(reestr.objects.filter((Q(reestrID=r.id) & Q(total_importance='Несущественное'))))
            info.append([r.id, remarks, customer, signific, insignific])
    elif request.user.is_superuser:
        reestrs = reestInfo.objects.all()
        for r in reestrs:
            remarks = len(reestr.objects.filter(reestrID=r.id))
            customer = len(reestr.objects.filter((Q(reestrID=r.id) & Q(total_importance='В компетенции Заказчика'))))
            signific = len(reestr.objects.filter((Q(reestrID=r.id) & Q(total_importance='Существенное'))))
            insignific = len(reestr.objects.filter((Q(reestrID=r.id) & Q(total_importance='Несущественное'))))
            info.append([r.id, remarks, customer, signific, insignific])
    elif request.user.groups.filter(name='Руководитель').exists():
        group = 'Руководитель'
        remarkList = reestr.objects.filter(responsibleTrouble_name=request.user)
        IDlist = []
        for r in remarkList:
            IDlist.append(r.reestrID.id)
        reestrs = reestInfo.objects.filter(id__in=IDlist)
        for r in reestrs:
            remarks = len(reestr.objects.filter((Q(reestrID=r.id) & Q(responsibleTrouble_name=request.user))))
            customer = len(reestr.objects.filter((Q(reestrID=r.id) & Q(total_importance='В компетенции Заказчика') & Q(responsibleTrouble_name=request.user))))
            signific = len(reestr.objects.filter((Q(reestrID=r.id) & Q(total_importance='Существенное') & Q(responsibleTrouble_name=request.user))))
            insignific = len(reestr.objects.filter((Q(reestrID=r.id) & Q(total_importance='Несущественное') & Q(responsibleTrouble_name=request.user))))
            info.append([r.id, remarks, customer, signific, insignific])
    elif request.user.groups.filter(name='Исполнитель').exists():
        group = 'Исполнитель'
        remarkList = reestr.objects.filter(executor_name=request.user)
        IDlist = []
        for r in remarkList:
            IDlist.append(r.reestrID.id)
        reestrs = reestInfo.objects.filter(id__in=IDlist)
        for r in reestrs:
            remarks = len(reestr.objects.filter((Q(reestrID=r.id) & Q(executor_name=request.user))))
            customer = len(reestr.objects.filter((Q(reestrID=r.id) & Q(total_importance='В компетенции Заказчика') & Q(executor_name=request.user))))
            signific = len(reestr.objects.filter((Q(reestrID=r.id) & Q(total_importance='Существенное') & Q(executor_name=request.user))))
            insignific = len(reestr.objects.filter((Q(reestrID=r.id) & Q(total_importance='Несущественное') & Q(executor_name=request.user))))
            info.append([r.id, remarks, customer, signific, insignific])
    else:
        return redirect("accounts/login/?next=/")
    if request.method == 'POST':
        xlslxCreate(request)
        return render(request, 'home.html', {'reestrs': reestrs, 'group': group, 'info': info})
    else:
        return render(request, 'home.html', {'reestrs': reestrs, 'group': group, 'info': info})

def newReestr(request):
    if request.user.groups.filter(name='ГИП').exists() or request.user.is_superuser:
        if request.method == 'POST':
            form = ReestrForm(request.POST, request.FILES or None)
            if form.is_valid():
                form.save(commit=False)
                date_contract = form.cleaned_data.get('project_date_contract')
                out_mail = form.cleaned_data.get('out_mail_date')
                in_mail = form.cleaned_data.get('in_mail_date')
                if date_contract and out_mail and in_mail is not None:
                    form.save(commit=True)
                    name = form.cleaned_data.get("file_name")
                    comment = form.cleaned_data.get("file_comment")
                    form.save_files(reestInfo.objects.all().last(), name, comment)
                if date_contract is None:
                    form.add_error('project_date_contract', 'Пожалуйста, внесите данные')
                if out_mail is None:
                    form.add_error('out_mail_date', 'Пожалуйста, внесите данные')
                if in_mail is None:
                    form.add_error('in_mail_date', 'Пожалуйста, внесите данные')
            else:
                date_contract = form.cleaned_data.get('project_date_contract')
                out_mail = form.cleaned_data.get('out_mail_date')
                in_mail = form.cleaned_data.get('in_mail_date')
                if date_contract is None:
                    form.add_error('project_date_contract', 'Пожалуйста, внесите данные')
                if out_mail is None:
                    form.add_error('out_mail_date', 'Пожалуйста, внесите данные')
                if in_mail is None:
                    form.add_error('in_mail_date', 'Пожалуйста, внесите данные')
        else:
            form = ReestrForm()
        return render(request, 'newReestr.html', {'form': form})
    else:
        return render(request, 'newReestr.html')

def infoGIP(request, id):
    reest = reestInfo.objects.get(id=id)
    if request.user.groups.filter(name='ГИП').exists() or request.user.is_superuser:
        return render(request, 'reestInfo.html', {'reest': reest})
    else:
        return render(request, 'GIPlog.html')

def homeGIP(request, id):
    if request.user.groups.filter(name='ГИП').exists():
        reest = reestInfo.objects.get(id=id)
        reestrs = reestr.objects.filter(reestrID=id)
        deadline = workDays(reest.start_date, 2)
        if request.method == 'POST':
            if request.POST.get('id'):
                xlslxCreate(request)
            else:
                reest.step = request.POST.get("step")
                reest.save(update_fields=['step'])
        return render(request, 'homeGIP.html', {'reestrs': reestrs, 'reest': reest, 'deadline': deadline, 'group': 'ГИП'})
    elif request.user.groups.filter(name='Руководитель').exists():
        reest = reestInfo.objects.get(id=id)
        reestrs = reestr.objects.filter((Q(reestrID=id) & Q(responsibleTrouble_name=request.user)))
        deadline = workDays(reest.start_date, 2)
        if request.method == 'POST':
            if request.POST.get('id'):
                xlslxCreate(request, 'Руководитель')
            else:
                reest.step = request.POST.get("step")
                reest.save(update_fields=['step'])
        return render(request, 'homeGIP.html', {'reestrs': reestrs, 'reest': reest, 'deadline': deadline, 'group': 'Руководитель'})
    elif request.user.groups.filter(name='Исполнитель').exists():
        reest = reestInfo.objects.get(id=id)
        reestrs = reestr.objects.filter((Q(reestrID=id) & Q(executor_name=request.user)))
        deadline = workDays(reest.start_date, 2)
        if request.method == 'POST':
            if request.POST.get('id'):
                xlslxCreate(request, 'Исполнитель')
        return render(request, 'homeGIP.html', {'reestrs': reestrs, 'reest': reest, 'deadline': deadline, 'group': 'Исполнитель'})
    else:
        return render(request, 'GIPlog.html')

def fileManage(request, id):
    reest = reestInfo.objects.get(id=id)
    add_files = files.objects.filter(reestr_id=id)
    if request.user.groups.filter(name='ГИП').exists() or request.user.is_superuser:
        if request.method == 'POST':
            delets = request.POST.get('deletelist')
            filelist = []
            k = 0
            while delets[0] not in '0123456789':
                delets = delets[1:]
            for i in range(len(delets)):
                if delets[i] == ",":
                    filelist.append(int(delets[k:i]))
                    k = i+1
                elif i == len(delets)-1:
                    filelist.append(int(delets[k:]))
            for f in filelist:
                files.objects.get(id=f).delete()
            return render(request, 'fileManage.html', {'reest': reest, 'files': add_files, 'group': 'ГИП'})
        else:
            return render(request, 'fileManage.html', {'reest': reest, 'files': add_files, 'group': 'ГИП'})
    elif request.user.groups.filter(name='Руководитель').exists():
        return render(request, 'fileManage.html', {'reest': reest, 'files': add_files, 'group': 'Руководитель'})
    elif request.user.groups.filter(name='Исполнитель').exists():
        return render(request, 'fileManage.html', {'reest': reest, 'files': add_files, 'group': 'Исполнитель'})
    else:
        return render(request, 'GIPlog.html')

def delete_file(request, id):
    if request.user.groups.filter(name='ГИП').exists() or request.user.is_superuser:
        fileName = files.objects.get(id=id)
        if request.method == 'POST':
            reestr_id = files.objects.get(id=id).reestr_id
            files.objects.get(id=id).delete()
            return redirect('fileManage', id=reestr_id)
        else:
            return render(request, 'deleteFile.html', {'file': fileName})
    else:
        return render(request, 'GIPlog.html')

def delete_all(request, id):
    if request.user.groups.filter(name='ГИП').exists() or request.user.is_superuser:
        fileNames = files.objects.filter(reestr=id)
        reestr = reestInfo.objects.get(id=id)
        if request.method == 'POST':
            for f in fileNames:
                f.delete()
            return redirect('fileManage', id=id)
        else:
            return render(request, 'deleteAll.html', {'files': fileNames, 'reestr': reestr})
    else:
        return render(request, 'GIPlog.html')

def upload_file(request, id):
    if request.user.groups.filter(name='Руководитель').exists():
        group = "Руководитель"
    elif request.user.groups.filter(name='Исполнитель').exists():
        group = "Исполнитель"
    else:
        group = "ГИП"
    reestr = reestInfo.objects.get(id=id)
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save(commit=False)
            name = form.cleaned_data.get("file_name")
            comment = form.cleaned_data.get("comment")
            form.save_files(reestr, name, comment)
    else:
        form = FileForm()
    return render(request, 'uploadFile.html', {'form': form, 'reestr': reestr, 'group': group})

def gip(request, id):
    if request.user.groups.filter(name='ГИП').exists():
        reest = reestInfo.objects.get(id=id)
        if request.method == 'POST':
            form = GIPform(reest, request.POST, request.FILES or None)
            if form.is_valid():
                form.save(commit=False)
                respons = form.cleaned_data.get('responsibleTrouble_name')
                date_contract = form.cleaned_data.get('project_date_contract')
                out_mail = form.cleaned_data.get('out_mail_date')
                in_mail = form.cleaned_data.get('in_mail_date')
                if respons != request.user:
                    if date_contract and out_mail and in_mail is not None:
                        form.save(commit=True)
                        name = form.cleaned_data.get("file_name")
                        comment = form.cleaned_data.get("file_comment")
                        remark = form.cleaned_data.get("num_remark")
                        form.save_files(reest, name, comment, remark)
                else:
                    executor_fail_name = form.cleaned_data.get('executor_fail_name')
                    executor_name = form.cleaned_data.get('executor_name')
                    if executor_name != request.user:
                        if executor_name and executor_fail_name:
                            form.save(commit=True)
                            name = form.cleaned_data.get("file_name")
                            comment = form.cleaned_data.get("file_comment")
                            remark = form.cleaned_data.get("num_remark")
                            form.save_files(reestInfo.objects.get(id=id), name, comment, remark)
                    else:
                        answer_date = form.cleaned_data.get('answer_date_plan')
                        answer_deadline = form.cleaned_data.get('answer_deadline_correct_plan')
                        labor_costs = form.cleaned_data.get('labor_costs_plan')
                        comment = form.cleaned_data.get('comment')
                        total_importance = form.cleaned_data.get('total_importance')
                        root_cause_list = form.cleaned_data.get('root_cause_list')
                        if answer_date and answer_deadline and labor_costs and comment and total_importance and root_cause_list:
                            form.save(commit=True)
                            name = form.cleaned_data.get("file_name")
                            comment = form.cleaned_data.get("file_comment")
                            remark = form.cleaned_data.get("num_remark")
                            form.save_files(reestInfo.objects.get(id=id), name, comment, remark)
                        if answer_date is None:
                            form.add_error('answer_date_plan', 'Пожалуйста, внесите данные')
                        if answer_deadline is None:
                            form.add_error('answer_deadline_correct_plan', 'Пожалуйста, внесите данные')
                        if labor_costs is None:
                            form.add_error('labor_costs_plan', 'Пожалуйста, внесите данные')
                        if comment == "":
                            form.add_error('comment', 'Пожалуйста, внесите данные')
                        if total_importance == "":
                            form.add_error('total_importance', 'Пожалуйста, внесите данные')
                        if root_cause_list == "":
                            form.add_error('root_cause_list', 'Пожалуйста, внесите данные')
                    if executor_fail_name == "":
                        form.add_error('executor_fail_name', 'Пожалуйста, внесите данные')
                    if executor_name == "":
                        form.add_error('executor_name', 'Пожалуйста, внесите данные')

                if date_contract is None:
                    form.add_error('project_date_contract', 'Пожалуйста, внесите данные')
                if out_mail is None:
                    form.add_error('out_mail_date', 'Пожалуйста, внесите данные')
                if in_mail is None:
                    form.add_error('in_mail_date', 'Пожалуйста, внесите данные')
            else:
                respons = form.cleaned_data.get('responsibleTrouble_name')
                date_contract = form.cleaned_data.get('project_date_contract')
                out_mail = form.cleaned_data.get('out_mail_date')
                in_mail = form.cleaned_data.get('in_mail_date')
                if date_contract is None:
                    form.add_error('project_date_contract', 'Пожалуйста, внесите данные')
                if out_mail is None:
                    form.add_error('out_mail_date', 'Пожалуйста, внесите данные')
                if in_mail is None:
                    form.add_error('in_mail_date', 'Пожалуйста, внесите данные')

                if respons == request.user:
                    executor_fail_name = form.cleaned_data.get('executor_fail_name')
                    executor_name = form.cleaned_data.get('executor_name')
                    if executor_fail_name == "":
                        form.add_error('executor_fail_name', 'Пожалуйста, внесите данные')
                    if executor_name == "":
                        form.add_error('executor_name', 'Пожалуйста, внесите данные')
                    elif executor_name == request.user:
                        answer_date = form.cleaned_data.get('answer_date_plan')
                        answer_deadline = form.cleaned_data.get('answer_deadline_correct_plan')
                        labor_costs = form.cleaned_data.get('labor_costs_plan')
                        comment = form.cleaned_data.get('comment')
                        total_importance = form.cleaned_data.get('total_importance')
                        root_cause_list = form.cleaned_data.get('root_cause_list')
                        if answer_date is None:
                            form.add_error('answer_date_plan', 'Пожалуйста, внесите данные')
                        if answer_deadline is None:
                            form.add_error('answer_deadline_correct_plan', 'Пожалуйста, внесите данные')
                        if labor_costs is None:
                            form.add_error('labor_costs_plan', 'Пожалуйста, внесите данные')
                        if comment == "":
                            form.add_error('comment', 'Пожалуйста, внесите данные')
                        if total_importance == "":
                            form.add_error('total_importance', 'Пожалуйста, внесите данные')
                        if root_cause_list == "":
                            form.add_error('root_cause_list', 'Пожалуйста, внесите данные')

                return render(request, 'GIP.html', {'form': form})
        else:
            form = GIPform(reest)
        return render(request, 'GIP.html', {'form': form,
                                            'gipcontext': reest.gip.last_name + ' ' + reest.gip.first_name})
    else:
        return render(request, 'GIPlog.html')

def boss(request, id):
    if request.user.groups.filter(name='Руководитель').exists():
        if request.method == 'POST':
            db_form = reestr.objects.get(id=id)
            form = BossForm1(reestr.objects.get(id=id), request.POST or None)
            if form.is_valid():
                db_form.executor_fail_name = form.cleaned_data.get('executor_fail_name')
                db_form.executor_name = form.cleaned_data.get('executor_name')
                if db_form.executor_name != request.user:
                    db_form.save(update_fields=['executor_fail_name', 'executor_name'])
                else:
                    answer_date = form.cleaned_data.get('answer_date_plan')
                    answer_deadline = form.cleaned_data.get('answer_deadline_correct_plan')
                    labor_costs = form.cleaned_data.get('labor_costs_plan')
                    comment = form.cleaned_data.get('comment')
                    answer_remark = form.cleaned_data.get('answer_remark')
                    total_importance = form.cleaned_data.get('total_importance')
                    root_cause_list = form.cleaned_data.get('root_cause_list')
                    if answer_date and answer_deadline and labor_costs and comment and total_importance and root_cause_list:
                        db_form.answer_date_plan = answer_date
                        db_form.answer_deadline_correct_plan = answer_deadline
                        db_form.labor_costs_plan = labor_costs
                        db_form.comment = comment
                        db_form.answer_remark = answer_remark
                        db_form.total_importance = total_importance
                        db_form.root_cause_list = root_cause_list
                        db_form.save(update_fields=['executor_fail_name', 'executor_name', 'answer_date_plan', 'answer_deadline_correct_plan',
                          'labor_costs_plan', 'comment', 'answer_remark', 'total_importance', 'root_cause_list'])
                    if answer_date is None:
                        form.add_error('answer_date_plan', 'Пожалуйста, внесите данные')
                    if answer_deadline is None:
                        form.add_error('answer_deadline_correct_plan', 'Пожалуйста, внесите данные')
                    if labor_costs is None:
                        form.add_error('labor_costs_plan', 'Пожалуйста, внесите данные')
                    if comment == "":
                        form.add_error('comment', 'Пожалуйста, внесите данные')
                    if total_importance == "":
                        form.add_error('total_importance', 'Пожалуйста, внесите данные')
                    if root_cause_list == "":
                        form.add_error('root_cause_list', 'Пожалуйста, внесите данные')
                    print(answer_date, answer_deadline, labor_costs, comment, total_importance, root_cause_list)
            else:
                if db_form.executor_name == request.user:
                    answer_date = form.cleaned_data.get('answer_date_plan')
                    answer_deadline = form.cleaned_data.get('answer_deadline_correct_plan')
                    labor_costs = form.cleaned_data.get('labor_costs_plan')
                    comment = form.cleaned_data.get('comment')
                    total_importance = form.cleaned_data.get('total_importance')
                    root_cause_list = form.cleaned_data.get('root_cause_list')
                    if answer_date is None:
                        form.add_error('answer_date_plan', 'Пожалуйста, внесите данные')
                    if answer_deadline is None:
                        form.add_error('answer_deadline_correct_plan', 'Пожалуйста, внесите данные')
                    if labor_costs is None:
                        form.add_error('labor_costs_plan', 'Пожалуйста, внесите данные')
                    if comment is None:
                        form.add_error('comment', 'Пожалуйста, внесите данные')
                    if total_importance is None:
                        form.add_error('total_importance', 'Пожалуйста, внесите данные')
                    if root_cause_list is None:
                        form.add_error('root_cause_list', 'Пожалуйста, внесите данные')
                # return render(request, 'boss.html', context={'form': form,
                #                                              'gipcontext': reestr.objects.get(id=id).gip.last_name + ' ' + reestr.objects.get(id=id).gip.first_name})
        else:
            form = BossForm1(reest=reestr.objects.get(id=id))
        return render(request, 'boss.html', {'form': form,
                                             'gipcontext': reestr.objects.get(id=id).gip.last_name + ' ' + reestr.objects.get(id=id).gip.first_name,
                                             'rescontext': reestr.objects.get(id=id).responsibleTrouble_name.last_name + ' ' + reestr.objects.get(id=id).responsibleTrouble_name.first_name})
    else:
        return render(request, 'bossLog.html')

def employee(request, id):
    if request.user.groups.filter(name='Исполнитель').exists():
        if request.method == 'POST':
            form = emplForm(reestr.objects.get(id=id), request.POST or None)
            db_form = reestr.objects.get(id=id)
            if form.is_valid():
                # form.save(commit=False)
                labor_costs_plan = form.cleaned_data.get('labor_costs_plan')
                comment = form.cleaned_data.get('comment')
                answer_remark = form.cleaned_data.get('answer_remark')
                total_importance = form.cleaned_data.get('total_importance')
                root_cause_list = form.cleaned_data.get('root_cause_list')

                answer_date = form.cleaned_data.get('answer_date_plan')
                answer_deadline = form.cleaned_data.get('answer_deadline_correct_plan')
                if answer_date and answer_deadline and labor_costs_plan and comment and total_importance and root_cause_list:
                    db_form.answer_date_plan = answer_date
                    db_form.answer_deadline_correct_plan = answer_deadline
                    db_form.labor_costs_plan = labor_costs_plan
                    db_form.comment = comment
                    db_form.answer_remark = answer_remark
                    db_form.total_importance = total_importance
                    db_form.root_cause_list = root_cause_list
                    db_form.save(update_fields=['answer_date_plan', 'answer_deadline_correct_plan',
                      'labor_costs_plan', 'comment', 'answer_remark', 'total_importance', 'root_cause_list'])
                if answer_date is None:
                    form.add_error('answer_date_plan', 'Пожалуйста, внесите данные')
                if answer_deadline is None:
                    form.add_error('answer_deadline_correct_plan', 'Пожалуйста, внесите данные')
                if labor_costs_plan is None:
                    form.add_error('labor_costs_plan', 'Пожалуйста, внесите данные')
                if comment == "":
                    form.add_error('comment', 'Пожалуйста, внесите данные')
                if total_importance == "":
                    form.add_error('total_importance', 'Пожалуйста, внесите данные')
                if root_cause_list == "":
                    form.add_error('root_cause_list', 'Пожалуйста, внесите данные')
            else:
                labor_costs_plan = form.cleaned_data.get('labor_costs_plan')
                comment = form.cleaned_data.get('comment')
                total_importance = form.cleaned_data.get('total_importance')
                root_cause_list = form.cleaned_data.get('root_cause_list')
                answer_date = form.cleaned_data.get('answer_date_plan')
                answer_deadline = form.cleaned_data.get('answer_deadline_correct_plan')
                if answer_date is None:
                    form.add_error('answer_date_plan', 'Пожалуйста, внесите данные')
                if answer_deadline is None:
                    form.add_error('answer_deadline_correct_plan', 'Пожалуйста, внесите данные')
                if labor_costs_plan is None:
                    form.add_error('labor_costs_plan', 'Пожалуйста, внесите данные')
                if comment == "":
                    form.add_error('comment', 'Пожалуйста, внесите данные')
                if total_importance == "":
                    form.add_error('total_importance', 'Пожалуйста, внесите данные')
                if root_cause_list == "":
                    form.add_error('root_cause_list', 'Пожалуйста, внесите данные')
                # return render(request, 'employee.html', {'form': form})
        else:
            form = emplForm(reest=reestr.objects.get(id=id))
        return render(request, 'employee.html', {'form': form,
                                                 'gipcontext':
                                                     reestr.objects.get(id=id).gip.last_name + ' ' +
                                                     reestr.objects.get(id=id).gip.first_name,
                                                 'rescontext':
                                                     reestr.objects.get(id=id).responsibleTrouble_name.last_name + ' ' +
                                                     reestr.objects.get(id=id).responsibleTrouble_name.first_name,
                                                 'exfcontext':
                                                     reestr.objects.get(id=id).executor_fail_name.last_name + ' ' +
                                                     reestr.objects.get(id=id).executor_fail_name.first_name,
                                                 'excontext':
                                                     reestr.objects.get(id=id).executor_name.last_name + ' ' +
                                                     reestr.objects.get(id=id).executor_name.first_name})
    else:
        return render(request, 'employeeLog.html')

def boss2(request, id):
    if request.user.groups.filter(name='Руководитель').exists():
        if request.method == 'POST':
            form = GIPform2(reestr.objects.get(id=id), request.POST or None)
            db_form = reestr.objects.get(id=id)
            if form.is_valid():
                db_form.executor_fail_name = form.cleaned_data.get('executor_fail_name')
                db_form.executor_name = form.cleaned_data.get('executor_name')
                db_form.labor_costs_plan = form.cleaned_data.get('labor_costs_plan')
                db_form.comment = form.cleaned_data.get('comment')
                db_form.answer_remark = form.cleaned_data.get('answer_remark')
                db_form.total_importance = form.cleaned_data.get('total_importance')
                db_form.root_cause_list = form.cleaned_data.get('root_cause_list')
                db_form.answer_date_plan = form.cleaned_data.get('answer_date_plan')
                db_form.answer_deadline_correct_plan = form.cleaned_data.get('answer_deadline_correct_plan')
                db_form.save(update_fields=['executor_fail_name', 'executor_name',
                                                'answer_date_plan', 'answer_deadline_correct_plan', 'labor_costs_plan',
                                                'comment', 'answer_remark', 'total_importance', 'root_cause_list'])
            else:
                return render(request, 'boss2.html', {'form': form,
                                                      'gipcontext':
                                                          reestr.objects.get(id=id).gip.last_name + ' ' +
                                                          reestr.objects.get(id=id).gip.first_name,
                                                      'rescontext':
                                                          reestr.objects.get(
                                                              id=id).responsibleTrouble_name.last_name + ' ' +
                                                          reestr.objects.get(id=id).responsibleTrouble_name.first_name,
                                                      })
        else:
            form = GIPform2(reestr.objects.get(id=id))
        return render(request, 'boss2.html', {'form': form,
                                              'gipcontext':
                                                  reestr.objects.get(id=id).gip.last_name + ' ' +
                                                  reestr.objects.get(id=id).gip.first_name,
                                              'rescontext':
                                                  reestr.objects.get(id=id).responsibleTrouble_name.last_name + ' ' +
                                                  reestr.objects.get(id=id).responsibleTrouble_name.first_name,
                                              })
    else:
        return render(request, 'bosslog.html')

def gip2(request, id):
    if request.user.groups.filter(name='ГИП').exists():
        if request.method == 'POST':
            form = GIPform2(reestr.objects.get(id=id), request.POST or None)
            db_form = reestr.objects.get(id=id)
            if form.is_valid():
                db_form.remark_name = form.cleaned_data.get('remark_name')
                db_form.rational = form.cleaned_data.get('rational')
                db_form.designation_name = form.cleaned_data.get('designation_name')
                db_form.section_name = form.cleaned_data.get('section_name')
                db_form.responsibleTrouble_name = form.cleaned_data.get('responsibleTrouble_name')
                db_form.executor_fail_name = form.cleaned_data.get('executor_fail_name')
                db_form.executor_name = form.cleaned_data.get('executor_name')
                db_form.labor_costs_plan = form.cleaned_data.get('labor_costs_plan')
                db_form.comment = form.cleaned_data.get('comment')
                db_form.answer_remark = form.cleaned_data.get('answer_remark')
                db_form.total_importance = form.cleaned_data.get('total_importance')
                db_form.root_cause_list = form.cleaned_data.get('root_cause_list')
                db_form.answer_date_plan = form.cleaned_data.get('answer_date_plan')
                db_form.answer_deadline_correct_plan = form.cleaned_data.get('answer_deadline_correct_plan')
                db_form.save(update_fields=['remark_name', 'rational', 'designation_name', 'section_name',
                                                'responsibleTrouble_name', 'executor_fail_name', 'executor_name',
                                                'answer_date_plan', 'answer_deadline_correct_plan', 'labor_costs_plan',
                                                'comment', 'answer_remark', 'total_importance', 'root_cause_list'])
            else:
                return render(request, 'GIP2.html', {'form': form,
                                                     'gipcontext':
                                                         reestr.objects.get(id=id).gip.last_name + ' ' +
                                                         reestr.objects.get(id=id).gip.first_name,
                                                     })
        else:
            form = GIPform2(reestr.objects.get(id=id))
        return render(request, 'GIP2.html', {'form': form,
                                             'gipcontext':
                                                 reestr.objects.get(id=id).gip.last_name + ' ' +
                                                 reestr.objects.get(id=id).gip.first_name,
                                             })
    else:
        return render(request, 'GIPlog.html')

def final(request, id):
    if request.user.groups.filter(name='Руководитель').exists():
        if request.method == 'POST':
            form = FinalForm(reestr.objects.get(id=id), request.POST or None)
            db_form = reestr.objects.get(id=id)
            if form.is_valid():
                db_form.labor_costs_fact = form.cleaned_data.get('labor_costs_fact')
                db_form.answer_remark = form.cleaned_data.get('answer_remark')
                db_form.link_tech_name = form.cleaned_data.get('link_tech_name')

                answer_date = form.cleaned_data.get('answer_date_fact')
                answer_deadline = form.cleaned_data.get('answer_deadline_correct_fact')
                if answer_date and answer_deadline:
                    db_form.answer_date_fact = answer_date
                    db_form.answer_deadline_correct_fact = answer_deadline
                    db_form.save(update_fields=['labor_costs_fact', 'answer_remark', 'link_tech_name', 'answer_date_fact',
                                                'answer_deadline_correct_fact'])
                if answer_date is None:
                    form.add_error('answer_date_fact', 'Пожалуйста, внесите данные')
                if answer_deadline is None:
                    form.add_error('answer_deadline_correct_fact', 'Пожалуйста, внесите данные')
            else:
                print('invalid')
                answer_date = form.cleaned_data.get('answer_date_fact')
                answer_deadline = form.cleaned_data.get('answer_deadline_correct_fact')
                if answer_date is None:
                    form.add_error('answer_date_fact', 'Пожалуйста, внесите данные')
                if answer_deadline is None:
                    form.add_error('answer_deadline_correct_fact', 'Пожалуйста, внесите данные')
                return render(request, 'final.html', {'form': form})
        else:
            form = FinalForm(reestr.objects.get(id=id))
        return render(request, 'final.html', {'form': form,
                                              'gipcontext':
                                                     reestr.objects.get(id=id).gip.last_name + ' ' +
                                                     reestr.objects.get(id=id).gip.first_name,
                                              'rescontext':
                                                     reestr.objects.get(id=id).responsibleTrouble_name.last_name + ' ' +
                                                     reestr.objects.get(id=id).responsibleTrouble_name.first_name,
                                              'exfcontext':
                                                     reestr.objects.get(id=id).executor_fail_name.last_name + ' ' +
                                                     reestr.objects.get(id=id).executor_fail_name.first_name,
                                              'excontext':
                                                     reestr.objects.get(id=id).executor_name.last_name + ' ' +
                                                     reestr.objects.get(id=id).executor_name.first_name})
    else:
        return render(request, 'bossLog.html')

def close(request, id):
    if request.user.groups.filter(name='ГИП').exists():
        if request.method == 'POST':
            form = CloseForm(reestr.objects.get(id=id), request.POST or None)
            db_form = reestr.objects.get(id=id)
            if form.is_valid():
                cancel_remark = form.cleaned_data.get('cancel_remark')
                if cancel_remark is None:
                    form.add_error('cancel_remark', 'Пожалуйста, внесите данные')
                else:
                    db_form.cancel_remark = cancel_remark
                    db_form.save(update_fields=['cancel_remark'])
            else:
                cancel_remark = form.cleaned_data.get('cancel_remark')
                if cancel_remark is None:
                    form.add_error('cancel_remark', 'Пожалуйста, внесите данные')
                return render(request, 'close.html', {'form': form})
        else:
            form = CloseForm(reestr.objects.get(id=id))
        return render(request, 'close.html', {'form': form,
                                              'gipcontext':
                                                  reestr.objects.get(id=id).gip.last_name + ' ' +
                                                  reestr.objects.get(id=id).gip.first_name,
                                              'rescontext':
                                                  reestr.objects.get(id=id).responsibleTrouble_name.last_name + ' ' +
                                                  reestr.objects.get(id=id).responsibleTrouble_name.first_name,
                                              'exfcontext':
                                                  reestr.objects.get(id=id).executor_fail_name.last_name + ' ' +
                                                  reestr.objects.get(id=id).executor_fail_name.first_name,
                                              'excontext':
                                                  reestr.objects.get(id=id).executor_name.last_name + ' ' +
                                                  reestr.objects.get(id=id).executor_name.first_name})
    else:
        return render(request, 'GIPlog.html')


