from django.shortcuts import render, redirect
from django import forms
from random import choice

from . import util

class NewEntry(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

def entry_exists(title):
    return title.lower() in (name.lower() for name in util.list_entries())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/entry.html", {'title': title, 'entry': entry})
    else:
        return redirect("encyclopedia:404", title=title)

def search(request):
    if request.method == 'POST':
        q = request.POST['q']
        if q and entry_exists(q):
            return redirect("encyclopedia:entry", title=q)
        return render(request, "encyclopedia/404.html", {
            'title': q,
            'entries': [name for name in util.list_entries() if q.lower() in name.lower()]
        })

def new(request):
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]

            if entry_exists(title):
                return render(request, "encyclopedia/exists.html", {'title': title})

            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect("encyclopedia:entry", title=title)
        else:
            return render(request, "encyclopedia/form.html", {'form': form})
    return render(request, "encyclopedia/form.html", {'form': NewEntry()})

def edit(request, title):
    if request.method == "POST":
        if entry_exists(title):
            form = NewEntry({"title": title, "content": request.POST["content"]})
            if form.is_valid():
                util.save_entry(title, form.cleaned_data["content"])
                return redirect("encyclopedia:entry", title=title)
            else:
                context["form"] = form
                return render(request, "encyclopedia/form.html", {"form": form})
        else:
            return redirect("encyclopedia:404", title=title)

    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/form.html", {"form": NewEntry({'title': title, 'content': entry})})
    else:
        return Http404()

def random(request):
    title = choice(util.list_entries())
    return redirect("encyclopedia:entry", title=title)

def delete(request, title):
    return redirect("encyclopedia:index")

def not_found(request, title):
    return render(request, "encyclopedia/404.html", {"title": title})

        
    


