from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import UserRegisterForm
from .translation import maintranslation
from .txtspeech import txtToSpeach
from django.utils import timezone  
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import datetime 

from django.db import models
from .models import Translation
from typing import Tuple,List,Any
import asyncio
# Create your views here.


def home(request):
    return render(request,'base/home.html')




# login page 

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request,'Sorry User does not exists')
        
        user=authenticate(request,email=email,password=password)

        if user is not None:

            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'sorry , email or password is not correct ')
    context={'page':page}
    return render(request,'base/register-login.html',context)


# logout 
def logoutPage(requst):
    logout(requst)
    return redirect('home')


# registration form 
def registerPage(request):
    page='register'
    form=UserRegisterForm()
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            # user=form.save(commit=False)
            # user.username=user.username.lower()
            # user.save()
            user=form.save()
            login(request,user)
            return redirect('home')
        else:
            return messages.error(request,'Sorry, An error has occured while registration ! ')

    context={'form':form,'page':page}
    return render(request,'base/register-login.html',context)


#calculate next revision session
def nextRevisionDate(status:str,prev:str,created:datetime.datetime)->Tuple[datetime.datetime,str]:
   
    status_mapping={
        "hard":0,#add one day interval 
        "medium":1,#add 2 days 
        "easy":3 #add 4 days if previous status is not easy
    }
   
    #calculate next  revision based on current status
   
    next_revision=created+datetime.timedelta(days=status_mapping.get(status,1))
         
    if status=="easy":
        if prev=='easy':
            next_revision=created +datetime.timedelta(days=pow(4,status_mapping.get(status,1)))
      

    return next_revision,status

#user searchin for translation 
@login_required
def queryTranslation(request):

    if request.method=='POST':
        orgtext = request.POST.get('original')
        dest_lang=request.POST.get('dest')
        src_lang=request.POST.get('source')
    # else:

        # orgtext = 'Hola, ¿cómo estás?'
        # dest_lang='en'
        # src_lang='es'

    #perform translation
        translated_txt,targetlang=asyncio.run(maintranslation(orgtext,dest_lang))
    
    #generate audio ffiles
        trans_audio=txtToSpeach(translated_txt,dest_lang)

        org_audio=txtToSpeach(orgtext,src_lang)


# Get the current date and time
        current_datetime = timezone.now()
    #create the tranlsation object
        translation_instance=Translation.objects.create(
        user=request.user,
    original_txt=orgtext,
    translated_txt=translated_txt,
    original_audio=org_audio,
    translated_audio=trans_audio,
    status="hard",
    prev_status="hard",
    next_revision_date=nextRevisionDate("hard","hard",current_datetime)[0]
    )
        translation_instance.save()
    else:
        translation_instance=None


    

    # return HttpResponse(f'hello from my app {translated_txt}')
    return render(request,'base/translate.html',{'translation':translation_instance})

# revsion cards
# displays all the revision session card

def cards_revision(request):
    # Get the current date and time
    current_datetime = timezone.now()
    
    revision_cards=Translation.objects.filter(user=request.user,
    next_revision_date__lte=current_datetime)

    return render(request,'base/revise.html',{'revision_cards':revision_cards})

#changing the status during revision
@login_required
def status_change(request):
    current_datetime = timezone.now()
    if request.method == 'POST':
        card_id=request.POST.get('card_id')
        selected_status=request.POST.get(f'status_{card_id}')
        prev_st=request.POST.get('prev_status')
        selected_card=get_object_or_404(Translation,id=card_id)

        selected_card.status=selected_status
        selected_card.prev_status=prev_st
        selected_card.next_revision_date=nextRevisionDate(selected_status,prev_st,current_datetime)[0]
        selected_card.save()

        return redirect('revise')

    # return render(request,'base/card.html',{'selected_card':selected_card})
    return redirect('revise')