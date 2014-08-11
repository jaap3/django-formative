# -*- coding: utf-8 -*-
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models


class BaseFormBlob(models.Model):
    json_data = models.TextField()

    @property
    def data(self):
        return json.loads(self.json_data)

    @data.setter
    def data(self, value):
        self.json_data = json.dumps(value, cls=DjangoJSONEncoder)

    class Meta:
        abstract = True


class FormBlob(BaseFormBlob):
    unique_identifier = models.CharField(max_length=150, unique=True)
