from django import forms
from formapp.models import reestr, reestInfo, files
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import date, timedelta
import os

def getHumanReadable(size):
    suffixes = [' Б', ' КБ', ' МБ', ' ГБ', ' ТБ']
    suffixIndex = 0
    while size > 1024:
        suffixIndex += 1 #increment the index of the suffix
        size = float('{:.2f}'.format(size/1024.0)) #apply the division
    return str(size) + suffixes[suffixIndex]

def workDays(day, delay):
    k = 0
    while k < delay:
        day += timedelta(days=1)
        if day.weekday() < 5:
            k+=1
    return day

class FileForm(forms.ModelForm):
    class Meta:
        model = files
        fields = ('file', 'file_name', 'comment')
        widgets = {
            'file': forms.ClearableFileInput(attrs={"multiple": True}),
            'file_name': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'comment': forms.Textarea(attrs={'class': 'form-textinput', 'autocomplete': 'off'})
        }
    def save_files(self, reestr, name, comment):
        for upload in self.files.getlist("file"):
            add_file = files(reestr=reestr, file=upload, upload_date=date.today(), file_name=name, comment=comment,
                             file_size=getHumanReadable(upload.size), belong_to=reestr.project_dogovor[4:9]+reestr.num_reestr)
            add_file.save()

class ReestrForm(forms.ModelForm):
    class Meta:
        model = reestInfo
        fields = ('customer', 'gip', 'project_dogovor', 'project_date_contract', 'project_name', 'project_reviewer',
                  'out_mail_num', 'out_mail_date', 'in_mail_num', 'in_mail_date',  'num_reestr', 'start_date', 'end_date', 'step')
        error_messages = {
            'customer': {'required': 'Пожалуйста, внесите данные', },
            'project_dogovor': {'required': 'Пожалуйста, внесите данные', },
            'project_name': {'required': 'Пожалуйста, внесите данные', },
            'project_reviewer': {'required': 'Пожалуйста, внесите данные', },
            'out_mail_num': {'required': 'Пожалуйста, внесите данные', },
            'in_mail_num': {'required': 'Пожалуйста, внесите данные', },
            'num_reestr': {'required': 'Пожалуйста, внесите данные', },
        }
        widgets = {
            'customer': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'project_dogovor': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'project_date_contract': forms.SelectDateWidget(attrs={'class': 'form-dateinput'}, years=range(1980, date.today().year+1)),
            'project_name': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'project_reviewer': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'out_mail_num': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'out_mail_date': forms.SelectDateWidget(attrs={'class': 'form-dateinput'}, years=range(1980, date.today().year+1)),
            'in_mail_num': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'in_mail_date': forms.SelectDateWidget(attrs={'class': 'form-dateinput'}, years=range(1980, date.today().year+1)),
            'num_reestr': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'start_date': forms.DateInput(attrs={'value': date.today()}),
            'end_date': forms.DateInput(attrs={'value': workDays(date.today(), 10)}),
        }

    gip = forms.ModelChoiceField(queryset=User.objects.filter(groups=1), empty_label='-----',
                                 widget=forms.Select(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
                                 error_messages={'required': 'Пожалуйста, внесите данные'})
    add_files = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}),
                            required=False)
    file_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}), required=False)
    file_comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-textinput', 'autocomplete': 'off'}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['step'].initial = 1

    def save_files(self, reestr, name, comment):
        for upload in self.files.getlist("file"):
            add_file = files(reestr=reestr, file=upload, upload_date=date.today(), file_name=name, comment=comment,
                             file_size=getHumanReadable(upload.size),
                             belong_to=reestr.project_dogovor[4:9] + reestr.num_reestr)
            add_file.save()


class GIPform(forms.ModelForm):
    class Meta:

        model = reestr
        fields = ('reestrID', 'customer', 'gip', 'responsibleTrouble_name', 'project_dogovor', 'project_date_contract', 'project_name', 'project_reviewer',
                  'out_mail_num', 'out_mail_date', 'in_mail_num', 'in_mail_date',  'num_reestr', 'num_remark',
                  'remark_v', 'remark_name', 'rational', 'designation_name', 'section_name',
                  'executor_fail_name', 'executor_name', 'answer_date_plan', 'answer_deadline_correct_plan',
                  'labor_costs_plan', 'comment', 'answer_remark', 'total_importance', 'root_cause_list')
        error_messages = {
            'customer': {'required': 'Пожалуйста, внесите данные', },
            'project_dogovor': {'required': 'Пожалуйста, внесите данные', },
            'project_name': {'required': 'Пожалуйста, внесите данные', },
            'gip': {'required': 'Пожалуйста, внесите данные', },
            'project_reviewer': {'required': 'Пожалуйста, внесите данные', },
            'out_mail_num': {'required': 'Пожалуйста, внесите данные', },
            'in_mail_num': {'required': 'Пожалуйста, внесите данные', },
            'num_reestr': {'required': 'Пожалуйста, внесите данные', },
            'num_remark': {'required': 'Пожалуйста, внесите данные', },
            'remark_name': {'required': 'Пожалуйста, внесите данные', },
            'rational': {'required': 'Пожалуйста, внесите данные', },
            'designation_name': {'required': 'Пожалуйста, внесите данные', },
            'section_name': {'required': 'Пожалуйста, внесите данные', },
            'responsibleTrouble_name': {'required': 'Пожалуйста, внесите данные', },
            'executor_fail_name': {'required': ""},
            'executor_name': {'required': ""},
            'answer_date_plan': {'required': ""},
            'answer_deadline_correct_plan': {'required': ""},
            'labor_costs_plan': {'required': ""},
            'comment': {'required': ""},
            'total_importance': {'required': ""},
            'root_cause_list': {'required': ""},
        }
        widgets = {
            'customer': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'project_dogovor': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'project_date_contract': forms.SelectDateWidget(attrs={'class': 'form-dateinput'}, years=range(1980, date.today().year+1)),
            'project_name': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            # 'gip': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'project_reviewer': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'out_mail_num': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'out_mail_date': forms.SelectDateWidget(attrs={'class': 'form-dateinput'}, years=range(1980, date.today().year+1)),
            'in_mail_num': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'in_mail_date': forms.SelectDateWidget(attrs={'class': 'form-dateinput'}, years=range(1980, date.today().year+1)),
            'num_reestr': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'num_remark': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'remark_v': forms.NumberInput(attrs={'class': 'form-readonly', 'id': 'remark_v'}),
            'remark_name': forms.Textarea(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'rational': forms.Textarea(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'designation_name': forms.TextInput(attrs={'class': 'form-textinput', 'title': 'Пример: ТХ', 'autocomplete': 'off'}),
            'section_name': forms.TextInput(attrs={'class': 'form-textinput', 'title': 'Пример: 099-3053-1001624-ТХ', 'autocomplete': 'off'}),
            # 'responsibleTrouble_name': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            #
            # 'executor_fail_name': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            # 'executor_name': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),

            'answer_date_plan': forms.SelectDateWidget(attrs={'class': 'form-dateinput', 'empty_label': "---"},
                                                       years=range(1980, date.today().year + 2)),
            'answer_deadline_correct_plan': forms.SelectDateWidget(
                attrs={'class': 'form-dateinput', 'empty_label': "---"}, years=range(1980, date.today().year + 2)),
            'labor_costs_plan': forms.NumberInput(
                attrs={'id': 'labor_costs_plan', 'class': 'form-textinput', 'step': '0.25', 'min': '0',
                       'autocomplete': 'off'}),
            'comment': forms.Textarea(
                attrs={'class': 'form-textinput', 'title': 'Указывается информация о статусе замечания',
                       'autocomplete': 'off', 'id': 'comment'}),
            'answer_remark': forms.Textarea(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'total_importance': forms.TextInput(
                attrs={'class': 'form-importance', 'readonly': 'readonly', 'placeholder': '', 'id': 'total_imp'}),
            'root_cause_list': forms.TextInput(
                attrs={'class': 'form-textinput', 'hidden': 'hidden', 'id': 'root_cause'})
        }

    gip = forms.ModelChoiceField(queryset=User.objects.filter(groups=1), empty_label='-----',
                                 widget=forms.Select(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
                                 error_messages={'required': 'Пожалуйста, внесите данные'})
    responsibleTrouble_name = forms.ModelChoiceField(queryset=User.objects.filter((Q(groups=1) | Q(groups=2))), empty_label='-----',
                                 widget=forms.Select(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
                                 error_messages={'required': 'Пожалуйста, внесите данные'})

    executor_fail_name = forms.ModelChoiceField(queryset=User.objects.filter((Q(groups=1) | Q(groups=2) | Q(groups=3))),
                                                empty_label='-----',
                                                widget=forms.Select(
                                                    attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
                                                error_messages={'required': ''}, required=False)
    executor_name = forms.ModelChoiceField(queryset=User.objects.filter((Q(groups=1) | Q(groups=2) | Q(groups=3))),
                                           empty_label='-----',
                                           widget=forms.Select(
                                               attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
                                           error_messages={'required': ''}, required=False)
    add_files = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}),
                                required=False)
    file_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
                                required=False)
    file_comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
                                   required=False)
    def __init__(self, reest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # reest = reestr.objects.all()
        # reest = reestr.objects.all().last()
        self.fields['reestrID'].initial = reest.id
        self.fields['customer'].initial = reest.customer
        self.fields['project_dogovor'].initial = reest.project_dogovor
        self.fields['project_date_contract'].initial = reest.project_date_contract
        self.fields['project_name'].initial = reest.project_name
        self.fields['gip'].initial = reest.gip
        self.fields['project_reviewer'].initial = reest.project_reviewer
        self.fields['out_mail_num'].initial = reest.out_mail_num
        self.fields['out_mail_date'].initial = reest.out_mail_date
        self.fields['in_mail_num'].initial = reest.in_mail_num
        self.fields['in_mail_date'].initial = reest.in_mail_date
        self.fields['num_reestr'].initial = reest.num_reestr

    def save_files(self, reestr, name, comment, remark):
        for upload in self.files.getlist("add_files"):
            add_file = files(reestr=reestr, file=upload, upload_date=date.today(), file_name=name, comment=comment,
                             file_size=getHumanReadable(upload.size),
                             belong_to=reestr.project_dogovor[4:9] + reestr.num_reestr + "/"+remark)
            add_file.save()

class BossForm1(forms.ModelForm):
    class Meta:
        model = reestr
        fields = ('customer', 'project_dogovor', 'project_date_contract', 'project_name', 'project_reviewer',
                  'out_mail_num', 'out_mail_date', 'in_mail_num', 'in_mail_date',  'num_reestr', 'num_remark',
                  'remark_v', 'remark_name', 'rational', 'designation_name', 'section_name',
                  'executor_fail_name', 'executor_name', 'answer_date_plan', 'answer_deadline_correct_plan',
                  'labor_costs_plan', 'comment', 'answer_remark', 'total_importance', 'root_cause_list')
        error_messages = {
            'executor_fail_name': {'required': "Пожалуйста, внесите данные"},
            'executor_name': {'required': "Пожалуйста, внесите данные"},
            'answer_date_plan': {'required': "Пожалуйста, внесите данные"},
            'answer_deadline_correct_plan': {'required': "Пожалуйста, внесите данные"},
            'labor_costs_plan': {'required': ""},
            'comment': {'required': ""},
            'total_importance': {'required': ""},
            'root_cause_list': {'required': ""},
        }
        widgets = {
            'customer': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_dogovor': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_date_contract': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_name': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_reviewer': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'out_mail_num': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'out_mail_date': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'in_mail_num': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'in_mail_date': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'num_reestr': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'num_remark': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'remark_v': forms.NumberInput(attrs={'class': 'form-readonly', 'id': 'remark_v', 'readonly': 'readonly'}),
            'remark_name': forms.Textarea(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'rational': forms.Textarea(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'designation_name': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly', 'title': 'Пример: ТХ'}),
            'section_name': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly', 'title':'Пример: 099-3053-1001624-ТХ'}),
            'add_files': forms.ClearableFileInput(),

            'executor_fail_name': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'executor_name': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),

            'answer_date_plan': forms.SelectDateWidget(attrs={'class': 'form-dateinput', 'empty_label': "---"},years=range(1980, date.today().year+2)),
            'answer_deadline_correct_plan': forms.SelectDateWidget(attrs={'class': 'form-dateinput', 'empty_label': "---"},years=range(1980, date.today().year+2)),
            'labor_costs_plan': forms.NumberInput(attrs={'id': 'labor_costs_plan', 'class': 'form-textinput', 'step': '0.25', 'min': '0', 'autocomplete': 'off'}),
            'comment': forms.Textarea(attrs={'class': 'form-textinput', 'title': 'Указывается информация о статусе замечания',
                                             'autocomplete': 'off', 'id': 'comment'}),
            'answer_remark': forms.Textarea(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'total_importance': forms.TextInput(attrs={'class': 'form-importance', 'readonly': 'readonly', 'placeholder': '', 'id': 'total_imp'}),
            'root_cause_list': forms.TextInput(attrs={'class': 'form-textinput', 'hidden': 'hidden', 'id': 'root_cause'})
        }
        # widgets['add_files'].clear_checkbox_label = ''
        # widgets['add_files'].input_text = ''

    executor_fail_name = forms.ModelChoiceField(queryset=User.objects.filter((Q(groups=2) | Q(groups=3))), empty_label='-----',
                                                     widget=forms.Select(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
                                                     error_messages={'required': 'Пожалуйста, внесите данные'})
    executor_name = forms.ModelChoiceField(queryset=User.objects.filter((Q(groups=2) | Q(groups=3))),
                                                empty_label='-----',
                                                widget=forms.Select(
                                                    attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
                                                error_messages={'required': 'Пожалуйста, внесите данные'})

    def __init__(self, reest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # reest = reestr.objects.all()
        # reest = reestr.objects.all().last()
        self.fields['customer'].initial = reest.customer
        self.fields['project_dogovor'].initial = reest.project_dogovor
        self.fields['project_date_contract'].initial = reest.project_date_contract
        self.fields['project_name'].initial = reest.project_name
        self.fields['project_reviewer'].initial = reest.project_reviewer
        self.fields['out_mail_num'].initial = reest.out_mail_num
        self.fields['out_mail_date'].initial = reest.out_mail_date
        self.fields['in_mail_num'].initial = reest.in_mail_num
        self.fields['in_mail_date'].initial = reest.in_mail_date
        self.fields['num_reestr'].initial = reest.num_reestr
        self.fields['num_remark'].initial = reest.num_remark
        self.fields['remark_v'].initial = reest.remark_v
        self.fields['remark_name'].initial = reest.remark_name
        self.fields['rational'].initial = reest.rational
        self.fields['designation_name'].initial = reest.designation_name
        self.fields['section_name'].initial = reest.section_name

        if reest.executor_fail_name:
            self.fields['executor_fail_name'].initial = reest.executor_fail_name
        if reest.executor_name:
            self.fields['executor_name'].initial = reest.executor_name

class emplForm(forms.ModelForm):
    class Meta:
        model = reestr
        fields = ('customer', 'project_dogovor', 'project_date_contract', 'project_name', 'project_reviewer',
                  'out_mail_num', 'out_mail_date', 'in_mail_num', 'in_mail_date',  'num_reestr', 'num_remark',
                  'remark_v', 'remark_name', 'rational', 'designation_name', 'section_name',
                  'answer_date_plan', 'answer_deadline_correct_plan',
                  'labor_costs_plan', 'comment', 'answer_remark', 'total_importance', 'root_cause_list')
        error_messages = {
            'answer_date_plan': {'required': "Пожалуйста, внесите данные"},
            'answer_deadline_correct_plan': {'required': "Пожалуйста, внесите данные"},
            'labor_costs_plan': {'required': "Пожалуйста, внесите данные"},
            'comment': {'required': "Пожалуйста, внесите данные"},
            'answer_remark': {'required': "Пожалуйста, внесите данные"},
            'total_importance': {'required': "Пожалуйста, внесите данные"},
            'root_cause_list': {'required': "Пожалуйста, внесите данные"},
        }
        widgets = {
            'customer': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_dogovor': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_date_contract': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_name': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_reviewer': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'out_mail_num': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'out_mail_date': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'in_mail_num': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'in_mail_date': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'num_reestr': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'num_remark': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'remark_v': forms.NumberInput(attrs={'class': 'form-readonly', 'id': 'remark_v', 'readonly': 'readonly'}),
            'remark_name': forms.Textarea(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'rational': forms.Textarea(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'designation_name': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly', 'title': 'Пример: ТХ'}),
            'section_name': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly', 'title':'Пример: 099-3053-1001624-ТХ'}),
            'add_files': forms.ClearableFileInput(),

            'answer_date_plan': forms.SelectDateWidget(attrs={'class': 'form-dateinput'}, years=range(1980, date.today().year+2)),
            'answer_deadline_correct_plan': forms.SelectDateWidget(attrs={'class': 'form-dateinput', 'empty_label': "---"},years=range(1980, date.today().year+2)),
            'labor_costs_plan': forms.NumberInput(attrs={'minlength': 3, 'required': 'required', 'class': 'form-textinput', 'step': '0.25', 'min': '0', 'autocomplete': 'off'}),
            'comment': forms.Textarea(attrs={'required': 'required', 'class': 'form-textinput', 'title': 'Указывается информация о статусе замечания', 'autocomplete': 'off'}),
            'answer_remark': forms.Textarea(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'total_importance': forms.TextInput(attrs={'required': 'required', 'class': 'form-importance', 'readonly': 'readonly', 'placeholder': '', 'id': 'total_imp'}),
            'root_cause_list': forms.TextInput(attrs={'required': 'required', 'class': 'form-textinput', 'hidden': 'hidden', 'id': 'root_cause'})
        }

    def __init__(self, reest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].initial = reest.customer
        self.fields['project_dogovor'].initial = reest.project_dogovor
        self.fields['project_date_contract'].initial = reest.project_date_contract
        self.fields['project_name'].initial = reest.project_name
        self.fields['project_reviewer'].initial = reest.project_reviewer
        self.fields['out_mail_num'].initial = reest.out_mail_num
        self.fields['out_mail_date'].initial = reest.out_mail_date
        self.fields['in_mail_num'].initial = reest.in_mail_num
        self.fields['in_mail_date'].initial = reest.in_mail_date
        self.fields['num_reestr'].initial = reest.num_reestr
        self.fields['num_remark'].initial = reest.num_remark
        self.fields['remark_v'].initial = reest.remark_v
        self.fields['remark_name'].initial = reest.remark_name
        self.fields['rational'].initial = reest.rational
        self.fields['designation_name'].initial = reest.designation_name
        self.fields['section_name'].initial = reest.section_name

        if reest.answer_date_plan:
            self.fields['answer_date_plan'].initial = reest.answer_date_plan
        if reest.answer_deadline_correct_plan:
            self.fields['answer_deadline_correct_plan'].initial = reest.answer_deadline_correct_plan
        if reest.labor_costs_plan:
            self.fields['labor_costs_plan'].initial = reest.labor_costs_plan
        if reest.comment:
            self.fields['comment'].initial = reest.comment
        if reest.answer_remark:
            self.fields['answer_remark'].initial = reest.answer_remark
        if reest.total_importance:
            self.fields['total_importance'].initial = reest.total_importance
        if reest.root_cause_list:
            self.fields['root_cause_list'].initial = reest.root_cause_list


class GIPform2(forms.ModelForm):
    class Meta:
        model = reestr
        fields = ('customer', 'project_dogovor', 'project_date_contract', 'project_name', 'project_reviewer',
                  'out_mail_num', 'out_mail_date', 'in_mail_num', 'in_mail_date',  'num_reestr', 'num_remark',
                  'remark_v', 'remark_name', 'rational', 'designation_name', 'section_name', 'responsibleTrouble_name',
                  'executor_fail_name', 'executor_name', 'answer_date_plan', 'answer_deadline_correct_plan',
                  'labor_costs_plan', 'comment', 'answer_remark', 'total_importance', 'root_cause_list', 'reestrID', 'gip')
        error_messages = {
            'remark_name': {'required': 'Пожалуйста, внесите данные', },
            'rational': {'required': 'Пожалуйста, внесите данные', },
            'designation_name': {'required': 'Пожалуйста, внесите данные', },
            'section_name': {'required': 'Пожалуйста, внесите данные', },
            'responsibleTrouble_name': {'required': 'Пожалуйста, внесите данные', },
            'executor_fail_name': {'required': "Пожалуйста, внесите данные"},
            'executor_name': {'required': "Пожалуйста, внесите данные"},
            'answer_date_plan': {'required': "Пожалуйста, внесите данные"},
            'answer_deadline_correct_plan': {'required': "Пожалуйста, внесите данные"},
            'labor_costs_plan': {'required': "Пожалуйста, внесите данные"},
            'comment': {'required': "Пожалуйста, внесите данные"},
            'answer_remark': {'required': "Пожалуйста, внесите данные"},
            'total_importance': {'required': "Пожалуйста, внесите данные"},
            'root_cause_list': {'required': "Пожалуйста, внесите данные"},
        }
        widgets = {
            'customer': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_dogovor': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_date_contract': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_name': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_reviewer': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'out_mail_num': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'out_mail_date': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'in_mail_num': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'in_mail_date': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'num_reestr': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'num_remark': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'remark_v': forms.NumberInput(attrs={'class': 'form-readonly', 'id': 'remark_v', 'readonly': 'readonly'}),
            'remark_name': forms.Textarea(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'rational': forms.Textarea(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'designation_name': forms.TextInput(attrs={'class': 'form-textinput', 'title': 'Пример: ТХ', 'autocomplete': 'off'}),
            'section_name': forms.TextInput(attrs={'class': 'form-textinput', 'title':'Пример: 099-3053-1001624-ТХ', 'autocomplete': 'off'}),

            'answer_date_plan': forms.DateInput(attrs={'class': 'form-textinput', 'autocomplete': 'off', 'required': 'required'}),
            'answer_deadline_correct_plan': forms.DateInput(attrs={'class': 'form-textinput', 'empty_label': "---", 'autocomplete': 'off', 'required': 'required'}),
            'labor_costs_plan': forms.NumberInput(attrs={'class': 'form-textinput', 'autocomplete': 'off', 'required': 'required'}),
            'comment': forms.Textarea(attrs={'class': 'form-textinput', 'title': 'Указывается информация о статусе замечания', 'autocomplete': 'off', 'required': 'required'}),
            'answer_remark': forms.Textarea(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'total_importance': forms.TextInput(attrs={'class': 'form-textinput',
                                                       'placeholder': '', 'id': 'total_imp', 'autocomplete': 'off', 'required': 'required'}),
            'root_cause_list': forms.TextInput(attrs={'class': 'form-textinput', 'hidden': 'hidden', 'id': 'root_cause', 'autocomplete': 'off', 'required': 'required'})
        }

    responsibleTrouble_name = forms.ModelChoiceField(queryset=User.objects.filter((Q(groups=1) | Q(groups=2))),
                                                     empty_label='-----',
                                                     widget=forms.Select(
                                                         attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
                                                     error_messages={'required': 'Пожалуйста, внесите данные'})

    executor_fail_name = forms.ModelChoiceField(queryset=User.objects.filter((Q(groups=1) | Q(groups=2) | Q(groups=3))),
                                                empty_label='-----',
                                                widget=forms.Select(
                                                    attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
                                                error_messages={'required': 'Пожалуйста, внесите данные'})
    executor_name = forms.ModelChoiceField(queryset=User.objects.filter((Q(groups=1) | Q(groups=2) | Q(groups=3))),
                                           empty_label='-----',
                                           widget=forms.Select(
                                               attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
                                           error_messages={'required': 'Пожалуйста, внесите данные'})

    def __init__(self, reest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # reest = reestr.objects.all()
        # reest = reestr.objects.all().last()
        self.fields['customer'].initial = reest.customer
        self.fields['project_dogovor'].initial = reest.project_dogovor
        self.fields['project_date_contract'].initial = reest.project_date_contract
        self.fields['project_name'].initial = reest.project_name
        self.fields['project_reviewer'].initial = reest.project_reviewer
        self.fields['out_mail_num'].initial = reest.out_mail_num
        self.fields['out_mail_date'].initial = reest.out_mail_date
        self.fields['in_mail_num'].initial = reest.in_mail_num
        self.fields['in_mail_date'].initial = reest.in_mail_date
        self.fields['num_reestr'].initial = reest.num_reestr
        self.fields['num_remark'].initial = reest.num_remark
        self.fields['remark_v'].initial = reest.remark_v
        self.fields['remark_name'].initial = reest.remark_name
        self.fields['rational'].initial = reest.rational
        self.fields['designation_name'].initial = reest.designation_name
        self.fields['section_name'].initial = reest.section_name
        self.fields['answer_date_plan'].initial = reest.answer_date_plan
        self.fields['answer_deadline_correct_plan'].initial = reest.answer_deadline_correct_plan
        self.fields['labor_costs_plan'].initial = reest.labor_costs_plan
        self.fields['comment'].initial = reest.comment
        self.fields['answer_remark'].initial = reest.answer_remark
        self.fields['total_importance'].initial = reest.total_importance
        self.fields['root_cause_list'].initial = reest.root_cause_list

        self.fields['reestrID'].initial = reest.reestrID
        self.fields['gip'].initial = reest.gip

        if reest.responsibleTrouble_name:
            self.fields['responsibleTrouble_name'].initial = reest.responsibleTrouble_name
        if reest.executor_fail_name:
            self.fields['executor_fail_name'].initial = reest.executor_fail_name
        if reest.executor_name:
            self.fields['executor_name'].initial = reest.executor_name

class BossForm2(forms.ModelForm):
    class Meta:
        model = reestr
        fields = ('customer', 'project_dogovor', 'project_date_contract', 'project_name', 'project_reviewer',
                  'out_mail_num', 'out_mail_date', 'in_mail_num', 'in_mail_date',  'num_reestr', 'num_remark',
                  'remark_v', 'remark_name', 'rational', 'designation_name', 'section_name',
                  'executor_fail_name', 'executor_name', 'answer_date_plan', 'answer_deadline_correct_plan',
                  'labor_costs_plan', 'comment', 'answer_remark', 'total_importance', 'root_cause_list',
                  'responsibleTrouble_name', 'gip', 'reestrID')
        error_messages = {
            'remark_name': {'required': 'Пожалуйста, внесите данные', },
            'rational': {'required': 'Пожалуйста, внесите данные', },
            'designation_name': {'required': 'Пожалуйста, внесите данные', },
            'section_name': {'required': 'Пожалуйста, внесите данные', },
            'responsibleTrouble_name': {'required': 'Пожалуйста, внесите данные', },
            'executor_fail_name': {'required': "Пожалуйста, внесите данные"},
            'executor_name': {'required': "Пожалуйста, внесите данные"},
            'answer_date_plan': {'required': "Пожалуйста, внесите данные"},
            'answer_deadline_correct_plan': {'required': "Пожалуйста, внесите данные"},
            'labor_costs_plan': {'required': "Пожалуйста, внесите данные"},
            'comment': {'required': "Пожалуйста, внесите данные"},
            'answer_remark': {'required': "Пожалуйста, внесите данные"},
            'total_importance': {'required': "Пожалуйста, внесите данные"},
            'root_cause_list': {'required': "Пожалуйста, внесите данные"},
        }
        widgets = {
            'customer': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_dogovor': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_date_contract': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_name': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_reviewer': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'out_mail_num': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'out_mail_date': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'in_mail_num': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'in_mail_date': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'num_reestr': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'num_remark': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'remark_v': forms.NumberInput(attrs={'class': 'form-readonly', 'id': 'remark_v', 'readonly': 'readonly'}),
            'remark_name': forms.Textarea(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'rational': forms.Textarea(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'designation_name': forms.TextInput(attrs={'class': 'form-readonly', 'title': 'Пример: ТХ', 'readonly': 'readonly'}),
            'section_name': forms.TextInput(attrs={'class': 'form-readonly', 'title':'Пример: 099-3053-1001624-ТХ', 'readonly': 'readonly'}),

            'answer_date_plan': forms.DateInput(attrs={'class': 'form-textinput', 'autocomplete': 'off', 'required': 'required'}),
            'answer_deadline_correct_plan': forms.DateInput(attrs={'class': 'form-textinput', 'empty_label': "---", 'autocomplete': 'off', 'required': 'required'}),
            'labor_costs_plan': forms.NumberInput(attrs={'class': 'form-textinput', 'autocomplete': 'off', 'required': 'required'}),
            'comment': forms.Textarea(attrs={'class': 'form-textinput', 'title': 'Указывается информация о статусе замечания', 'autocomplete': 'off', 'required': 'required'}),
            'answer_remark': forms.Textarea(attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
            'total_importance': forms.TextInput(attrs={'class': 'form-textinput',
                                                       'placeholder': '', 'id': 'total_imp', 'autocomplete': 'off', 'required': 'required'}),
            'root_cause_list': forms.TextInput(attrs={'class': 'form-textinput', 'hidden': 'hidden', 'id': 'root_cause', 'autocomplete': 'off', 'required': 'required'})
        }
    executor_fail_name = forms.ModelChoiceField(queryset=User.objects.filter((Q(groups=1) | Q(groups=2) | Q(groups=3))),
                                                empty_label='-----',
                                                widget=forms.Select(
                                                    attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
                                                error_messages={'required': 'Пожалуйста, внесите данные'})
    executor_name = forms.ModelChoiceField(queryset=User.objects.filter((Q(groups=1) | Q(groups=2) | Q(groups=3))),
                                           empty_label='-----',
                                           widget=forms.Select(
                                               attrs={'class': 'form-textinput', 'autocomplete': 'off'}),
                                           error_messages={'required': 'Пожалуйста, внесите данные'})

    def __init__(self, reest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # reest = reestr.objects.all()
        # reest = reestr.objects.all().last()
        self.fields['customer'].initial = reest.customer
        self.fields['project_dogovor'].initial = reest.project_dogovor
        self.fields['project_date_contract'].initial = reest.project_date_contract
        self.fields['project_name'].initial = reest.project_name
        self.fields['project_reviewer'].initial = reest.project_reviewer
        self.fields['out_mail_num'].initial = reest.out_mail_num
        self.fields['out_mail_date'].initial = reest.out_mail_date
        self.fields['in_mail_num'].initial = reest.in_mail_num
        self.fields['in_mail_date'].initial = reest.in_mail_date
        self.fields['num_reestr'].initial = reest.num_reestr
        self.fields['num_remark'].initial = reest.num_remark
        self.fields['remark_v'].initial = reest.remark_v
        self.fields['remark_name'].initial = reest.remark_name
        self.fields['rational'].initial = reest.rational
        self.fields['designation_name'].initial = reest.designation_name
        self.fields['section_name'].initial = reest.section_name
        self.fields['answer_date_plan'].initial = reest.answer_date_plan
        self.fields['answer_deadline_correct_plan'].initial = reest.answer_deadline_correct_plan
        self.fields['labor_costs_plan'].initial = reest.labor_costs_plan
        self.fields['comment'].initial = reest.comment
        self.fields['answer_remark'].initial = reest.answer_remark
        self.fields['total_importance'].initial = reest.total_importance
        self.fields['root_cause_list'].initial = reest.root_cause_list

        self.fields['responsibleTrouble_name'].initial = reest.responsibleTrouble_name
        self.fields['gip'].initial = reest.gip
        self.fields['reestrID'].initial = reest.reestrID

        if reest.executor_fail_name:
            self.fields['executor_fail_name'].initial = reest.executor_fail_name
        if reest.executor_name:
            self.fields['executor_name'].initial = reest.executor_name

class FinalForm(forms.ModelForm):
    class Meta:
        model = reestr
        fields = ('customer', 'project_dogovor', 'project_date_contract', 'project_name', 'project_reviewer',
                  'out_mail_num', 'out_mail_date', 'in_mail_num', 'in_mail_date',  'num_reestr', 'num_remark',
                  'remark_v', 'remark_name', 'rational', 'designation_name', 'section_name', 'answer_date_plan',
                  'answer_date_fact', 'answer_deadline_correct_plan', 'answer_deadline_correct_fact', 'labor_costs_plan',
                  'labor_costs_fact', 'comment', 'answer_remark', 'link_tech_name', 'total_importance', 'root_cause_list')
        error_messages = {
            'answer_date_plan': {'required': "Пожалуйста, внесите данные"},
            'answer_deadline_correct_plan': {'required': "Пожалуйста, внесите данные"},
            'labor_costs_plan': {'required': "Пожалуйста, внесите данные"},
            'answer_date_fact': {'required': "Пожалуйста, внесите данные"},
            'answer_deadline_correct_fact': {'required': "Пожалуйста, внесите данные"},
            'labor_costs_fact': {'required': "Пожалуйста, внесите данные"},
            'answer_remark': {'required': "Пожалуйста, внесите данные"},
            'link_tech_name': {'required': "Пожалуйста, внесите данные"},
        }
        widgets = {
            'customer': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_dogovor': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_date_contract': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_name': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_reviewer': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'out_mail_num': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'out_mail_date': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'in_mail_num': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'in_mail_date': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'num_reestr': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'num_remark': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'remark_v': forms.NumberInput(attrs={'class': 'form-readonly', 'id': 'remark_v', 'readonly': 'readonly'}),
            'remark_name': forms.Textarea(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'rational': forms.Textarea(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'designation_name': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly', 'title': 'Пример: ТХ'}),
            'section_name': forms.TextInput(attrs={'class': 'form-readonly', 'title':'Пример: 099-3053-1001624-ТХ', 'readonly': 'readonly'}),

            'answer_date_plan': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'answer_date_fact': forms.SelectDateWidget(attrs={'class': 'form-dateinput', 'empty_label': "---"}, years=range(1980, date.today().year+2)),
            'answer_deadline_correct_plan': forms.DateInput(attrs={'class': 'form-readonly', 'empty_label': "---", 'readonly': 'readonly'}),
            'answer_deadline_correct_fact': forms.SelectDateWidget(attrs={'class': 'form-dateinput', 'empty_label': "---"}, years=range(1980, date.today().year+2)),
            'labor_costs_plan': forms.NumberInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'labor_costs_fact': forms.NumberInput(attrs={'class': 'form-textinput', 'autocomplete': 'off', 'required': 'required'}),
            'comment': forms.Textarea(attrs={'class': 'form-readonly', 'title': 'Указывается информация о статусе замечания', 'readonly': 'readonly'}),
            'answer_remark': forms.Textarea(attrs={'class': 'form-textinput', 'required': 'required', 'autocomplete': 'off'}),
            'link_tech_name': forms.TextInput(attrs={'class': 'form-textinput', 'autocomplete': 'off', 'required': 'required'}),
            'total_importance': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly',
                                                       'placeholder': '', 'id': 'total_imp'}),
            'root_cause_list': forms.TextInput(attrs={'class': 'form-readonly', 'id': 'root_cause', 'readonly': 'readonly'})
        }

    def __init__(self, reest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # reest = reestr.objects.all()
        # reest = reestr.objects.all().last()
        self.fields['customer'].initial = reest.customer
        self.fields['project_dogovor'].initial = reest.project_dogovor
        self.fields['project_date_contract'].initial = reest.project_date_contract
        self.fields['project_name'].initial = reest.project_name
        self.fields['project_reviewer'].initial = reest.project_reviewer
        self.fields['out_mail_num'].initial = reest.out_mail_num
        self.fields['out_mail_date'].initial = reest.out_mail_date
        self.fields['in_mail_num'].initial = reest.in_mail_num
        self.fields['in_mail_date'].initial = reest.in_mail_date
        self.fields['num_reestr'].initial = reest.num_reestr
        self.fields['num_remark'].initial = reest.num_remark
        self.fields['remark_v'].initial = reest.remark_v
        self.fields['remark_name'].initial = reest.remark_name
        self.fields['rational'].initial = reest.rational
        self.fields['designation_name'].initial = reest.designation_name
        self.fields['section_name'].initial = reest.section_name
        self.fields['answer_date_plan'].initial = reest.answer_date_plan
        self.fields['answer_deadline_correct_plan'].initial = reest.answer_deadline_correct_plan
        self.fields['labor_costs_plan'].initial = reest.labor_costs_plan
        self.fields['comment'].initial = reest.comment
        self.fields['answer_remark'].initial = reest.answer_remark
        self.fields['total_importance'].initial = reest.total_importance
        self.fields['root_cause_list'].initial = reest.root_cause_list

class CloseForm(forms.ModelForm):
    class Meta:
        model = reestr
        fields = ('customer', 'project_dogovor', 'project_date_contract', 'project_name', 'project_reviewer',
                  'out_mail_num', 'out_mail_date', 'in_mail_num', 'in_mail_date',  'num_reestr', 'num_remark',
                  'remark_v', 'remark_name', 'rational', 'designation_name', 'section_name', 'answer_date_plan',
                  'answer_date_fact', 'answer_deadline_correct_plan', 'answer_deadline_correct_fact', 'labor_costs_plan',
                  'labor_costs_fact', 'comment', 'answer_remark', 'link_tech_name', 'cancel_remark', 'total_importance', 'root_cause_list')
        error_messages = {
            'cancel_remark': {'required': "Пожалуйста, внесите данные"},
        }
        widgets = {
            'customer': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_dogovor': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_date_contract': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_name': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'project_reviewer': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'out_mail_num': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'out_mail_date': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'in_mail_num': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'in_mail_date': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'num_reestr': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'num_remark': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'remark_v': forms.NumberInput(attrs={'class': 'form-readonly', 'id': 'remark_v', 'readonly': 'readonly'}),
            'remark_name': forms.Textarea(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'rational': forms.Textarea(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'designation_name': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly', 'title': 'Пример: ТХ'}),
            'section_name': forms.TextInput(attrs={'class': 'form-readonly', 'title':'Пример: 099-3053-1001624-ТХ', 'readonly': 'readonly'}),

            'answer_date_plan': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'answer_date_fact': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'answer_deadline_correct_plan': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'answer_deadline_correct_fact': forms.DateInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'labor_costs_plan': forms.NumberInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'labor_costs_fact': forms.NumberInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'comment': forms.Textarea(attrs={'class': 'form-readonly', 'title': 'Указывается информация о статусе замечания', 'readonly': 'readonly'}),
            'answer_remark': forms.Textarea(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'link_tech_name': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly'}),
            'cancel_remark': forms.SelectDateWidget(attrs={'class': 'form-dateinput', 'empty_label': "---", 'required': 'required'}, years=range(1980, date.today().year+1)),
            'total_importance': forms.TextInput(attrs={'class': 'form-readonly', 'readonly': 'readonly',
                                                       'placeholder': '', 'id': 'total_imp'}),
            'root_cause_list': forms.TextInput(attrs={'class': 'form-readonly', 'id': 'root_cause', 'readonly': 'readonly'})
        }

    def __init__(self, reest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # reest = reestr.objects.all()
        # reest = reestr.objects.all().last()
        self.fields['customer'].initial = reest.customer
        self.fields['project_dogovor'].initial = reest.project_dogovor
        self.fields['project_date_contract'].initial = reest.project_date_contract
        self.fields['project_name'].initial = reest.project_name
        self.fields['project_reviewer'].initial = reest.project_reviewer
        self.fields['out_mail_num'].initial = reest.out_mail_num
        self.fields['out_mail_date'].initial = reest.out_mail_date
        self.fields['in_mail_num'].initial = reest.in_mail_num
        self.fields['in_mail_date'].initial = reest.in_mail_date
        self.fields['num_reestr'].initial = reest.num_reestr
        self.fields['num_remark'].initial = reest.num_remark
        self.fields['remark_v'].initial = reest.remark_v
        self.fields['remark_name'].initial = reest.remark_name
        self.fields['rational'].initial = reest.rational
        self.fields['designation_name'].initial = reest.designation_name
        self.fields['section_name'].initial = reest.section_name
        self.fields['answer_date_plan'].initial = reest.answer_date_plan
        self.fields['answer_deadline_correct_plan'].initial = reest.answer_deadline_correct_plan
        self.fields['labor_costs_plan'].initial = reest.labor_costs_plan
        self.fields['answer_date_fact'].initial = reest.answer_date_fact
        self.fields['answer_deadline_correct_fact'].initial = reest.answer_deadline_correct_fact
        self.fields['labor_costs_fact'].initial = reest.labor_costs_fact
        self.fields['comment'].initial = reest.comment
        self.fields['answer_remark'].initial = reest.answer_remark
        self.fields['link_tech_name'].initial = reest.link_tech_name
        self.fields['total_importance'].initial = reest.total_importance
        self.fields['root_cause_list'].initial = reest.root_cause_list

class ProfileForm(forms.ModelForm):
    class Meta:
        model = reestr
        fields = ('gip', 'num_reestr', 'num_remark', 'remark_name',)
