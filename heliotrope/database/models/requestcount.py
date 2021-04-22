from tortoise import Model, fields


class RequestCount(Model):
    index = fields.IntField(pk=True)
    title = fields.CharField(255)
    count: int = fields.IntField()
