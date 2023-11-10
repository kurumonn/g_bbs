from django import forms
from .models import G_Topic,Replyg
import logging



class TopicAdminForm(forms.ModelForm):

    class Meta:
        model = G_Topic
        fields = ["g_comment","g_dt"]

    g_comment = forms.CharField(widget=forms.Textarea(attrs={"max length":str(G_Topic.g_comment.field.max_length), }),
                                    label=G_Topic.g_comment.field.verbose_name)

class TopicForm(forms.ModelForm):

    class Meta:
        model   = G_Topic
        #fields  = [ "category","comment","user" ]
        fields = ["g_comment"]

        logging.debug(fields)

class TopicFirstForm(forms.Form):
    first = forms.IntegerField(required=False)

class ReplyForm(forms.ModelForm):

    class Meta:
        model   = Replyg
        fields  = [ "g_target","g_comment" ]

#ロングポーリング用のフォームクラス






"""
class PhotoListForm(forms.ModelForm):

    class Meta:
        model   = PhotoList
        fields  = ['photo']

class DocumentListForm(forms.ModelForm):

    class Meta:
        model   = DocumentList
        fields  = ['document']

"""

