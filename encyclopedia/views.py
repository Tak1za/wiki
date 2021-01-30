from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    markdown_data = util.get_entry(title)
    if markdown_data == None:
        return render(request, "encyclopedia/notfound.html")
    html_data = markdown2.markdown(markdown_data)
    return render(request, "encyclopedia/wiki.html", {
        "content": html_data,
        "title": title
    })


def search(request):
    if request.method == "POST":
        form_data = request.POST.dict()
        searchText = form_data.get("q")
        entries = util.list_entries()
        if searchText in entries:
            return HttpResponseRedirect(reverse("wiki", args=(searchText,)))
        else:
            validSearchEntries = []
            for entry in entries:
                if searchText in entry:
                    validSearchEntries.append(entry)

            return render(request, "encyclopedia/search.html", {
                "entries": validSearchEntries
            })

    return render(request, "encyclopedia/search.html", {
        "entries": []
    })
