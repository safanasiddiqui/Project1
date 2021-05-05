from django.shortcuts import render, redirect
import markdown
import markdown2
from django import forms
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import random




from . import util

class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title")
    text = forms.CharField(label="Text", widget=forms.Textarea(attrs={'rows': 1}))


class EditPageForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={
        'id': 'edit-entry-title'}))
    text = forms.CharField(label="Text", widget=forms.Textarea(attrs={
        'id': 'edit-entry', 'size': '3'}))

class Edit(forms.Form):
    text = forms.CharField(widget=forms.Textarea(), label='')


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def topic(request, title):
    """ Displays the requested entry page, if it exists """
    entry_md = util.get_entry(title)
    """entry_HTML = util.convert_md(title)"""
    if entry_md != None:
        # Title exists, convert md to HTML and return rendered template
        """entry_HTML = markdown.Markdown().convert(entry_md)"""
        entry_HTML = util.convert_md(title)
        return render(request, "encyclopedia/page.html", {
            "entry_HTML": entry_md,
            "title": title,
            "body":entry_HTML
            })
    else:
        # Page does not exist

        return render(request, "encyclopedia/notfound.html", {
            "title": title,
            })

def search(request, title=None):
    title = request.GET.get('q')
    entry_md = util.get_entry(title)
    if entry_md != None:
        # Title exists, convert md to HTML and return rendered template
        search = util.convert_md(title)
        return render(request, "encyclopedia/page.html", {
            "search": entry_md,
            "title": title,
            "body": search
            })
    else:
        # Page does not exist

        return render(request, "encyclopedia/notfound.html", {
            "title": title,
            })



def newpage(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/exists.html", {"message": "Page already exists"})
            else:
                util.save_entry(title, text)
                file = ContentFile(content)

                default_storage.save( f"entries/{title}.md", file)
                title = util.get_entry(title)
                title.append(entries)
                messages.success(request, f'New page "{title}" created successfully!')

    return render(request, "encyclopedia/newpage.html",{
        "form": NewTaskForm()
    })

def edit(request, title):
    if request.method == "GET":
        entry = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "form": EditPageForm(),
            "edit": Edit(initial={'text': entry}),
            "title" : title
        })
    else:
        if request.method == "POST":
            form = EditPageForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data["title"]
                text = form.cleaned_data["text"]
                util.save_entry(title, text)
                entry = util.get_entry(title)
                readlines = util.get_entry(text)
                entry_html = util.convert_md(title)
                data = {
                    "title": title,
                    "text": ''.join(content[1:])
                }
                return render(request, "encyclopedia/entry.html",{
                "form": EditPageForm(data),
                "entry": entry_html,
                "content": util.get_entry(title),
                "title": title
            })

def randompage(request):
    choice = random.choice(util.list_entries())
    html = util.convert_md(choice)
    return render(request,"encyclopedia/page.html",{
        "title":choice, "body":html
    })
