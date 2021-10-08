from django.core import validators
from django.db import models


class Document(models.Model):
    # docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    docfile = models.FileField(upload_to='documents', validators=[validators.FileExtensionValidator(['jpg','jpeg'], message='文件格式必须是JPG和JPEG')])

