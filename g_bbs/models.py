import os
import json
import logging
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.conf import settings

bad_words = [ "バカ","アホ","まぬけ","Украина","Россия","Russia","Ukraine","ロシア","http","script","https"]
bad_onewords = ["Z", "z"]

#BAD_WORD_PATH = os.path.join(settings.BASE_DIR, 'bad_word.json')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAD_WORD_PATH = os.path.join(BASE_DIR, 'bad_word.json')
print(BAD_WORD_PATH)
if not os.path.exists(BAD_WORD_PATH):
    print(BAD_WORD_PATH)
    with open(BAD_WORD_PATH, 'w', encoding='utf-8') as f:
        print(BAD_WORD_PATH)
        json.dump([], f)


def load_bad_words():
    with open(BAD_WORD_PATH, 'r', encoding='utf-8') as f:
        g_data = json.load(f)
        bad_words = []
        for g_word in g_data:
            if g_word not in bad_words:
                bad_words.append(g_word)
        return bad_words


        """
        for key in data:
            for word in data[key]:
                if word not in bad_words:
                    bad_words.append(word)
        return bad_words
        """




def validate_bad_word(value):


    for g_word in bad_words:
        if g_word in value:
            print(g_word)
            print(bad_words)
            print(value)
            logger.warning(f"{g_word}は不適切な単語が含まれているためエラーです")
            raise ValidationError(f"{g_word}には不適切な単語{value}が含まれています。", params={'value': value})

    bad_onewords = AdminBlockWord.get_bad_onewords()
    for word in bad_onewords:
        if word == value:
            logger.warning("1文字不適切な単語が含まれています。")
            raise ValidationError("1文字不適切な単語が含まれています。", params={'value': value})


class AdminBlockWord(models.Model):
    word = models.CharField(verbose_name="不適切な単語", max_length=100)

    @classmethod
    def get_bad_words(cls):
        return load_bad_words()

    @classmethod
    def get_bad_onewords(cls):
        return ["Z", "z"]

    def __str__(self):
        return self.word


# logs フォルダが存在しない場合は作成
if not os.path.exists('logs'):
    os.makedirs('logs')

# logger settings
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ログのフォーマットを指定
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

# ログのファイル名を指定
now = datetime.now()
filename = now.strftime('%Y-%m-%d.log')
foldername = now.strftime('%Y/%m/%d')
log_dir = f'logs/{foldername}'
# ログの保存先ディレクトリが存在しない場合は作成する
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# ログの保存先ファイルを指定する
# file_handler = logging.FileHandler(f'{log_dir}/{filename}')
file_handler = logging.FileHandler(f'{log_dir}/{filename}', mode='a', encoding='utf-8')  # UTF-8設定追加
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def get_client_ip(request):
    # request.META.get('HTTP_X_FORWARDED_FOR') にはクライアントの IP アドレスが含まれる場合がある
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip







class G_Topic(models.Model):
    g_dt = models.DateTimeField(verbose_name="G投稿日時", default=timezone.now)
    g_comment = models.CharField(verbose_name="Gコメント", max_length=2000, validators=[validate_bad_word])
    g_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Gユーザー", on_delete=models.CASCADE, null=True, blank=True)
    # category = models.ForeignKey(Category, verbose_name="カテゴリ", on_delete=models.CASCADE)
    def __str__(self):
        return self.g_comment

    def save(self, *args, **kwargs):
        if self.g_user:
            logger.info(f'{str(self.g_dt)} {self.g_user.username} {self.g_comment}')
            logger.warning(f'{str(self.g_dt)} {self.g_user.username} {self.g_comment}')
        else:
            logger.info(f'{str(self.g_dt)} {self.g_comment}')
            logger.warning(f'{str(self.g_dt)} None {self.g_comment}')
        super(G_Topic, self).save(*args, **kwargs)

class Replyg(models.Model):

    g_target = models.ForeignKey(G_Topic, verbose_name="リプライ対象のGトピック", on_delete=models.CASCADE)

    g_comment = models.CharField(verbose_name="コメント", max_length=2000)

    def __str__(self):
        return self.g_comment

# Create your models here.

