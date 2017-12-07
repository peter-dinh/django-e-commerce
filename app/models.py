from __future__ import unicode_literals

from django.db import models

from django.contrib.auth import get_user_model

# Create your models here.
class thongsocamera(models.Model):
    diemmanh = models.CharField(max_length = 100)
    thongsocoban = models.CharField(max_length = 100)
    dacdiem = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.thongsocoban.encode('utf8')

    class Meta:
        db_table = 'thongsocamera' 


class ketnoi(models.Model):
    wlan =  models.CharField(max_length = 100)
    bluetooth = models.CharField(max_length = 100)
    gps = models.CharField(max_length = 100)

    def __str__(self):
        return self.wlan.encode('utf8')

    class Meta:
        db_table = 'ketnoi' 

class tuychon(models.Model):
    mausac = models.CharField(max_length = 100)
    bonhotrong = models.CharField(max_length = 100)
    
    def __str__(self):
        return (self.mausac + " | " +self.bonhotrong).encode('utf8')

    class Meta:
        db_table = 'tuychon' 

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

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
    dongsp_catalog = models.CharField(max_length = 100)
    
    
    def __str__(self):
        return self.tensp.encode('utf8')

    class Meta:
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

    def image_tag(self):
        return u'<img src="http://localhost:8000/media/%s" width="200" />'  %(self.anhdaidien)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    class Meta:
        db_table = 'sanphamtuychon' 

class taikhoan(models.Model):
    username = models.CharField(unique=True, max_length = 50)
    password = models.CharField(unique = True, max_length = 50)
    hovaten = models.CharField(max_length = 100)
    sinhnhat = models.DateField()
    SEX_CHOICES = ((True, 'Nam'), (False, 'Nu'))
    gioitinh = models.BooleanField()
    sodienthoai = models.CharField(max_length = 12)
    email = models.EmailField(unique = True)
    diachi = models.TextField(max_length=None)
    ROLE_CHOICES = ((0, 'Customer'), (1, 'Staff'))
    loaitaikhoan = models.IntegerField(default=1, choices=ROLE_CHOICES)
    
    def __str__ (self):
        return self.username.encode('utf8')

    class Meta:
        db_table = 'taikhoan' 



class phieunhap(models.Model):
    imei_may = models.CharField(max_length=50, unique =True, primary_key=True)
    masanphamtuychon = models.ForeignKey(sanphamtuychon,  on_delete=models.SET(get_sentinel_user))
    ngaylap = models.DateTimeField(auto_now=True)
    usernhanvien = models.ForeignKey(taikhoan,  on_delete=models.SET(get_sentinel_user))
    gia = models.DecimalField(max_digits=12, decimal_places=2)
    LOCK_CHOICES = ((True, 'Lock'), (False, 'UnLock'))
    locked = models.BooleanField(choices=LOCK_CHOICES, default=False)
    ghichu = models.TextField()

    def __str__(self):
        return self.imei_may.encode('utf8')

    class Meta:
        db_table = 'phieunhap' 


class kho(models.Model):
    imei_may = models.OneToOneField(phieunhap, primary_key=True,  on_delete=models.SET(get_sentinel_user),)
    masanphamtuychon = models.ForeignKey(sanphamtuychon,  on_delete=models.SET(get_sentinel_user),)
    trangthaiban = models.BooleanField()
    
    def __str__(self):
        return self.imei_may.imei_may.encode('utf8')

    class Meta:
        db_table = 'kho' 

class hoadon(models.Model):
    user_khachhang = models.ForeignKey(taikhoan,  on_delete=models.SET(get_sentinel_user), related_name='khachhang')
    tonggia = models.DecimalField(max_digits=12, decimal_places=2, default= 0)
    usernhanvien = models.ForeignKey(taikhoan,  on_delete=models.SET(get_sentinel_user),  related_name='nhanvien')
    ngaylap = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = ((0, 'Cancel'), (1, 'Success'), (2, 'Processing'))
    trangthai = models.IntegerField(choices=STATUS_CHOICES, default=2)
    LOCK_CHOICES = ((True, 'Lock'), (False, 'UnLock'))
    locked = models.BooleanField(choices=LOCK_CHOICES, default=False)
    ghichu = models.TextField()

    def __str__(self):
        return self.user_khachhang.username.encode('utf8')

    class Meta:
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
        db_table = 'hoadonchitiet' 

class phieuxuat(models.Model):
    mahoadon = models.ForeignKey(hoadon,  on_delete=models.SET(get_sentinel_user),)
    manguoilap = models.ForeignKey(taikhoan,  on_delete=models.SET(get_sentinel_user),)
    ngaylap = models.DateTimeField(auto_now=True)
    imei_may = models.ForeignKey(kho,  on_delete=models.SET(get_sentinel_user))
    LOCK_CHOICES = ((True, 'Lock'), (False, 'UnLock'))
    locked = models.BooleanField(choices=LOCK_CHOICES, default=False)
    ghichu = models.TextField()
    
    def __str__(self):
        return self.imei_may.encode('utf8')
    
    class Meta:
        db_table = 'phieuxuat' 