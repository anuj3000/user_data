from django.shortcuts import render
from django.http import Http404
from pathlib import Path
import os
from .fig2 import data 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

def home(request):
    if request.method == "POST":
        city = request.POST["city"]
        area = request.POST["tehsil"]
        try:
            if(city == "Bhopal (Capital city)"):
                r = data.generate_combined_plotly_graphs(os.path.join(BASE_DIR,"app\\bhopal\\{}.xlsx").format(area))
                return render(request, 'main.html')
            elif(city == "Indore"):
                r = data.generate_combined_plotly_graphs(os.path.join(BASE_DIR,"app\\indore\\{}.xlsx").format(area))
                return render(request, 'main.html')
        except:
            raise Http404("The requested resource does not exist")
    else:
        # Render the index.html template for GET requests
        return render(request, 'home.html')