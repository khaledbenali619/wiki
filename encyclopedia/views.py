from lib2to3.pytree import convert
from random import choice, randint
from turtle import title
from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from . import util
from django.urls import reverse
from markdown2 import Markdown
import markdown
import random
from markdownify import markdownify

from . import util

#new page
class NewPageForm(forms.Form):
    pagename = forms.CharField(label="Title",required = True,
    widget= forms.TextInput
    (attrs={'placeholder':'Enter Title', 'class': 'form-control'}))
    body = forms.CharField(label="Markdown content",required= False, 
    widget= forms.Textarea
    (attrs={'placeholder':'Enter markdown content', 'class': 'form-control'}))


class SearchForm(forms.Form):
    """ Form Class for Search Bar """
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Search Encyclopedia"}))

def md_converter(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else: 
        return markdowner.convert(content)


#Edit Page
class EditForm(forms.Form):
  """ Form Class for Editing Entries """
  text = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Enter Page Content", 'class': 'form-control'
    }))

#Search for result
def result(request, name):
    entry_HTML = md_converter(name)
    return render(request,"encyclopedia/result.html", {
        "name":name,
        "entry": entry_HTML,
        
    })
# Random page

def random_entry(request):
    titles = util.list_entries()
    title = random.choice(titles)

    # Redirect to selected page:
    return redirect(reverse('result', args=[title]))


#Search
def search_result(request):
    if request.method == "POST":
        name = request.POST['q']
        entry_HTML = md_converter(name)
    return render(request, "encyclopedia/result.html",{
        "entry": entry_HTML,
        "name":name
    })

#Edit Entry
def edit(request, name):
    """ Lets users edit an already existing page on the wiki """

    # If reached via editing link, return form with post to edit:
    if request.method == "GET":
        text = util.get_entry(name)

        # return pre-populated form:
        return render(request, "encyclopedia/edit.html", {
          "name": name,
          "edit_form": EditForm(initial={'text':text}),
          "search_form": SearchForm()
        })

    # If reached via posting form, updated page and redirect to page:
    elif request.method == "POST":
        form = EditForm(request.POST)

        if form.is_valid():
          text = form.cleaned_data['text']
          util.save_entry(name, text)
          entry_HTML = md_converter(name)
          return render(request,"encyclopedia/result.html", {
            "entry": entry_HTML,
            "name":name
        })



#Home page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


#Create new entry
def create_new_entry(request):

    create_form = NewPageForm(request.POST)
    if create_form.is_valid():
        title = create_form.cleaned_data["pagename"]
        body = create_form.cleaned_data["body"]
        titlefound = util.get_entry(title)

        if titlefound is not None:
            return render( request, "encyclopedia/error.html")
        else:        
            util.save_entry(title,body)
            return result(request, title)

    else:
        
        return render(request, "encyclopedia/create_new_entry.html",{
        "create_form":create_form

    })


