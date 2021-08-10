from django.http.response import HttpResponseRedirect
from main.forms import CreateNewList
from django.shortcuts import render
from django.http import HttpResponse
from .models import ToDoList, Item
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='/login/')
def index(response,id):
    ls = ToDoList.objects.get(id=id)
    if ls in response.user.todolist.all():
        if response.method == "POST":
            #print(response.POST)
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c"+str(item.id)):
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()
            elif response.POST.get("addNewItemButton"):
                item_text=response.POST.get("newItemTxt")

                if len(item_text) > 2: 
                    ls.item_set.create(text=item_text,complete=False)

            elif response.POST.get('delete'):
                del_obj=ls.item_set.get(id=response.POST.get('delete'))
                del_obj.delete()
        return render(response,'main/list.html',{"ls":ls})
    return HttpResponseRedirect('/')

def home(response):
    return render(response,'main/home.html',{'name':"test"})

@login_required(login_url='/login/')
def create(response):
    if response.method == 'POST':
        form = CreateNewList(response.POST)
        if form.is_valid():
            form_name=form.cleaned_data['name']
            form_list=ToDoList(name=form_name)
            form_list.save()
            response.user.todolist.add(form_list)
        return HttpResponseRedirect(f'/{form_list.id}')
    else:
        form = CreateNewList()
        return render(response, 'main/create.html',{'form':form})

@login_required(login_url='/login/')
def view(response):
    return render(response,'main/view.html',{})