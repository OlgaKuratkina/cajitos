import peewee as pw
import datetime as dt

from main.main_app import db


class BaseModel(pw.Model):
    class Meta:
        database = db


class TimestampModel(BaseModel):
    created_at = pw.DateTimeField(default=dt.datetime.utcnow)
    modified_at = pw.DateTimeField(default=dt.datetime.utcnow)

    def save(self, **kwargs):
        """Update self modified at."""
        self.modified_at = dt.datetime.utcnow()
        return super(TimestampModel, self).save(**kwargs)


class VocabularyCard(TimestampModel):
    origin_word = pw.TextField()
    translation_word = pw.TextField()
    origin_language = pw.CharField(choices=('es', 'ru', 'en'), default='en')
    part_of_speech = pw.CharField(max_length=50, null=True)

    def __str__(self):
        return f"'{self.origin_word}' - {self.origin_language} -->  '{self.translation_word}'"
