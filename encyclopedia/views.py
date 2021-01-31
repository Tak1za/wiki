from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

import markdown2
import random as rand

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
        searchText = searchText.lower()
        entries = util.list_entries()
        lowercase_entries = [item.lower() for item in entries]
        
        if searchText in lowercase_entries:
            return HttpResponseRedirect(reverse("wiki", args=(searchText,)))
        else:
            validSearchEntries = []
            for entry in lowercase_entries:
                if searchText in entry:
                    validSearchEntries.append(entry)

            return render(request, "encyclopedia/search.html", {
                "entries": validSearchEntries
            })

    return render(request, "encyclopedia/search.html", {
        "entries": []
    })

class EntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

def add(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        existing_entries = util.list_entries()
        existing_lowercase_entries = [item.lower() for item in existing_entries]
        if title.lower() in existing_lowercase_entries:
            return render(request, "encyclopedia/add.html", {
                "error": "Already existing entry " + title,
                "form": EntryForm()
            })
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("wiki", args=(title,)))

    return render(request, "encyclopedia/add.html", {
        "form": EntryForm()
    })

def random(request):
    entries = util.list_entries()
    random_choice = rand.choice(entries)
    return HttpResponseRedirect(reverse("wiki", args=(random_choice,)))

def edit(request, title):
    if request.method == "POST":
        updated_content = request.POST["content"]
        util.save_entry(title, updated_content)
        return HttpResponseRedirect(reverse("wiki", args=(title,)))

    markdown_data = util.get_entry(title)
    if markdown_data == None:
        return render(request, "encyclopedia/notfound.html")

    initial_dict = {
        "title": title,
        "content": markdown_data
    }
    
    form_data = EntryForm(initial=initial_dict)
    return render(request, "encyclopedia/edit.html", {
        "form": form_data,
        "title": title
    })