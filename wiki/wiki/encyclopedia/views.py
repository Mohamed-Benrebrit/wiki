
from unicodedata import name
from django.shortcuts import render
from . import util
import random


import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def pages(request, title):

    if util.get_entry(title):
        content = markdown.markdown(util.get_entry(title))
        return render(request, "encyclopedia/Title.html", {
            "title": title, "content": content
        })
    else:
        return render(request, "encyclopedia/Title.html", {
            "title": "Error", "error": f"{title} Not found."
        })


def search(request):
    Value = request.GET['q']
    if util.get_entry(Value):
        return pages(request, Value)
    else:
        entries = util.list_entries()
        search = [entry for entry in entries if Value.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "result": search
        })


def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    elif request.method == "POST" and util.get_entry(request.POST["t"]) is None:
        util.save_entry(request.POST["t"], request.POST["c"])
        return pages(request, request.POST["t"])
    else:
        return render(request, "encyclopedia/new.html", {
            "error": "Page already exist"
        })


def edit(request):

    if request.method == "GET":
        title = request.GET["h"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title, "c": content
        })
    else:
        util.save_entry(request.POST["t"], request.POST["c"])
        return pages(request, request.POST["t"])


def rand(request):
    randomly = random.choice(util.list_entries())
    return pages(request, randomly)
