# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from model_revision.signals import pre_save_callback

REVISION_MODELS = []


def register_revisions(model):
    if model not in REVISION_MODELS:
        REVISION_MODELS.append(model)
        pre_save.connect(pre_save_callback, sender=model, dispatch_uid='{}_model_revision_pre_save'.format(
            model.__name__
        ))
    return model
