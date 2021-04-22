from tortoise.fields.data import CharField, IntField, TextField
from tortoise.fields.relational import ManyToManyField, ManyToManyRelation
from tortoise.models import Model


class Index(Model):
    id = IntField(pk=True)
    index_id = CharField(255)


class GalleryInfo(Model):
    language_localname = TextField(null=True)
    language = TextField(null=True)
    date = TextField(null=True)
    files: ManyToManyRelation["File"] = ManyToManyField("models.File")
    tags: ManyToManyRelation["Tag"] = ManyToManyField("models.Tag")
    japanese_title = TextField(null=True)
    title = TextField(null=True)
    id = CharField(255, pk=True)
    type = TextField(null=True)


class File(Model):
    id = IntField(pk=True)
    index_id = CharField(255)
    width = IntField(null=True)
    hash = CharField(64, null=True)
    haswebp = IntField(null=True)
    hasavifsmalltn = IntField(null=True)
    name = TextField(null=True)
    height = IntField(null=True)
    hasavif = IntField(null=True)


class Tag(Model):
    id = IntField(pk=True)
    index_id = CharField(255)
    male = CharField(1, null=True)
    female = CharField(1, null=True)
    tag = CharField(255, null=True)
    url = CharField(255, null=True)
