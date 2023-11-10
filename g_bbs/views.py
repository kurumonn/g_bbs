#from django.shortcuts import redirect
from django.views import View
from django.template.loader import render_to_string
from .models import G_Topic

from .forms import TopicForm, TopicFirstForm
# リダイレクトモジュール
from django.contrib.auth.mixins import LoginRequiredMixin
import time
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

import logging


"""

# define home function
def home(request):
    return HttpResponse('Hello World!')
"""

""""
@csrf_exempt
def webhook(request):
    # build a request object
    req = json.loads(request.body)
    # get action from json
    action = req.get('queryResult').get('action')
    # return a fulfillment message
    fulfillmentText = {'fulfillmentText': 'This is Django test response from webhook.'}
    # return response
    return JsonResponse(fulfillmentText, safe=False)
"""

# define home function


@xframe_options_exempt
def ok_to_load_in_a_frame(request):
    return HttpResponse("This page is safe to load in a frame on any site.")


ALLOWED_MIME = ["application/pdf"]


class IndexView(LoginRequiredMixin, View):
    template_name = 'index.html'
    def render_content(self, request):
        g_topics = G_Topic.objects.order_by("-g_dt")
        g_context = {"g_topics": g_topics}
        # カテゴリの選択肢を作るため、全てのカテゴリをcontextに引き渡す
        # context["categories"] = Category.objects.all()

        return render_to_string("g_bbs/content.html", g_context, request)

    def get(self, request, *args, **kwargs):

        g_topics = G_Topic.objects.all()
        g_context = {"G_topics": g_topics}

        # context["categories"] = Category.objects.all()

        return render(request, "g_bbs/index.html", g_context)

    def post(self, request, *args, **kwargs):

        data = {"error": True}
        form = TopicForm(request.POST)

        if not form.is_valid():
            print(form.errors)
            return JsonResponse(data)

        form.save()

        data["error"] = False
        data["g_content"] = self.render_content(request)

        return JsonResponse(data)
    '''
    def delete(self, request, *args, **kwargs):

        data = {"error": True}

        if "pk" not in kwargs:
            return JsonResponse(data)

        topic = Topic.objects.filter(id=kwargs["pk"]).first()

        if not topic:
            return JsonResponse(data)

        topic.delete()

        data["error"] = False
        data["content"] = self.render_content(request)

        return JsonResponse(data)
    '''
    def top(request):
        logger = logging.getLogger('django.request')
        logger.info(f'IP Address: {request.META["REMOTE_ADDR"]} accessed to the top page.')
        return render(request, 'g_bbs/index.html')


index = IndexView.as_view()


# ロングポーリング

class RefreshViewg(View):

    def get(self, request, *args, **kwargs):

        data = {"error": True}

        form = TopicFirstForm(request.GET)

        # 誰も何も投稿していない場合、firstに来る値は何もないので、必ずバリデーションエラーになってしまう。
        # 未投稿の状況でもロングポーリングをさせるには、nullを許可する必要が有ると思われる。←required=Falseで対処
        if not form.is_valid():
            print(form.errors)
            return JsonResponse(data)
            print("null許可")
        cleaned = form.clean()

        first_id = None

        if "first" in cleaned:
            first_id = cleaned["first"]

        # 15回ループする。(1秒おきにDBにアクセスする)
        # CHECK:このループは最大で30秒間レスポンスを返さないことを意味しているので、ブラウザのタイムアウトを考慮して調整する必要が有る。
        for i in range(15):

            G_topic = G_Topic.objects.order_by("-g_dt").first()

            # topicが存在しており、そのtopicがかつての最新のものと違う場合、ループを抜ける。
            if G_topic:
                if G_topic.id != first_id:
                    break
            else:
                # かつての最新の投稿がNoneではない場合、削除されたことを意味するので、この場合もループを抜ける
                if first_id != None:
                    break


            time.sleep(0.5)
            # print("ロングポーリング中")

        g_topics = G_Topic.objects.order_by("-g_dt")
        context = {"G_Topic": G_Topic}

        data["error"] = False
        data["g_content"] = render_to_string("g_bbs/content.html", context, request)

        return JsonResponse(data)


refreshg = RefreshViewg.as_view()

def single(request):
    # ビューのロジック
    return render(request,'template.html')


# 画像送信
"""
class PhotoView(View):

    def get(self, request, *args, **kwargs):
        data = PhotoList.objects.all()
        context = {"data": data}

        return render(request, "upload/index.html", context)

    def post(self, request, *args, **kwargs):
        form = PhotoListForm(request.POST, request.FILES)

        if form.is_valid():
            print("バリデーションOK")
            form.save()

        return redirect("bbs:photo")


photo = PhotoView.as_view()
"""












