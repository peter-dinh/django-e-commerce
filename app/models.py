# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.db import connection  

from django.contrib.auth import get_user_model


# from collections import namedtuple

# # fucntion get queryset in stored procedure
# def namedtuplefetchall(cursor):
#     "Return all rows from a cursor as a namedtuple"
#     desc = cursor.description
#     nt_result = namedtuple('Result', [col[0] for col in desc])
#     return [nt_result(*row) for row in cursor.fetchall()]


# def dictfetchall(cursor):
#     "Return all rows from a cursor as a dict"
#     columns = [col[0] for col in cursor.description]
#     return [
#         dict(zip(columns, row))
#         for row in cursor.fetchall()
#     ]

# fuction try catch delete foreign key
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

# Create your models here.
class thongsocamera(models.Model):
    diemmanh = models.CharField(max_length = 100)
    thongsocoban = models.CharField(max_length = 100)
    dacdiem = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.thongsocoban.encode('utf8')

    class Meta:
        verbose_name_plural = 'Thông số camera'
        db_table = 'thongsocamera' 

class ketnoi(models.Model):
    wlan =  models.CharField(max_length = 100)
    bluetooth = models.CharField(max_length = 100)
    gps = models.CharField(max_length = 100)

    def __str__(self):
        return self.wlan.encode('utf8')

    class Meta:
        verbose_name_plural = 'Kết nối'
        db_table = 'ketnoi' 

class dongsanpham(models.Model):
    tendongsanpham = models.CharField(max_length=200)

    def __str__(self):
        return self.tendongsanpham.encode('utf8')

    class Meta:
        verbose_name_plural = 'Dòng sản phẩm'
        db_table = 'dongsanpham'

    @staticmethod   
    def getlist():  
        # create a cursor  
        cur = connection.cursor()  
        # execute the stored procedure passing in   
        # search_string as a parameter  
        cur.callproc('WSP_DanhSachDongSanPham', [])  
        # grab the results  
        results = cur.fetchall()  
        cur.close()  
  
        # wrap the results up into Document domain objects   
        return [dongsanpham(*row) for row in results]  

class tuychon(models.Model):
    mausac = models.CharField(max_length = 100)
    bonhotrong = models.CharField(max_length = 100)
    
    def __str__(self):
        return (self.mausac + " | " +self.bonhotrong).encode('utf8')

    class Meta:
        verbose_name_plural = 'Tùy chọn'
        db_table = 'tuychon' 

class sanpham(models.Model):
    tensp = models.CharField(max_length = 200)
    kichthuocman = models.CharField(max_length = 100)
    thongsoman = models.CharField(max_length = 100)
    pin = models.CharField(max_length = 100)
    macameratruoc = models.ForeignKey(thongsocamera,  on_delete=models.SET(get_sentinel_user), related_name='camera_truoc')
    macamerasau = models.ForeignKey(thongsocamera,  on_delete=models.SET(get_sentinel_user), related_name='camera_sau')
    kichthuoc = models.CharField(max_length = 100)
    khoiluong = models.CharField(max_length = 100)
    thoidiemramat = models.DateField()
    chipset = models.CharField(max_length = 100)
    tscpu = models.CharField(max_length = 100)
    bonhoram = models.CharField(max_length = 100)
    ketnoi = models.ForeignKey(ketnoi, on_delete=models.SET(get_sentinel_user))
    hedieuhanh = models.CharField(max_length = 100)
    baomatvantay = models.CharField(max_length = 100)
    chongnuoc = models.CharField(max_length = 100)
    dongsp_catalog = models.ForeignKey(dongsanpham,  on_delete=models.SET(get_sentinel_user))
    
    
    def __str__(self):
        return self.tensp.encode('utf8')

    class Meta:
        verbose_name_plural = 'Sản phẩm'
        db_table = 'sanpham'

class sanphamtuychon(models.Model):
    ma_sp =  models.ForeignKey(sanpham, on_delete=models.CASCADE)
    ma_tuy_chon =  models.ForeignKey(tuychon,  on_delete=models.SET(get_sentinel_user),)
    soluong = models.IntegerField(default=0)
    giasanpham = models.DecimalField(max_digits=12, decimal_places=2)
    anhdaidien = models.ImageField(upload_to='media')
    LOCK_CHOICES = ((True, 'Lock'), (False, 'UnLock'))
    locked = models.BooleanField(choices=LOCK_CHOICES, default=False)
    
    def __str__(self):
        return (self.ma_sp.tensp + " | " + self.ma_tuy_chon.mausac).encode('utf8')

    @staticmethod   
    def getlistdongsanpham(id_catalog):  
        # create a cursor  
        cur = connection.cursor()  
        # execute the stored procedure passing in   
        # search_string as a parameter  
        cur.callproc('WSP_IphoneCatalog', [id_catalog])  
        # grab the results  
        results = cur.fetchall()  
        cur.close()  
  
        # wrap the results up into Document domain objects   
        return results

    @staticmethod
    def danhsachIPhone8():
        cur = connection.cursor()
        cur.callproc('WSP_Iphone8', [])
        results = cur.fetchall()
        cur.close()

        return results
    @staticmethod
    def danhsachIPhone7():
        cur = connection.cursor()
        cur.callproc('WSP_Iphone7', [])
        results = cur.fetchall()
        cur.close()

        return results

    @staticmethod
    def danhsachIPhone6():
        cur = connection.cursor()
        cur.callproc('WSP_Iphone6', [])
        results = cur.fetchall()
        cur.close()

        return results

    @staticmethod
    def danhsachIPhone5():
        cur = connection.cursor()
        cur.callproc('WSP_Iphone5', [])
        results = cur.fetchall()
        cur.close()

        return results

    @staticmethod
    def danhsachSanPhamMoi():
        cur = connection.cursor()
        cur.callproc('WSP_SanPhamMoi', [])
        results = cur.fetchall()
        cur.close()
        return results

    @staticmethod
    def danhsachSanPhamBan():
        cur = connection.cursor()
        cur.callproc('WSP_SanPhamBan', [])
        results = cur.fetchall()
        cur.close()
        return results

    @staticmethod
    def  danhsachTimKiem(keyword):
        cur = connection.cursor()
        cur.callproc('WSP_TimKiem', [keyword])
        results = cur.fetchall()
        cur.close()
        return results
    
    @staticmethod
    def Sanphamcungloai(id_catalog):
        cur = connection.cursor()
        cur.callproc('WSP_SanPhamCungLoai', [id_catalog])
        results = cur.fetchall()
        cur.close()
        return results

    # @staticmethod
    # def laythongtinsanpham():
    #     cur = connection.cursor()
    #     cur.callproc('WSP_SanPhamBan', [])
    #     results = cur.fetchall()
    #     cur.close()
    #     return results


    def image_tag(self):
        return u'<img src="http://localhost:8000/media/%s" width="200" />'  %(self.anhdaidien)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    class Meta:
        verbose_name_plural = 'Sản phẩm đang bán'
        db_table = 'sanphamtuychon' 


#
#   Tai Khoan
#
class taikhoan(models.Model):
    username = models.CharField(unique=True, max_length = 50)
    password = models.CharField(max_length = 50)
    hovaten = models.CharField(max_length = 100, null=True)
    sinhnhat = models.DateField(null=True)
    SEX_CHOICES = ((True, 'Nam'), (False, 'Nu'))
    gioitinh = models.BooleanField(default=True)
    sodienthoai = models.CharField(max_length = 12,null=True)
    email = models.EmailField(unique = True)
    diachi = models.TextField(max_length=None, null=True)
    
    def __str__ (self):
        return self.username.encode('utf8')

    # def check_login( username, password):
    #     cur = connection.cursor()  

    #     cur.callproc('WSP_Login', [username, password])  
    #     results = cur.fetchall()  
    #     cur.close()  
  
    #     return results

    class Meta:
        verbose_name_plural = 'Tài khoản'
        db_table = 'taikhoan' 



class phieunhap(models.Model):
    imei_may = models.CharField(max_length=50, unique =True, primary_key=True)
    masanphamtuychon = models.ForeignKey(sanphamtuychon,  on_delete=models.SET(get_sentinel_user))
    ngaylap = models.DateTimeField(auto_now=True)
    gia = models.DecimalField(max_digits=12, decimal_places=2)
    LOCK_CHOICES = ((True, 'Lock'), (False, 'UnLock'))
    locked = models.BooleanField(choices=LOCK_CHOICES, default=False)
    ghichu = models.TextField()

    def __str__(self):
        return self.imei_may.encode('utf8')

    class Meta:
        verbose_name_plural = 'Phiếu nhập'
        db_table = 'phieunhap' 


class kho(models.Model):
    imei_may = models.OneToOneField(phieunhap, primary_key=True,  on_delete=models.SET(get_sentinel_user),)
    masanphamtuychon = models.ForeignKey(sanphamtuychon,  on_delete=models.SET(get_sentinel_user),)
    trangthaiban = models.BooleanField()
    
    def __str__(self):
        return self.imei_may.imei_may.encode('utf8')

    class Meta:
        verbose_name_plural = 'Kho'
        db_table = 'kho' 


class hoadon(models.Model):
    user_khachhang = models.ForeignKey(taikhoan,  on_delete=models.SET(get_sentinel_user), related_name='khachhang')
    tonggia = models.DecimalField(max_digits=12, decimal_places=2, default= 0)
    ngaylap = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = ((0, 'Cancel'), (1, 'Success'), (2, 'Processing'))
    trangthai = models.IntegerField(choices=STATUS_CHOICES, default=2)
    LOCK_CHOICES = ((True, 'Lock'), (False, 'UnLock'))
    locked = models.BooleanField(choices=LOCK_CHOICES, default=False)
    sodienthoai = models.CharField(max_length = 12)
    ghichu = models.TextField()

    def __str__(self):
        return self.user_khachhang.username.encode('utf8')

    class Meta:
        verbose_name_plural = 'Hóa đơn'
        db_table = 'hoadon' 
    
class hoadonchitiet(models.Model):
    mahoadon = models.ForeignKey(hoadon,  on_delete=models.SET(get_sentinel_user),)
    masanphamtuychon = models.ForeignKey(sanphamtuychon,  on_delete=models.SET(get_sentinel_user),)
    gia = models.DecimalField(max_digits=12, decimal_places=2)
    soluong = models.IntegerField(default=1)
    LOCK_CHOICES = ((True, 'Lock'), (False, 'UnLock'))
    locked = models.BooleanField(choices=LOCK_CHOICES, default=False)

    def __str__(self):
        return (self.masanphamtuychon.ma_sp.tensp + " | " + self.masanphamtuychon.ma_tuy_chon.mausac).encode('utf8')

    class Meta:
        verbose_name_plural = 'Hóa đơn chi tiết'
        db_table = 'hoadonchitiet' 


class phieuxuat(models.Model):
    mahoadon = models.ForeignKey(hoadon,  on_delete=models.SET(get_sentinel_user),)
    ngaylap = models.DateTimeField(auto_now=True)
    imei_may = models.ForeignKey(kho,  on_delete=models.SET(get_sentinel_user))
    LOCK_CHOICES = ((True, 'Lock'), (False, 'UnLock'))
    locked = models.BooleanField(choices=LOCK_CHOICES, default=False)
    ghichu = models.TextField()
    
    def __str__(self):
        return self.imei_may.encode('utf8')
    
    class Meta:
        verbose_name_plural = 'Phiếu xuất'
        db_table = 'phieuxuat' 