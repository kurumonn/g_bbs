from .models import G_Topic

def first_topic(request):

    context = {}
    context["FIRST_TOPIC"]  = G_Topic.objects.order_by("-id").first()

    return context