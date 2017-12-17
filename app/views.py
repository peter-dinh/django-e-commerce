# coding=utf-8
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .models import dongsanpham, taikhoan, sanpham, sanphamtuychon, hoadon, hoadonchitiet
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib.auth.hashers import make_password
from carton.cart import Cart

from .models import *
from django.shortcuts import render_to_response
from django.template import RequestContext


def handler404(request):
    response = render_to_response('app/404.html', {},context_instance=RequestContext(request))
    response.status_code = 404
    return response

def myView(request, param):
    if not param:
        raise Http404
    return render_to_response('app/404.html')



def index(request):
    # viet bang stored
    catalog = dongsanpham.getlist()  

    iphone8 = sanphamtuychon.danhsachIPhone8()
    iphone7 = sanphamtuychon.danhsachIPhone7()
    iphone6 = sanphamtuychon.danhsachIPhone6()
    iphone5 = sanphamtuychon.danhsachIPhone5()
    sanphammoi= sanphamtuychon.danhsachSanPhamMoi()
    sanphamban = sanphamtuychon.danhsachSanPhamBan()

    return render(request, 'app/index.html', {
        'catalog'   : catalog,
        'iphone8'   :  iphone8,
        'iphone7'   :  iphone7,
        'iphone6'   :  iphone6,
        'iphone5'   :  iphone5,
        'sanphammoi1': sanphammoi[0:4],
        'sanphammoi2': sanphammoi[4:8],
        'sanphamban': sanphamban,
    })

def login(request):
    
    if 'id_khachhang' in request.session:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        passsword = make_password(request.POST.get('password'), None, 'unsalted_md5')
        result = taikhoan.objects.filter(username= username, password = passsword)
        if result:
            request.session['id_khachhang'] = result[0].id
            return redirect('/')
        else:
            return redirect('login')
        
    return render(request, 'app/login.html')

def logout(request):
    if 'id_khachhang' in request.session: 
        del request.session['id_khachhang']
    else:
        messages.warning(request, message='You must signin in system', extra_tags='alert')
        return redirect('/')
    return redirect('/')

def register(request):

    if 'id_khachhang' in request.session:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('r_user')
        email = request.POST.get('r_email')
        passsword = make_password(request.POST.get('r_pass'), None, 'unsalted_md5')
        
        if username == "":
            messages.warning(request, message="Username không được để trống!", extra_tags='alert')
            return redirect('/login')

        if passsword == "":
            messages.warning(request, message="Password không được để trống!", extra_tags='alert')
            return redirect('/login')

        if email == "":
            messages.warning(request, message="Email không được để trốngg", extra_tags='alert')
            return redirect('/login')

        try:
            taikhoan.objects.get(username=username)
            messages.warning(request, message="Username đã tồn tạii!", extra_tags='alert')
            return redirect('/login')
        except:
            pass
        try:
            taikhoan.objects.get(email=email)
            messages.warning(request, message="Email da ton tai", extra_tags='alert')
            return redirect('/login')
        except:
            pass

        insert = taikhoan.objects.create(username = username, email = email, password = passsword)
        if insert.id:
            messages.success(request, message="Them thanh cong", extra_tags='alert')
        else:
            messages.success(request, message="Them that bai", extra_tags='alert')

    return redirect('/login')

def cart(request):

    if 'id_khachhang' in request.session:
        thongtintaikhoan = taikhoan.objects.get(id=request.session['id_khachhang'])
    else:
        thongtintaikhoan=()

    
    # kiem tra dang nhap
    cart = Cart(request.session)
    
    return render(request, 'app/cart.html', {
            'taikhoan': thongtintaikhoan
        })
    
def add(request, id):
    cart = Cart(request.session)
    try:
        product = sanphamtuychon.objects.get(id=id)
        sp = sanpham.objects.get(id = product.ma_sp_id)
        tc = tuychon.objects.get(id = product.ma_tuy_chon_id)
        product.ma_tuy_chon_id = tc
        product.ma_sp_id = sp
    except:
        messages.warning(request, message="Sản phẩm không tồi tại", extra_tags='alert')
        return redirect('/')
    
    if product.soluong <= 0:
        messages.warning(request, message='Sản phẩm đã hết hàng', extra_tags='alert')
        return redirect('/')
    
    for x in cart.items:
        if x.product.id == product.id:
            if x.product.soluong <= x.quantity:
                messages.warning(request, message='Sản phẩm đã hết hàng', extra_tags='alert')
                return redirect('/')

    cart.add(product, price=product.giasanpham, quantity=1)
    return redirect('/cart')

def set_quatity(request):
    cart = Cart(request.session)
    try:
        product = sanphamtuychon.objects.get(id=request.GET.get('id'))
    except:
        messages.warning(request, message="Lỗi", extra_tags='alert')
        return redirect('/cart')
    qty = request.GET.get('qty')
    if qty <= '0':
        print 'Không sửa được'
        messages.warning(request, message="Không sửa được", extra_tags='alert')
        return redirect('/cart')
    count = product.soluong
    for x in cart.items:
        if x.product.id == product.id:
            
            if long(qty) > count:
                print 'Số lượng sản phẩm không đủ'
                messages.warning(request, message='Số lượng sản phẩm không đủ', extra_tags='alert')
                return redirect('/cart')
            else:
                print 'Sửa thành công'
                cart.set_quantity(product, quantity=qty)
                messages.success(request, message="Sửa thành công", extra_tags='alert')
                return redirect('/cart')
        else:
            print 'Sản phẩm không có trong giỏ hàng!'
            messages.success(request, message="Sản phẩm không có trong giỏ hàng!", extra_tags='alert')
            return redirect('/cart')

    return redirect('/cart')

def remove(request, id):
    cart = Cart(request.session)
    product = sanphamtuychon.objects.filter(id=id)
    cart.remove(product[0])
    messages.success(request, message='Sản phẩm đã được xóa', extra_tags='alert')
    return redirect('/cart')

def clear(request):
    cart = Cart(request.session)
    cart.clear()
    messages.success(request, message='Danh sách sản phẩm đã được xóa!', extra_tags='alert')
    return redirect('/cart')

def info(request, id_sanphamtuychon):
    catalog = dongsanpham.getlist()  
    try:
        get_sanphamtuychon = sanphamtuychon.objects.get(id=id_sanphamtuychon)
    except:
        messages.warning(request, message='Sản phẩm không tồn tại', extra_tags='alert')
        return redirect('/')
    get_sanpham = sanpham.objects.get(id = get_sanphamtuychon.ma_sp_id)
    get_ketnoi = ketnoi.objects.get(id=get_sanpham.ketnoi_id)
    get_cameratruoc = thongsocamera.objects.get(id=get_sanpham.macameratruoc_id)
    get_camerasau = thongsocamera.objects.get(id=get_sanpham.macamerasau_id)
    get_dongsanpham = dongsanpham.objects.get(id=get_sanpham.dongsp_catalog_id)
    get_tuychon = tuychon.objects.get(id = get_sanphamtuychon.ma_tuy_chon_id)

    get_sanpham.ketnoi_id = get_ketnoi
    get_sanpham.macameratruoc_id = get_cameratruoc
    get_sanpham.macamerasau_id = get_camerasau
    get_sanpham.dongsp_catalog_id = get_dongsanpham
    get_sanphamtuychon.ma_sp_id = get_sanpham
    get_sanphamtuychon.ma_tuy_chon_id = get_tuychon

    get_sanphamcungloai = sanphamtuychon.Sanphamcungloai(get_sanphamtuychon.ma_sp_id.dongsp_catalog_id.id)
   
    

    return render(request, 'app/product-details.html',{
        'catalog': catalog,
        'sanpham': get_sanphamtuychon,
        'danhsachcungloai1': get_sanphamcungloai[0:3],
        'danhsachcungloai2': get_sanphamcungloai[3:6],
    })

def catalog(request, id_catalog):
    danhsachsanpham = sanphamtuychon.getlistdongsanpham(id_catalog)
    catalog = dongsanpham.getlist() 

    paginator = Paginator(danhsachsanpham, 15)

    page = request.GET.get('page')

    try:
        danhsach = paginator.page(page)
    except PageNotAnInteger:
        danhsach = paginator.page(1)
    except EmptyPage:
        danhsach = paginator.page(paginator.num_pages)

    return render(request, 'app/shop.html', {
        'danhsach' : danhsach,
        'catalog' : catalog,
    })

def search(request):
    catalog = dongsanpham.getlist() 
    if request.method == "POST": 
        request.session['r'] = request.POST.get("r")
    try:
        keyword = request.session['r']
    except:
        messages.warning(request, message='Bạn chưa nhập từ khóa', extra_tags='alert')
        return redirect('/')
    danhsachtimkiem = sanphamtuychon.danhsachTimKiem(keyword)
    paginator = Paginator(danhsachtimkiem, 15)

    page = request.GET.get('page')

    try:
        danhsach = paginator.page(page)
    except PageNotAnInteger:
        danhsach = paginator.page(1)
    except EmptyPage:
        danhsach = paginator.page(paginator.num_pages)

    return render(request, 'app/shop.html', {
        'catalog': catalog,
        'danhsach' : danhsach,
    })

def account(request):
    catalog = dongsanpham.getlist()  
    # kiem tra dang nhap
    if 'id_khachhang' not in request.session:
        messages.warning(request, message='Bạn chưa đang nhập vào hệ thống', extra_tags='alert')
        return redirect('/')
    khachhang = taikhoan.objects.get(id=request.session.get('id_khachhang'))
    

    if request.method == "POST":
        name = request.POST.get('name')
        birthday = request.POST.get('birthday')
        sex = request.POST.get('sex')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        khachhang.hovaten = name
        khachhang.sinhnhat = birthday   
        if  sex == '0':
            khachhang.gioitinh = False
        else:
            khachhang.gioitinh =  True
        khachhang.sodienthoai = phone
        if khachhang.email != email:
            try:
                taikhoan.objects.get(email=email)
                messages.warning(request, message="Email đã tồn tại!", extra_tags='alert')
                return redirect('/account')
            except:
                khachhang.email = email

        khachhang.diachi = address

        try:
            khachhang.save()
        except:
            messages.warning(request, message="Ngày sinh không hợp lệ ", extra_tags='alert')
            return redirect('/account')
        messages.success(request, message="Thành công", extra_tags='alert')
        return redirect('/account')

    return render(request, 'app/account.html', {
            'khachhang' : khachhang,
            'catalog': catalog,
        })

def bill(request):
    catalog = dongsanpham.getlist()  
    # kiem tra dang nhap
    if 'id_khachhang' not in request.session:
        messages.warning(request, message='Bạn chưa đăng nhập vào hệ thống', extra_tags='alert')
        return redirect('/')

    danhsachhoadon = hoadon.objects.filter(user_khachhang_id=request.session['id_khachhang']).order_by('-id')


    return render(request, 'app/bill.html', {
        'danhsachhoadon': danhsachhoadon,
        'catalog': catalog
    })

def bill_info(request, id_bill):
    catalog = dongsanpham.getlist()  
    # kiem tra dang nhap
    if 'id_khachhang' not in request.session:
        messages.warning(request, message='Bạn chưa đăng nhập vào hệ thống', extra_tags='alert')
        return redirect('/')
    
    get_hoadon = hoadon.objects.get(id=id_bill)
    get_taikhoan = taikhoan.objects.get(id=get_hoadon.user_khachhang_id)
    get_hoadon.user_khachhang_id = get_taikhoan
    
    get_hoadonchitiet = hoadonchitiet.objects.filter(mahoadon_id=get_hoadon)
    for item in get_hoadonchitiet:
        get_sanphamtuychon = sanphamtuychon.objects.get(id=item.masanphamtuychon_id)
        get_sanpham = sanpham.objects.get(id=get_sanphamtuychon.ma_sp_id)
        get_sanphamtuychon.ma_sp_id = get_sanpham
        item.masanphamtuychon_id = get_sanphamtuychon

    

    return render(request, 'app/bill_info.html', {
            'catalog': catalog,
            'hoadon': get_hoadon,
            'hoadonchitiet': get_hoadonchitiet,
        })

def submit(request):
    if 'id_khachhang' not in request.session:
        messages.warning(request, message='Bạn chưa đăng nhập vào hệ thống', extra_tags='alert')
        return redirect('/cart')
    thongtintaikhoan = taikhoan.objects.get(id=request.session['id_khachhang'])
    if request.method == "POST":
        # try:
            cart = Cart(request.session)
            if cart.unique_count > 0:
                sodienthoai = request.POST.get('phone')
                if sodienthoai == "":
                    messages.warning(request, message='Bạn chưa nhập số điện thoại', extra_tags='alert')
                    return redirect('/cart')

                diachi = request.POST.get('address')
                if diachi == "":
                    messages.warning(request, message='Bạn chưa nhập địa chỉ', extra_tags='alert')
                    return redirect('/cart')
                # trang thai 1: thanh cong, 0: that bai, 2: dang xu ly, 3 da thanh toan
                insert_bill = hoadon(tonggia=0, trangthai=2, locked=0, sodienthoai=sodienthoai, ghichu=diachi, user_khachhang_id=request.session['id_khachhang'] )
                insert_bill.save()
                id_bill = insert_bill.id
                for item in cart.items:
                    insert_billinffo = hoadonchitiet(masanphamtuychon_id=item.product.id, mahoadon_id=id_bill, gia= item.price, soluong=item.quantity)
                    insert_billinffo.save()
                messages.success(request, message='Đơn đặt hàng đã được tạo', extra_tags='alert')
                cart.clear()
                return redirect('/bill')
            else:
                messages.warning(request, message='Bạn chưa chọn mua sản phẩm', extra_tags='alert')
                return redirect('/cart')
        # except:
        #     messages.warning(request, message='Bạn chưa chọn mua sản phẩm', extra_tags='alert')
        #     return redirect('/cart')

    return redirect('/cart')

def change_pass(request):
    catalog = dongsanpham.getlist()  
    # kiem tra dang nhap
    if 'id_khachhang' not in request.session:
        messages.warning(request, message='Bạn chưa đăng nhập vào hệ thống', extra_tags='alert')
        return redirect('/')
    
    khachhang = taikhoan.objects.get(id=request.session['id_khachhang'])

    if request.method == "POST":
        password = request.POST.get('pass')
        repeat = request.POST.get('repeat')
        
        if password == repeat:
            khachhang.password = make_password(password, None, 'unsalted_md5')
            khachhang.save()
            messages.success(request, message='Thay đổi thành công', extra_tags='alert')
            return redirect('/change_pass')
        else:
            messages.warning(request, message='Mật khẩu không trùng khớp', extra_tags='alert')
            return redirect('/change_pass')

    return render(request, 'app/change_pass.html',{
            'catalog': catalog,
        })

