from random import randint
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import csv
from django import forms
from . import util
from django.urls import reverse


class SearchForm(forms.Form):
    """ Form Class for Search Bar """
    name = forms.CharField(label='', widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Search wiki"}))

#new page
class NewPageForm(forms.Form):
    pagename = forms.CharField(label="Title",required = True,
    widget= forms.TextInput
    (attrs={'placeholder':'Enter Title', 'class': 'form-control'}))
    body = forms.CharField(label="Markdown content",required= False, 
    widget= forms.Textarea
    (attrs={'placeholder':'Enter markdown content', 'class': 'form-control'}))

#Edit Page
class EditForm(forms.Form):
  """ Form Class for Editing Entries """
  text = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Enter Page Content using Github Markdown", 'class': 'form-control'
    }))

#Search for result
def result(request, name):
    return render(request,"encyclopedia/result.html", {
        "entry": util.get_entry(name),
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
          return render(request,"encyclopedia/result.html", {
            "entry": util.get_entry(name),
            "name":name
        })

  

#Search
def search_result(request):
    if request.method == "POST":
        name = request.POST['q']
    return render(request, "encyclopedia/result.html",{
        "entry": util.get_entry(name)
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

        if title in util.list_entries():
            messages.success(request, f"{title} exist and been replaced")
            util.save_entry(title,body)
            return result(request, title)
        else:        
            util.save_entry(title,body)
            return result(request, title)

    else:
        
        return render(request, "encyclopedia/create_new_entry.html",{
        "create_form":create_form

    })

# Random page

def random_entry(request):
    entries = util.list_entries()
    entry = entries[randint(0, len(entries) - 1)]
    return result(request, entry)
