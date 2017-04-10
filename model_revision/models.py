import json
from decimal import Decimal

import iso8601
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _


def get_field_data(instance):
    data = {}
    for field in instance._meta.get_fields():
        try:
            if not field.is_relation and field.serialize:
                value = field.value_from_object(instance)
                try:
                    # See if value can be serialized by standard JSON encoder
                    json.dumps(value)
                except:
                    # Try encoding this value with DjangoJSONEncoder, but don't double encode
                    value = json.loads(json.dumps(value, cls=DjangoJSONEncoder))
                data[field.get_attname()] = value
        except:
            # exclude this field if an exception is thrown
            pass
    return data


class RevisionQuerySet(models.QuerySet):

    def get_historical_values(self, field, asc=False, include_dates=False):
        if asc:
            qs = self.order_by('created_at')
        else:
            qs = self.order_by('-created_at')

        values = []

        def get_last_value():
            if len(values) == 0:
                return None
            else:
                value = values[-1]
                if type(value) == tuple:
                    return value[0]
                else:
                    return value

        def add_value(revision, value):
            last_value = get_last_value()
            if value != last_value:
                if include_dates:
                    values.append((revision.created_at, value))
                else:
                    values.append(value)

        for revision in qs:
            add_value(revision, revision.get_data().get(field, None))

        return values


class RevisionManager(models.Manager):

    def create_from_instance(self, instance):
        revision = Revision(
            content_object=instance,
            data=get_field_data(instance),
        )
        revision.save()
        return revision

    def get_for_instance(self, instance):
        return self.filter(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk
        )


class Revision(models.Model):
    objects = RevisionManager.from_queryset(RevisionQuerySet)()
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    data = JSONField(db_index=True, null=False, default=dict)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def get_data(self):
        revision_data = {}
        for key, value in self.data.items():
            if value is not None:
                try:
                    field = self.content_object._meta.get_field(key)
                    field_type = type(field)
                    if field_type in (models.DateField, models.TimeField, models.DateTimeField):
                        dt_value = iso8601.parse_date(value)
                        if field_type == models.DateField:
                            revision_data[key] = dt_value.date()
                        elif field_type == models.DateField:
                            revision_data[key] = dt_value.time()
                        else:
                            revision_data[key] = dt_value
                    elif field_type == models.DecimalField:
                        revision_data[key] = Decimal(value)
                except:
                    pass
            else:
                revision_data[key] = value
        return revision_data

    def __str__(self):
        return ugettext('Revision for {} from {}'.format(self.content_object, self.created_at))

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Revision')
        verbose_name_plural = _('Revisions')
