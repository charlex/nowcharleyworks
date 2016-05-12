from django.utils import timezone
from django.shortcuts import render
from nowcharleyworks.models import Thing
from django.template.loader import render_to_string
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.humanize.templatetags.humanize import naturaltime

class JsonException(JsonResponse):
    status_code = 500

def index(request):
    """
    A homepage that lists all the liveblogs.
    """
    context = {
        "things": Thing.objects.all().exclude(archived=True).order_by("-create_datetime")
    }
    return render(request, 'nowcharleyworks/index.html', context)

def save(request):
    """
    Return a count of how many cards the liveblog has in the database.
    """
    thing_name = request.POST.get("name", None)
    # return JsonResponse({})
    if not thing_name:
        return JsonException({"message": "Nothing to save."})

    thing_obj = Thing.objects.create(
        name=thing_name
    )
    t = timezone.localtime(thing_obj.create_datetime)
    return JsonResponse({
        "message": "Thing saved.",
        "pk": thing_obj.pk,
        "created": t.strftime('%A %-I:%M %p'),
        "created_ago": naturaltime(t),
        "created_iso8601": t.isoformat()
    })

def delete(request):
    """
    Return a count of how many cards the liveblog has in the database.
    """
    thing_pk = request.POST.get("pk", None)
    try:
        thing_obj = Thing.objects.get(pk=thing_pk)
    except Thing.DoesNotExist:
        return JsonException({"message": "Thing cannot be found."})

    thing_obj.delete()

    return JsonResponse({ "message": "Thing deleted." })

def archive(request):
    """
    Return a count of how many cards the liveblog has in the database.
    """
    thing_pk = request.POST.get("pk", None)
    try:
        thing_obj = Thing.objects.get(pk=thing_pk)
    except Thing.DoesNotExist:
        return JsonException({"message": "Thing cannot be found."})

    thing_obj.archived = True
    thing_obj.save()

    return JsonResponse({ "message": "Thing archived." })
