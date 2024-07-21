from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse , HttpRequest, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Post,TeamMember,Testimonial,ContactForm,MenuItem,Cart,Reservation,Payment
from.models import Order
from django.db.models import Sum, Max,F
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
import razorpay
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .utils import send_notification_email
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
# Create your views here.

def index(request):
    context = {}
    members = TeamMember.objects.all()
    testimonials=Testimonial.objects.all()
    context["testimonials"]= testimonials
    context["members"] = members
    return render(request,"index.html",context)


def base(request):
    return render(request,"base.html")

def about(request):
    context = {}
    members = TeamMember.objects.all()
    context["members"] = members
    return render(request,"about.html",context)

def head(request):
    return render(request,"header.html")

def headlink(request):
    return render(request,"headlink.html")

def footer(request):
    return render(request,"footer.html")


def send_otp_via_email(email, otp):
    subject = 'Your OTP for Password Reset'
    message = f'Your OTP for password reset is: {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            otp = random.randint(100000, 999999)
            request.session['reset_otp'] = otp
            request.session['reset_email'] = email
            send_otp_via_email(email, otp)
            return redirect('password_reset_otp')
    return render(request, 'password_reset_email.html')

def password_reset_otp(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        if int(otp) == request.session.get('reset_otp'):
            return redirect('password_reset_confirm')
    return render(request, 'password_reset_otp.html')

def password_reset_confirm(request):
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            email = request.session.get('reset_email')
            user = User.objects.filter(email=email).first()
            if user:
                user.set_password(new_password)
                user.save()
                return redirect('login')
    return render(request, 'password_reset_confirm.html')


def post_list(request):
    context={}
    posts = Post.objects.all()
    context["posts"]=posts
    return render(request,"blogs.html",context)


def team(request):
    context = {}
    members = TeamMember.objects.all()
    context["members"] = members
    return render(request, 'team.html', context)



def ulogin(request):
    if request.method == "POST":
        e = request.POST["username"]
        p = request.POST["password"]
        print(e, p)
        
        if e == "" or p == "":
            messages.error(request, "Fields cannot be empty. Please fill all the fields.")
            return render(request, 'login.html')
        else:
            u = authenticate(username=e, password=p)
            print(u)
            if u is not None:
                login(request, u)
                messages.success(request, "Login successfully!")
                return redirect('/index')
            else:
                messages.error(request, "Username and password do not match.")
                return render(request, 'login.html')          
    return render(request, "login.html")


def ulogout(request):
    logout(request)
    return redirect('/index')
    return render(request,"logout.html")


def send_notification_email(subject, message, recipient_list):
    from django.core.mail import send_mail
    from_email = 'daddyinfo1@gmail.com'
    send_mail(subject, message, from_email, recipient_list)

def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        cpassword = request.POST["cpassword"]
        print(name, email, password, cpassword)

        if not all([name, email, password, cpassword]):
            messages.error(request, "Fields cannot be empty. Please fill all the fields.")
            return render(request, 'register.html')
        elif password != cpassword:
            messages.error(request, "Passwords do not match. Please re-enter your password.")
            return render(request, 'register.html')
        else:
            try:
                u = User.objects.create(username=name, email=email)
                u.set_password(password)
                u.save()
                messages.success(request, "Registration successful!")
                subject = "THE DADDY'S RESTAURANT!"
                message = f'Thank you for registering, {name}! Our team takes care of your taste and we serve the world\'s best quality of food. We are confident that this is not the last time we will serve you. We are always at your service. THANK YOU!!!'
                send_notification_email(subject, message, [email])
            except IntegrityError:
                messages.error(request, "A user with this email or username already exists.")
                return render(request, "register.html")
            return redirect('/ulogin')
    return render(request, 'register.html')

def menu(request):
    context={}
    menuitems=MenuItem.objects.all()
    print(menuitems)
    context["menuitems"]=menuitems
    print(request.user.is_authenticated)
    return render(request,"menu.html",context)


def filterbycategory(request,cid):
    context={}
    menuitems=MenuItem.objects.filter(category=int(cid))
    categories = MenuItem.objects.filter(category=int(cid))
    context["menuitems"]=menuitems
    context["categories"] = categories
    return render(request,'menu.html',context)


def filterbytype(request,tid):
    context={}
    menuitems=MenuItem.objects.filter(type=int(tid))
    types = MenuItem.objects.filter(category=int(tid))
    context["menuitems"]=menuitems
    context["types"]=types
    return render(request,'menu.html',context)


def service(request):
    return render(request,"service.html")



# def contact(request):
#     if request.method == 'POST':
#         na = request.POST['user']
#         ph = request.POST['phone']
#         em = request.POST['email']
#         su = request.POST['subject']
#         me = request.POST['message']

#         contact_form = ContactForm(name=na,phone=ph,email=em,subject=su,message=me)
#         contact_form.save()
#         messages.success(request, 'Your message has been sent successfully!')
#         return redirect('/contact')

#     return render(request, 'contact.html')

def contact(request):
    if request.method == 'POST':
        na = request.POST['user']
        ph = request.POST['phone']
        em = request.POST['email']
        su = request.POST['subject']
        me = request.POST['message']

        # Save the contact form
        contact_form = ContactForm(name=na, phone=ph, email=em, subject=su, message=me)
        contact_form.save()

        # Send confirmation email to the user
        subject = 'Contact Form Submission Confirmation'
        message = f'Thank you {na} for reaching out to us. We have received your query and will get back to you soon.\n\nYour Query:\nSubject: {su}\nMessage: {me}'
        from_email = 'your-email@gmail.com'
        recipient_list = [em]

        try:
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, 'Your message has been sent successfully! A confirmation email has been sent to your email address.')
        except Exception as e:
            messages.error(request, 'Your message was sent, but we were unable to send a confirmation email. Please check your email configuration.')

        return redirect('/contact')

    return render(request, 'contact.html')


def queryviews(request):
    if request.user.is_authenticated:
        context={}
        querys = ContactForm.objects.filter(email=request.user.email).order_by('-is_solved')
        context['querys']=querys
        return render(request,'querys.html',context)
    else:
        return redirect('/ulogin')


def savebooking(request):
    if request.method == 'POST':
        n = request.POST['username']
        e = request.POST['email']
        dt = request.POST['datetime']
        num = request.POST['peoples']
        s = request.POST['message']
        try:
            datetime = timezone.datetime.strptime(dt, '%m/%d/%Y %I:%M %p')
        except ValueError:
            messages.error(request, 'Invalid datetime format. Please use mm/dd/yyyy hh:mm AM/PM format.')
        # Create a new reservation object
        booking = Reservation(name=n,email=e,date_time=datetime,num_people=num,special_request=s)
        booking.save()
        sms='your reservation table has been successfully reserved'
        subject = 'Table Reservation Confirmation'
        message = f'Thank you for your reservation. Your table has been reserved for {datetime.strftime("%m/%d/%Y %I:%M %p")}.'
        from_email = 'your-email@gmail.com'
        recipient_list = [e]
        try:
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, 'Your message has been sent successfully! A confirmation email has been sent to your email address.')
        except Exception as e:
            messages.error(request, 'Your message was sent, but we were unable to send a confirmation email. Please check your email configuration.')
    return render(request,"booking.html")


def reservation_view(request):
    context = {}
    if request.user.is_authenticated:
        reservations = Reservation.objects.filter(email=request.user.email).order_by('-is_reserved')
        context["reservations"] = reservations
        if reservations.exists():
            reservations.update(is_completed=True)
            # reservations.delete()
            return render(request, 'reservations.html', context)
        else:
            messages.error(request, "No upcoming reservations.")
            return render(request,'reservations.html',context)
    else:
        return redirect('/ulogin')


def reviews(request):
    if request.method=='POST':
        n=request.POST['username']
        p=request.POST['prof']
        t=request.POST['client']
        r=request.POST['rating']
        i=request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(i.name, i)
        c=Testimonial(name=n,profession=p,testimonial=t,rating=r,image=filename)
        c.save()
    
    return render(request,'reviews.html')


def testimonial(request):
    context={}
    testimonials=Testimonial.objects.all()
    context["testimonials"]= testimonials
    return render(request,"testimonial.html",context)



def addtocart(request,mid):
    context={}
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        m=MenuItem.objects.filter(id=mid)
        q1=Q(userid=u[0])
        q2=Q(mid=m[0])
        c=Cart.objects.filter(q1&q2)
        n=len(c)
        context["menuitems"]=m
        if n==1:
            messages.error=(request,"Product is already Existed")
            return render(request,'menu.html',context)
        else:
            cart=Cart.objects.create(mid=m[0],userid=u[0])
            cart.save()
            # Send confirmation email to the user
            subject = 'Item Added to Your Cart'
            message = f'Dear {u},\n\nYou have successfully added {m} to your cart.\n\n your total items {n}.\n\nThank you for order with us!\n\nBest regards,\nDadys Restaurant'
            from_email = 'daddysinfo1@gmail.com'
            recipient_list = [request.user.email]
            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, 'Your item has been added successfully! A confirmation email has been sent to your email address.')
            except Exception as e:
                messages.error(request, 'Your message was sent, but we were unable to send a confirmation email. Please check your email configuration.')
            return render(request,'menu.html',context)
    else:
        return redirect("/login")


def viewcart(request):
    context={}
    if request.user.is_authenticated:
        c=Cart.objects.filter(userid=request.user.id)
        context["carts"]=c
        totalqty=0
        totalprice=0
        actualprice=0
        for i in c:
            totalqty=totalqty+i.qty
            totalprice=totalprice+i.qty*i.mid.price
            actualprice=actualprice+i.mid.price
        print(totalqty)
        print(totalprice)
        context["price"]=totalprice
        context["items"]=totalqty
        context["actual"]=actualprice
        return render(request,'cart.html',context)
    else:
        return redirect("/ulogin")

  
def removecart(request,cid):
    context={}
    c=Cart.objects.filter(id=cid)
    c.delete()
    messages.success=(request,"cart removed successfully")
    c=Cart.objects.filter(userid=request.user.id)
    
    context["carts"]=c
    # print(c)
    return render(request,"cart.html",context)


def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    if x=="1":
        q=q+1
    elif q>1:
        q=q-1
    c.update(qty=q)
    messages.success=(request,"cart updated successfully")
    return redirect("/viewcart")


import random
def conformorder(request):
    c = Cart.objects.filter(userid=request.user.id)
    oid = random.randint(11111, 99999)
    print(oid)
    amount = 0

    for x in c:
        amount += x.qty * x.mid.price
        o = Order.objects.create(order_id=oid, amt=amount, qty=x.qty ,m_id=x.mid, user_id=x.userid)
        o.save()
        c.delete()
        request.session['current_order_id'] = oid
        subject = 'Order Confirmation'
        message = f'Thank you for your order. Your order ID is {oid}. The total amount is {amount:.2f}.'
        from_email = 'daddyinfo1@gmail.com'
        recipient_list = [request.user.email]
        try:
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, 'Your order has been successfully confirmed! A confirmation email has been sent to your email address.')
        except Exception as e:
            messages.error(request, 'Your order was placed, but we were unable to send a confirmation email. Please check your email configuration.')
    return redirect("/fetchorder")

def fetchorder(request):
    context = {}
    current_order_id = request.session.get('current_order_id')
    
    if current_order_id:
        orders = Order.objects.filter(user_id=request.user.id, order_id=current_order_id)
    else:
        orders = Order.objects.none()
    
    context["orders"] = orders
    sum=0
    count=0
    for order in orders:
        sum = order.amt
        count=order.qty
    context["n"]=count
    context["total"] = sum
    
    print(count)
    print(sum)
    return render(request, "pay.html", context)

# def conformorder(request):
#     c=Cart.objects.filter(userid=request.user.id)
#     oid=random.randint(11111,99999)
#     print(oid)
#     amount=0

#     for x in c:
#         amount+=x.qty*x.mid.price
#         o=Order.objects.create(order_id=oid,amt=amount,m_id=x.mid,user_id=x.userid)
#         o.save()
#         subject = 'Order Confirmation'
#         message = f'Thank you for your order. Your order ID is {oid}. The total amount is {amount:.2f}.'
#         from_email = 'daddyinfo1@gmail.com'
#         recipient_list = [request.user.email]
#         try:
#             send_mail(subject, message, from_email, recipient_list)
#             messages.success(request, 'Your order has been added successfully conformed! A confirmation email has been sent to your email address.')
#         except Exception as e:
#             messages.error(request, 'Your message was sent, but we were unable to send a confirmation email. Please check your email configuration.')
#     return redirect("/fetchorder")


# def fetchorder(request):
#     context={}
#     orders=Order.objects.filter(user_id=request.user.id)
#     context["orders"]=orders
#     sum=0
#     context['n']=len(orders)
#     for order in orders:
#         sum=order.amt
#     context["total"]=sum
#     print(sum)
#     return render(request,"pay.html",context)


def track(request):
    if request.user.is_authenticated:
        context = {}
        trackers = Order.objects.filter(user_id=request.user.id).order_by('-is_ready')
        context["trackers"] = trackers
        completed_orders = trackers.filter(is_ready=True)
        pending_orders = trackers.filter(is_ready=False)
        completed_orders.delete()
        return render(request,'track.html',context)
    else:
        return redirect('/ulogin')

# def makepayment(request):
#     client = razorpay.Client(auth=("RAZORPAY_API_KEY", "RAZORPAY_SECRET_KEY"))
#     context = {}
#     orders = Order.objects.filter(user_id=request.user.id)
#     context["orders"] = orders
#     total_amount = orders.aggregate(total_amount=Sum(F('m_id.amt') * F('qty')))['total_amount'] or 0
#     last_order_id = orders.aggregate(last_order_id=Max('order_id'))['last_order_id'] or 'order_rcptid_11'
#     data = {
#         "amount": float(total_amount * 100),
#         "currency": "INR",
#         "receipt": last_order_id  
#     }
#     payment = client.order.create(data=data)
#     context["payment"] = payment
#     print(payment)
#     return redirect(request,"/paymentsuccess")

def makepayment(request):
    orders=Order.objects.filter(user_id=request.user.id)
    s=0
    for x in orders:
        s=x.amt*x.qty
        oid=x.order_id

    client= razorpay.Client(auth=("RAZORPAY_API_KEY", "RAZORPAY_SECRET_KEY"))
    data={"amount":s, "currency":"INR", "receipt":oid}
    payment=client.order.create(data=data)
    print(payment)
    orders.delete()
    return HttpResponse('/paymentsuccess')




@csrf_exempt
def paymentsuccess(request):
    context={}
    if request.method == 'POST':
        payment=request.POST['order_id']
        paymentid= request.POST['razorpay_payment_id']
        orderid = request.POST['razorpay_order_id']
        signature = request.POST['razorpay_signature']
        p=Payment(razorpay_payment_id=paymentid,razorpay_order_id=orderid,razorpay_signature=signature, order=o,amount=s,is_paid=True)
        p.save()
        print(p)


        client = razorpay.Client(auth=("RAZORPAY_API_KEY", "RAZORPAY_SECRET_KEY"))
        client.utility.verify_payment_signature({'razorpay_order_id': orderid, 'razorpay_payment_id': paymentid,  'razorpay_signature': signature})
        orders = Order.objects.filter(user_id=request.user.id)
        for order in orders:
            s=order.amt*order.qty
            o=order.order_id
            order.is_Paid = True    
            order.save()# Store payment details in your Payment model

        payment = Payment.objects.create(order=orders.first(), razorpay_payment_id=paymentid, razorpay_order_id=orderid,rozarpay_signature_id=signature , is_Paid=True, amount=s )
        payment.save()
        print(payment)    
        send_invoice_email(request.user, orders, s)
            # Clear the user's cart
        orders.delete()

        context = {'payment': payment,'total_amount': s}
    return render(request, 'paymentsuccess.html',context)

def send_invoice_email(user, orders, total_amount):
    subject = "Your Order Invoice"
    message = render_to_string('invoice_email.html', {
        'user': user,
        'orders': orders,
        'total_amount': total_amount
    })
    email = EmailMessage(subject, message, to=[user.email])
    email.send()

