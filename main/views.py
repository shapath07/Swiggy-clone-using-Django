from django.shortcuts import redirect, render, get_object_or_404
from .models import Category, Product, Order ,coupon ,OrderGroup
from .form import SignupForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

def home(request):
    return render(request, "main/home.html")

def category_list(request):
    categories = Category.objects.all()
    return render(request, "main/categories.html", {"categories": categories})

def product_list(request):
    categories = Category.objects.prefetch_related('product_set').all()
    return render(request, "main/product.html", {"categories": categories})

def final_bill(user,status = 'cart'):
    bill_amount = float(Order.objects.filter(user=user,status=status).aggregate(total=Sum('total_price'))['total'] or 0)
    return bill_amount

def order_list(request):
    user = request.user
    orders = Order.objects.filter(user=user,status='ordered')
    Your_bill = final_bill(user,status='ordered')
    amount_to_paid = request.session.get("discounted_bill", final_bill(user,status='ordered'))
    groups = OrderGroup.objects.filter(user=request.user).prefetch_related('order_set')

    

    return render(request, "main/order.html", {
        "orders": orders,
        "amount_to_paid": amount_to_paid,
        "Your_bill":Your_bill,
        "groups":groups}
        )

def cart(request):
    user = request.user
    orders = Order.objects.filter(user=user, status='cart')

    total_bill =  float(final_bill(user, status='cart'))
    amount_to_paid = request.session.get("discounted_bill", float(final_bill(user, status='cart')))
    coupon_applied = getattr(user, "coupon_applied", False)

    return render(request, "main/cart.html", {
        "orders": orders,
        "amount_to_paid": amount_to_paid,
        "total_bill":total_bill,
        "coupon_applied": coupon_applied
    }) 




def profile_view(request):
    if not request.user.is_authenticated:
         return redirect('login')
   
    user = request.user
    order = user.order_set.all()

    total_price = 0
    for orders in order:
        total_price += orders.product.price * orders.quantity

    return render(request, "main/profile.html", {"user": user,'orders':order})

def products_by_category(request, category_id):
    category = get_object_or_404(Category,id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, "main/products_by_category.html", {"category": category, "products": products})



def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = SignupForm()

    return render(request, 'main/signup.html', {'form': form})

        
    
def login_view(request):
         if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username=username,password=password)
            
            if user is not None:
                 login(request,user)
                 return redirect("home")
            
            else :
                 messages.error(request,"Wrong Credential or User not found , Signup first")
                 redirect('login')

         return render(request,'main/login.html')

@login_required
def logout_view(request):
     logout(request)
     messages.success(request,"You have succesfully logged out")
     return redirect("home")

def add_to_cart(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    product = get_object_or_404(Product,id=id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity",1)) 
        Order.objects.create(
            user = request.user,
            product=product,
            quantity=quantity,
            status='cart'
            )

    messages.success(request,"product succesfully added into cart")

    return redirect('products')




def apply_coupon(request):
    if request.method == "POST":
        c_code = request.POST.get("coupon","").strip()
        user = request.user
 
        try:
            cpn = coupon.objects.get(c_name=c_code)
        except coupon.DoesNotExist:
           return redirect("order_list")
        
        dis = int(''.join(filter(str.isdigit,cpn.c_name)))
        bill_amount = final_bill(user)
        new_bill = bill_amount - dis

        request.session["discounted_bill"] = new_bill

        user.discounted_bill = new_bill
        user.coupon_applied = True
        user.save()
        
       
        messages.success(request,f"coupon apllied ! You saved ₹{dis} , new_bill : ₹{new_bill} ")
        return redirect("Your_cart")

def cancelfromcart(request, id):
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        order = get_object_or_404(Order, id=id)

        remaining_qty = order.quantity - quantity

        if remaining_qty > 0:
            order.quantity = remaining_qty
            order.save()
        else:
            order.delete()

        messages.success(request, f"{quantity} item(s) removed from your cart.")
        return redirect("Your_cart")
    
def cancel_order(request, id):
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        order = get_object_or_404(Order, id=id)

        remaining_qty = order.quantity - quantity

        if remaining_qty > 0:
            order.quantity = remaining_qty
            order.save()
        else:
            order.delete()

        messages.success(request, f"{quantity} order succesfully canceled.")
        return redirect("orders")


def place_order(request):
    if request.method == "POST":
        user = request.user
        cart_items = Order.objects.filter(user=user, status='cart')

        if not cart_items.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect("Your_cart")

        total_amount = sum(item.total_price for item in cart_items)

        # Create a new order group
        group = OrderGroup.objects.create(user=user, total_amount=total_amount)

        # Assign group and update status
        for item in cart_items:
            item.status = 'ordered'
            item.group = group
            item.save()

        # Optionally clear discount
        request.session.pop("discounted_bill", None)
        user.discounted_bill = None
        user.coupon_applied = False
        user.save()

        messages.success(request, f"Order placed successfully! Group ID: {group.id}")
        return redirect("orders")

     
    
def view_details(request,name):
        product = get_object_or_404(Product,name=name)
        return render(request,"main/view_product.html",{"product":product})
    

         

            

    
        



     
     



     
                 
         

 
    
                 
                
     



