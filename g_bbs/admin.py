from django.contrib import admin
from django.db import models
from django.conf import settings
from .models import G_Topic
from .forms import TopicAdminForm
import json
import os


class TopicAdmin(admin.ModelAdmin):
    form = TopicAdminForm


admin.site.register(G_Topic, TopicAdmin)


class BlockWord(models.Model):
    word = models.CharField(max_length=100)
    is_oneword = models.BooleanField(default=False)
    json_data = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.word

    def save(self, *args, **kwargs):
        # JSON 形式に変換して json_data に格納する
        data = {
            'word': self.word,
            'is_oneword': self.is_oneword,
        }
        self.json_data = json.dumps(data)

        super().save(*args, **kwargs)


class BlockWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'get_is_oneword')

    def get_is_oneword(self, obj):
        return obj.is_oneword
    get_is_oneword.short_description = 'is_oneword'



admin.site.register(BlockWord, BlockWordAdmin)


BAD_WORD_PATH = os.path.join(settings.BASE_DIR, 'bad_word.json')
print(BAD_WORD_PATH)
if not os.path.exists(BAD_WORD_PATH):
    print(BAD_WORD_PATH)
    with open(BAD_WORD_PATH, 'w', encoding='utf-8') as f:
        json.dump([], f)
else:
    pass