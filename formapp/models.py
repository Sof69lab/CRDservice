from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_delete, post_save
from changelog.mixins import ChangeloggableMixin
from changelog.signals import journal_save_handler, journal_delete_handler

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/...
    if "/" in instance.belong_to:
        i = len(instance.belong_to)-1
        while instance.belong_to[i] != "/":
            i -= 1
        print(instance.belong_to[i+1:])
        return 'реестр_{0}/{1}/{2}'.format(instance.reestr.project_dogovor[4:9]+instance.reestr.num_reestr, instance.belong_to[i+1:], filename)
    else:
        return 'реестр_{0}/{1}'.format(instance.reestr.project_dogovor[4:9]+instance.reestr.num_reestr, filename)

def get_full_name(self):
    return self.last_name + ' ' + self.first_name

User.add_to_class("__str__", get_full_name)

class reestInfo(ChangeloggableMixin, models.Model):
    class Meta:
        verbose_name = "реестр"
        verbose_name_plural = "Реестры"
    #заголовок
    customer = models.TextField(verbose_name="Заказчик")
    project_dogovor = models.TextField(verbose_name="Договор №")
    project_date_contract = models.DateField(verbose_name="Дата договора", blank=True)
    project_name = models.TextField(verbose_name="Наименование договора")
    gip = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ГИП", related_name='gip_set1')
    project_reviewer = models.TextField(verbose_name="Рецензент")
    out_mail_num = models.TextField(verbose_name="Письмо исх. №")
    out_mail_date = models.DateField(verbose_name="Письмо исх. дата", blank=True)
    in_mail_num = models.TextField(verbose_name="Письмо вх. №")
    in_mail_date = models.DateField(verbose_name="Письмо вх. дата", blank=True)
    # таблица
    num_reestr = models.TextField(verbose_name="1. Реестр №")
    # другое
    start_date = models.DateField(verbose_name="Дата создания")
    end_date = models.DateField(verbose_name="Срок")
    step = models.IntegerField(verbose_name="Этап")
    def __str__(self):
        return f"{self.project_dogovor[4:8]}-{self.num_reestr}"

post_save.connect(journal_save_handler, sender=reestInfo)
post_delete.connect(journal_delete_handler, sender=reestInfo)

class reestr(ChangeloggableMixin, models.Model):
    class Meta:
        verbose_name = "замечание"
        verbose_name_plural = "Замечания"
    reestrID = models.ForeignKey(reestInfo, on_delete=models.CASCADE, verbose_name="ID реестра")
    actuality = models.BooleanField(verbose_name="Актуальность", default=True)
    #ГИП. Формирование реестра
    # заголовок
    customer = models.TextField(verbose_name="Заказчик")
    project_dogovor = models.TextField(verbose_name="Договор №")
    project_date_contract = models.DateField(verbose_name="Дата договора", blank=True)
    project_name = models.TextField(verbose_name="Наименование договора")
    gip = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ГИП", related_name='gip_set')
    project_reviewer = models.TextField(verbose_name="Рецензент")
    out_mail_num = models.TextField(verbose_name="Письмо исх. №")
    out_mail_date = models.DateField(verbose_name="Письмо исх. дата", blank=True)
    in_mail_num = models.TextField(verbose_name="Письмо вх. №")
    in_mail_date = models.DateField(verbose_name="Письмо вх. дата", blank=True)
    # таблица
    num_reestr = models.TextField(verbose_name="1. Реестр №")
    num_remark = models.TextField(verbose_name="1.1. № Замечания")
    remark_v = models.IntegerField(verbose_name="1.2. Версия замечания") #версия замечания
    remark_name = models.TextField(verbose_name="2. Наименование замечания")
    rational = models.TextField(verbose_name="2.1. Обоснование")
    designation_name = models.TextField(verbose_name="3. Обозначение раздела в проекте")
    section_name = models.TextField(verbose_name="4. Наименование раздела")
    responsibleTrouble_name = models.ForeignKey(User, on_delete=models.CASCADE,
                                                verbose_name="5. Ответственный за устранение замечаний (начальник подразделения)",
                                                related_name='responsTroble_set')
    #НП. Заполнение реестра
    executor_fail_name = models.ForeignKey(User, on_delete=models.CASCADE,
                                           verbose_name="6. Исполнитель, допустивший замечание", related_name='executFail_set', blank=True, null=True)
    executor_name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="6.1. Исполнитель, ответственный за устранение замечания",
                                      related_name='execut_set', blank=True, null=True)
    answer_date_plan = models.DateField(verbose_name="7. Дата предоставления ответов на замечания (План)", blank=True, null=True)
    answer_deadline_correct_plan = models.DateField(verbose_name="9. Срок внесения корректировок (План)", blank=True, null=True)
    labor_costs_plan = models.FloatField(verbose_name="10.1 Трудозатраты, дн. (на устранение замечания) (План)", blank=True, null=True)
    comment = models.TextField(verbose_name="10.3. Комментарии", blank=True, null=True)
    answer_remark = models.TextField(verbose_name="11. Ответы на замечания", blank=True, null=True) #не обязательное поле
    total_importance = models.TextField(verbose_name="14. Значимость замечания", blank=True, null=True)
    root_cause_list = models.TextField(verbose_name="15. Коренная причина", blank=True, null=True)
    # подготовка и отправка электронного письма
    #####################################################
    link_tech_name = models.TextField(verbose_name="12. Ссылка  в  технической документации", blank=True, null=True)
    cancel_remark = models.DateField(verbose_name="13. Отметка о снятии замечания, дата", blank=True, null=True)
    answer_date_fact = models.DateField(verbose_name="8. Дата предоставления ответов на замечания (Факт)", blank=True, null=True)
    answer_deadline_correct_fact = models.DateField(verbose_name="10. Срок внесения корректировок (Факт)", blank=True, null=True)
    labor_costs_fact = models.FloatField(verbose_name="10.2. Трудозатраты, дн. (на устранение замечания) (Факт)", blank=True, null=True)
    def __str__(self):
        return f"{self.project_dogovor[4:8]}-{self.num_reestr}/{self.num_remark}/{self.remark_v}"

post_save.connect(journal_save_handler, sender=reestr)
post_delete.connect(journal_delete_handler, sender=reestr)

class files(ChangeloggableMixin, models.Model):
    class Meta:
        verbose_name = "файл"
        verbose_name_plural = "Файлы"
    reestr = models.ForeignKey(reestInfo, on_delete=models.CASCADE, verbose_name="ID реестра")
    belong_to = models.TextField(verbose_name="Принадлежность")
    file = models.FileField(upload_to=user_directory_path, blank=True, null=True, verbose_name="Файл")
    file_name = models.TextField(blank=True, null=True, verbose_name="Наименование документа")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    file_size = models.TextField(blank=True, null=True, verbose_name="Размер файла")
    upload_date = models.DateField(verbose_name="Дата загрузки")
    def __str__(self):
        return f"{self.file}"

post_save.connect(journal_save_handler, sender=files)
post_delete.connect(journal_delete_handler, sender=files)