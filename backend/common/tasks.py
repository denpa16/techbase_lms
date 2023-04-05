from urllib import request

import requests
from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile

from .integrations import SMSRSMS


@shared_task
def save_remote_image(app_label, model, pk, attr_name, url):
    ct = ContentType.objects.get_by_natural_key(app_label, model)
    obj = ct.get_object_for_this_type(pk=pk)
    if not url:
        raise ValueError("url is empty")
    if not hasattr(obj, attr_name):
        raise AttributeError(f"{obj} has no attribute {attr_name}")
    attr = getattr(obj, attr_name)
    try:
        response = requests.get(url)
    except:
        try:
            response = requests.get(url, verify=False)
        except Exception as e:
            print(f"Error {e} {url}")
            return
    if not response.status_code == 200:
        print(f"Error status code {response.status_code} {url}")
        return
    image = ContentFile(response.content)
    filename = request.urlparse(url).path.split("/")[-1]
    attr.save(filename, image)


@shared_task
def convert_to_png(app_label, model, pk, to_attr, url, width, height) -> None:
    ct = ContentType.objects.get_by_natural_key(app_label, model)
    obj = ct.get_object_for_this_type(pk=pk)
    if not url:
        raise ValueError("url is empty")
    if not hasattr(obj, to_attr):
        raise AttributeError(f"{obj} has no attribute {to_attr}")
    attr = getattr(obj, to_attr)
    g = requests.get(f"http://imgproxy:8080/insecure/fit/{width}/{height}/sm/0/plain/{url}@png")
    g.raise_for_status()
    image = ContentFile(g.content)
    filename = f"{obj.id}_plan_png.png"
    attr.save(filename, image)


@shared_task
def send_sms(to, body):
    message = SMSRSMS(to=to, body=body)
    message.send()
