from tortoise import fields, models


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    email = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=128)


class Sections(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=30)
    author = fields.ForeignKeyField(
        "models.Users", related_name="section")

    def __str__(self):
        return f"{self.title}, {self.author_id} on {self.created_at}"


class Notes(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=30)
    description = fields.CharField(max_length=225, null=True)
    comments = fields.TextField(null=True)
    deadline = fields.DateField()
    section = fields.ForeignKeyField(
        "models.Sections", related_name="note")

    def __str__(self):
        return f"{self.title}, {self.section_id} on {self.created_at}"
