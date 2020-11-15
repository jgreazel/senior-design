from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .forms import JSONForm

def get_json(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print(request.POST)
        # create a form instance and populate it with data from the request:
        json = JSONForm(request.POST)
        # check whether it's valid:
        if json.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request,'simple/thanks.html')#HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        json = JSONForm()

    return render(request, 'simple/json_enter.html', {'form': json})
