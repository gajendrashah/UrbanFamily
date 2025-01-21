from datetime import date, datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User , auth
from django.contrib.auth.decorators import login_required
from django.http import Http404,JsonResponse
from roomapp.form import Advance_paymentForm, BookedAccountupdateForm, CustomerCretionForm, CustomerCretionForm1, Non_room_OrderCreationForm, Order_creation_Non_room_user, OrderCreationForm, ReservationCreationForm, RoomCreationForm, RoomUpdateForm
from roomapp.models import Additional_id, Advance_payment, Booked, Ch_out, Customer, Customer_list, Grouped_room, Non_room_user, Order, Room
from django.db.models import Q

# Create your views here.
@login_required(login_url="signin")
def dashboard(request):
    customer_list = Customer_list.objects.filter(status=True).order_by("-bookd_roooms__booked_date")
    ad_form = Advance_paymentForm()

    cus = Customer.objects.all().order_by("-check_out",)
    context = {"customer":cus[:5],"customer_list":customer_list,"ad_form":ad_form}
    return render(request, 'index.html',context)



def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def get_room_by_group(request):
    grouped_room = Grouped_room.objects.all().values()
    return JsonResponse(list(grouped_room),safe=False)


def customerdata(request):
    result = []
    if "term" in request.GET:
        term = request.GET.get("term")
        print(term)
        obj = Customer.objects.filter(Q(full_name__icontains=term) | Q(phone_number__icontains=term))
        print(obj)
        for t in obj:
            result.append(t.id)
            result.append(t.full_name)

        return JsonResponse(list(result),safe=False)



def get_user(request):
    data = request.GET.get("user")
    customer = Customer.objects.filter(full_name__icontains=data).values()
    user = Customer.objects.get(id=customer[0]["id"])
    room = Booked.objects.filter(customer_details=user).last()
    room_dis = Ch_out.objects.filter(customer=user).last()
    print("customer")
    room_numbers = []
    for i in room.room_id.all():
        room_numbers.append(i.room_number)
    
    if room_dis is not None:
        room_dis = room_dis.room_discount
    else:
        room_dis = 0.0


    return JsonResponse({"customer":list(customer),"romms":list(room_numbers),"room_disc":str(room_dis)},safe=False)

@login_required(login_url="signin")
def checkin(request):
    ad_form = Advance_paymentForm()
    form = CustomerCretionForm
    customer_list = Customer_list.objects.filter(status=True).order_by("-bookd_roooms__booked_date")
    if request.method == "POST":
        phone_number= request.POST.get("phone_number")
        print(phone_number)
        rooms = request.POST.getlist("id_room")
        main_id_add= request.FILES.getlist("main_additional_id")

        if rooms != []:
            user_id = request.POST.get("phone_number")
            try:
                users = Customer.objects.get(user=user_id)
                if users:
                    form = CustomerCretionForm(request.POST,request.FILES,instance=users)
                else:
                    form = CustomerCretionForm(request.POST,request.FILES)
            except:
                form = CustomerCretionForm(request.POST,request.FILES)
            
            if form.is_valid:
                data = form.save(commit=False)
                data.check_in = datetime.now()
                form.save()
                # print(form.pk)
                child = form.cleaned_data.get("Child")
                male_number = form.cleaned_data.get("male_number")
                female_number = form.cleaned_data.get("female_number")
                other_gender = form.cleaned_data.get("other_gender")
                # print("here is a id ",main_id_add)
                user = Customer.objects.get(id = data.pk)
                
                for img in main_id_add:
                    obs = Additional_id.objects.create(customer=user,add_id=img)
                    obs.save()
                # print(main_id_add)            
            
                res = [eval(i) for i in rooms]
                get_room_list = Room.objects.filter(id__in=rooms)
        
                book_id = Booked.objects.create(customer_details=user, child=child,male_number=male_number,female_number=female_number,other_gender=other_gender)
                book_id.room_id.set(res)
                book_id.status=True
                book_id.save()
                x = Booked.objects.get(id=book_id.pk)
                cus_active = Customer_list.objects.create(customer=user,bookd_roooms=x)
                cus_active.save()
                for room in get_room_list:
                    room.status ="booked"
                    room.save()
                messages.success(request, 'Customer creation successfully ')
                return redirect("checkin")
        else:
            messages.error(request, 'Please Provide room data')
            return redirect("checkin")
    
    if is_ajax(request=request):
        term = request.GET.get("room")
        group = Grouped_room.objects.get(title=term)
        room = Room.objects.filter(status="available",group=group).values()
        # print(room)
        return JsonResponse(list(room),safe=False)

    context={"customer_list":customer_list,"form":form,"form2":ad_form}
    return render(request, 'roomapp/checkin.html',context)

def checkin_edit(request,pk):
    cus = Customer.objects.get(id=pk)
    b = Booked.objects.filter(customer_details=cus).first()
    print(b)
    customer_form = CustomerCretionForm1(instance=cus)
    book_form = BookedAccountupdateForm(instance=b)
    if request.method=="POST":
        customer_form = CustomerCretionForm1(request.POST,request.FILES,instance=cus)
        book_form = BookedAccountupdateForm(request.POST,request.FILES,instance=b)
        if customer_form.is_valid():
            customer_form.save()
        if book_form.is_valid():
            book_form.save()
        return redirect("checkin")

    context={"customer_form":customer_form,"book_form":book_form}
    return render(request,"roomapp/check_in_edit.html",context)

@login_required(login_url="signin")
def checkout(request):
    customer_list = Customer_list.objects.filter(status=True).order_by("-bookd_roooms__booked_date")
   
   
    
    if request.method == "POST":
                
        user_id = request.POST.get("user")
        ammount = request.POST.get("ammount", None)
        paytype = request.POST.get("paytype")
        remarks = request.POST.get("remarks")
        # print(type(ammount),paytype,user_id)
        if user_id != "" and ammount != "" and paytype != "": 

            user = Customer.objects.get(id=user_id)
            obj = Advance_payment.objects.create(customer=user,Advance_amount=ammount,payment_mode=paytype,remarks=remarks)
            obj.save()
        
       
            return JsonResponse({"message":"success"},safe=False)
        else:
            return JsonResponse({"message":"Please fill all values"},safe=False)
    
    
    if is_ajax(request=request):
        term = request.GET.get("room")
        group = Grouped_room.objects.get(title=term)
        room = Room.objects.filter(status="available",group=group).values()
        
        return JsonResponse(list(room),safe=False)

    context = {"customer_list":customer_list}


    return render(request, 'roomapp/checkout.html',context)

def check_out(request):
    if request.method == "POST":
        room_num= []
        pk = request.POST.get("user")
        if pk != "":
            user = Customer.objects.get(id=pk)
            rooms = Customer_list.objects.filter(customer=user).last()
            all_rooms = rooms.all_rooms
            for i in all_rooms:
                room_number = i.room_number
                room_num.append(room_number)
            room_cost = rooms.room_cost
            res_cost = rooms.total_resturent_amount
            advance_amt = rooms.total_amount
            remaing_balance = Ch_out.objects.filter(customer=user).last()
            if remaing_balance is not None:
                rem_blc = remaing_balance.rem_bln
                # print(rem_blc)
                room_discount = remaing_balance.room_dic
                resturet_discount = remaing_balance.resturent_dic
            else:
                rem_blc = 0
                room_discount = 0
                resturet_discount = 0
                
            # print("here i am",res_cost)
            context={"username":user.full_name,"room_cost":room_cost,
            "res_cost":res_cost,"advance_amt":advance_amt,"remaing_balance":rem_blc,
            "room_discount":room_discount,
            "resturet_discount":resturet_discount,
            "room_number":room_num
            }
            return JsonResponse(context,safe=False)

def check_out_process(request):
    if request.method != "POST":
        raise Http404
    

    user_id = request.POST.get("user")
    room_discount = request.POST.get("room_discount")
    resturent_discount = request.POST.get("resturent_discount")
    vat = request.POST.get("vat")
    remarks = request.POST.get("remarks")
    remaing_amt = request.POST.get("remaing_amt")

    # print(request.POST)

    if user_id != "" :
    
        cus = Customer.objects.get(id = user_id)
        # user = Customer_list.objects.filter(customer=cus,status=True)
        obj = Ch_out.objects.create(customer=cus,remaing_balance=abs(float(remaing_amt)),
        resturent_discount=resturent_discount,room_discount=room_discount,vat=bool(vat),
        remarks=remarks

        )
        obj.save()
        ad = Advance_payment.objects.filter(customer=cus)
        # print("this is ad",ad)
        if ad is not None:
            for i in ad:
                i.Advance_amount = 0
                i.save()
        else:
            pass
        deactive = Customer_list.objects.filter(customer=cus,status=True).first()
        print("deactivate",deactive)
        rooms = deactive.all_rooms
        print("rooms",rooms)
        for room in rooms:
            room.status = "cleaning"
            room.save()
        deactive.status=False
        deactive.save()
        cus.check_out = datetime.now()
        cus.save()
        

        return JsonResponse({"msg":"User Check Out sucessfully "},safe=False)
    else:
        return JsonResponse({"msg":"Please Make sure the data will be filled correctly"},safe=False)



@login_required(login_url="signin")
def addroom(request):
    form = RoomCreationForm
    rooms= Room.objects.all()
    if request.method == "POST":

        form = RoomCreationForm(request.POST)
        if form.is_valid():
            room_number = form.cleaned_data["room_number"] 
            form.save()


            messages.success(request,f'Room are Createted !!! {room_number}')
            return redirect("addroom")
        else:
            messages.error(request,"Room Cant Create !!")
            return redirect("roomdetails")




    context = {"allrooms":rooms,"form":form}

    return render(request, 'roomapp/addroom.html',context)

@login_required(login_url="signin")
def reserveroom(request):
    cs = Booked.objects.filter(status= False)
    form = ReservationCreationForm

    av_room = Room.objects.filter(status="available")
   
    if request.method == "POST":
        # print(request.POST,request.FILES)
        form =ReservationCreationForm(request.POST,request.FILES)
        room_id = request.POST.getlist("room")
        if form.is_valid():
            data = form.save(commit=False)
           
            form.save()
            child = form.cleaned_data.get("Child")
            male_number = form.cleaned_data.get("male_number")
            female_number = form.cleaned_data.get("female_number")
            other_gender = form.cleaned_data.get("Other_gender")
            number_of_days = form.cleaned_data.get("number_of_days")
            user = Customer.objects.get(id=data.pk)

            res = [eval(i)for i in room_id]
            book_id = Booked.objects.create(customer_details=user,number_of_days=number_of_days, child=child,male_number=male_number,female_number=female_number,other_gender=other_gender)
            book_id.room_id.set(res)
            book_id.save()


            for rid in room_id:
                room_update = Room.objects.get(id=rid)
                room_update.status= "not-confirm"
                room_update.save()
            messages.success(request,"Your Resevation is complete")
            return redirect("reserveroom")
        else:
            messages.error(request,form.errors)
            return redirect("reserveroom")
    context = {"customers": cs, "av_room": av_room, "form":form}
    return render(request, 'roomapp/reserve_room.html',context)


def reservation_edit(request,pk):
    foo_ = Booked.objects.get(id=pk)
    cus = Customer.objects.get(id = foo_.customer_details_id)
    # print("foo",foo_)
    form = ReservationCreationForm(instance=cus)
    room_id = request.POST.getlist("room")
    if request.method == "POST":
        form = ReservationCreationForm(request.POST,request.FILES,instance=cus)
        if form.is_valid():
            data= form.save(commit=False)

            child = form.cleaned_data.get("Child")
            # print("Child",child)
            male_number = form.cleaned_data.get("male_number")
            female_number = form.cleaned_data.get("female_number")
            other_gender = form.cleaned_data.get("Other_gender")
            number_of_days = form.cleaned_data.get("number_of_days")
            
            Bks = Booked.objects.get(customer_details_id=data.pk)
            Bks.child= int(child)
            Bks.male_number = male_number
            Bks.female_number = female_number
            Bks.other_gender = other_gender
            Bks.number_of_days = number_of_days
            
            
            res = [eval(i)for i in room_id]
            Bks.room_id.set(res)
            Bks.save()

            for rid in room_id:
                room_update = Room.objects.get(id=rid)
                room_update.status= "not-confirm"
                room_update.save()

            
            form.save()
            messages.success(request,"Data updated successfully !!!")
            return redirect("reserveroom")



    context={"form":form}
    return render(request,"roomapp/reserve_room_edit.html",context)
 

def reservation_checkin(request):
    if request.method != "POST":
        raise Http404
    
    else:
        booke_id = request.POST.get("bookd_id")
        books_= Booked.objects.get(id=booke_id)
        books_.status = True
        cus= cus = Customer_list.objects.create(bookd_roooms=books_,customer=books_.customer_details)
        cus.status=True
        for r in books_.room_id.all():
            r.status = "booked"
            r.save()
        cus.save()
        books_.save()

        return JsonResponse({"msg":"This is working "},safe=False)

def reservation_cancle(request):
    if request.method == "POST":
        pk = request.POST.get("bookd_id")
        booked = get_object_or_404(Booked,id=pk)
        for r in booked.room_id.all():
            r.status = "available"
            r.save()
            booked.delete()
        return JsonResponse({"msg":"Booking cancle sucssfully !!!"},safe=False)
    # return JsonResponse({"msg","reserveroom"},safe=False)



@login_required(login_url="signin")
def roommanager(request):
    form = RoomUpdateForm
    rooms= Room.objects.all().exclude(status__in=["cleaning","maintenance"])
    rooms_mainc= Room.objects.all().filter(status__in=["cleaning","maintenance"])
    if request.method == "POST":

        form = RoomCreationForm(request.POST)
        if form.is_valid():
            first_number = form.cleaned_data.get("initial_number")
            last_number = form.cleaned_data.get("final_number")
            
            room_group = form.cleaned_data.get("room_name")
            price = form.cleaned_data.get("price")
            room_list = list(range(first_number,last_number+1))
            obj = Grouped_room.objects.create(title=room_group)
            # obj.save(commit=False)
            obj.save()
            group_id = Grouped_room.objects.get(id=obj.id)

            for data in room_list:
                obj = Room.objects.create(group= group_id,room_number=data,price_pernight=price)
                obj.save()
            messages.success(request,"Room are Createted !!!")
            return redirect("roomdetails")
        else:
            messages.error(request,"Room Cant Create !!")
            return redirect("roomdetails")




    context = {"allrooms":rooms,"rooms_mainc":rooms_mainc,"form":form}
    return render(request, 'roomapp/room_manager.html',context)


def room_update(request):
    form = RoomUpdateForm()
    
    if request.method =="POST":
        r_id = request.POST.get("room_id")
        status = request.POST.get("status")
        room_id = Room.objects.get(id=r_id)
        room_id.status = status
        room_id.save()
        return JsonResponse({"msg":"room updated"},safe=False)

   
    context = {'form':form}
    return render (request,"roomapp/room_update.html",context)

def room_delete(request,pk):
    customer = get_object_or_404(Room,id=pk)
    customer.delete()
    messages.success(request, "Room Delete successfully" )
    return redirect('addroom')

def customerdetail(request):
    cust = Customer.objects.all()
    # print(len(cust))

    context={"customer":cust}
    return render(request, 'roomapp/report.html',context)

def with_room(request):
    order = Order.objects.all().order_by("-order_date")
    form = OrderCreationForm
    
    if request.method == "POST":
        if request.POST.get("room_id") != None:
            
            
            room_id = request.POST.get("room_id")
            order_id = request.POST.get("order_id")
            total = request.POST.get("total")
            # cus = Order.objects.filter(room=room_id)
            # print(room_id,order_id,total)

            # form = OrderCreationForm(request.POST)
            r = Room.objects.get(room_number=room_id) #room id
            # print(r.id)
            c = Booked.objects.filter(room_id__id=r.id).values()

            c_id= c[0]["customer_details_id"]

        
            obj = Order.objects.create(order_id=order_id,customer_id=c_id,
                room=r,total=total
            )
            # obj.order_date = datetime.now()
            obj.save()
            return JsonResponse({"msg":"ok"},safe=False)
        

    context ={"form":form,"order":order}


    return render(request,"resturentapp/withroom.html",context)
def order_update(request,pk):
    order = get_object_or_404(Order,id=pk)
    form = OrderCreationForm(instance=order)
    if request.method == 'POST':
        form = OrderCreationForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order update successfully" )
            return redirect('withroom')
        else:        
            messages.error(request, "Order Cant made" )
            return redirect('withroom_update',pk=pk)


   
    context = {'form':form}
    return render (request,"resturentapp/withroom_update.html",context)

def order_delete(request,pk):
    customer = get_object_or_404(Order,id=pk)
    customer.delete()
    messages.success(request, "Order Delete successfully" )
    return redirect('withroom')

def with_out_room(request):
    form = Order_creation_Non_room_user
    non_room = Non_room_user.objects.all().order_by("-order_date")
    if request.method == "POST":
        
        form = Order_creation_Non_room_user(request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request,"Order Create successfully")
            return redirect("withoutroom")
        else:
            messages.error(request,"Order order cant create !!")
            return redirect("withoutroom")

    context ={"form":form,"non_room_user":non_room}
    return render (request,"resturentapp/withoutroom.html",context)

def with_out_room_update(request,pk):
    order = get_object_or_404(Non_room_user,id=pk)
    # print(order)
    form = Non_room_OrderCreationForm(instance=order)
    if request.method == 'POST':
        form = Non_room_OrderCreationForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            messages.success(request,"Order Updated !!!")
            return redirect('withoutroom')
        else:
            messages.error(request,"order  Cant Updated !!!")
            return redirect('withoutroom_update')
    context = {'form':form}
    return render(request, "resturentapp/without_room_update.html",context)

def with_out_room_delete(request,pk):
    customer = get_object_or_404(Non_room_user,id=pk)
    customer.delete()
    messages.success(request, "Oder Delete successfully" )
    return redirect('withoutroom')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username OR password is incorrect')

    return render(request,"extra pages/signin.html")


def user_signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':  
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']  

            # print("here we are")
            if password1==password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request,'Username already taken')
                    return redirect('signup')
                elif User.objects.filter(email=email).exists():
                    messages.info(request,'Email already taken')
                    return redirect('signup')    
                else:    
                    user = User.objects.create_user(username=username, email=email,password=password1)
                    user.save()
                    return redirect('signin')
            else:
                messages.info(request,'Password did not matched.')
                return redirect('signup')
        

    return render(request,"extra pages/signup.html")


def user_logout(request):
    auth.logout(request)
    return redirect('signin')


def edit_room(request):
    form = RoomCreationForm
    if request.method == "POST":

        form = RoomCreationForm(request.POST)
        if form.is_valid():
            first_number = form.cleaned_data.get("initial_number")
            last_number = form.cleaned_data.get("final_number")
            
            room_group = form.cleaned_data.get("room_name")
            price = form.cleaned_data.get("price")

            
            r = Room.objects.filter(intital_number=first_number,final_number=last_number)
            r.delete()
            g = Grouped_room.objects.filter(title=room_group)
            g.delete()


            room_list = list(range(first_number,last_number+1))
            obj = Grouped_room.objects.create(title=room_group)
            # obj.save(commit=False)
            obj.save()
            group_id = Grouped_room.objects.get(id=obj.id)

            for data in room_list:
                obj = Room.objects.create(group= group_id,room_number=data,price_pernight=price,intital_number=first_number,final_number=last_number)
                obj.save()
            messages.success(request,"Room are Createted !!!")
            return redirect("addroom")
        else:
            messages.error(request,"Room Cant Create !!")
            return redirect("roomdetails")


    context ={"form":form}
    return render(request,"update_room.html",context)




def report_gen(request):
    if request.POST:
        # print(request.POST)
        amt_pay = 0;
        user_id = request.POST.get("user")
        cus = Customer.objects.filter(id=user_id).values()
        print(cus)
        a = Customer.objects.get(id=user_id)
        x = Ch_out.objects.filter(customer=a)
        data = []
        for i in x:

          
            data.append({"resturent discount":i.resturent_dic,"room discount":i.room_dic,"remaing balance":i.rem_bln})
            amt_pay +=i.rem_bln
        r = Booked.objects.filter(customer_details=a)
        for i in r:
            z = i.room_id.all()
            for l in z:
                data.append({"room id ":l.room_number})
        data.append({"amt_pay":amt_pay})
        return JsonResponse({"data":list(cus),"bills":data,"msg":"scccess"},safe=False)