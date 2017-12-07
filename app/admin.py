from django.contrib import admin
from django.conf import settings

# Register your models here.

from .models import taikhoan, hoadon, hoadonchitiet, phieunhap, phieuxuat
from .models import sanpham, sanphamtuychon, tuychon, ketnoi, kho, thongsocamera



class taikhoanAdmin(admin.ModelAdmin):
    list_display  = ('username', 'hovaten', 'gioitinh', 'sodienthoai', 'email', 'loaitaikhoan')
    search_fields = ('username', 'hovaten', 'gioitinh', 'sodienthoai', 'loaitaikhoan', 'email', 'loaitaikhoan' )

class sanphamtuychonAdmin(admin.ModelAdmin):
    fields = ['ma_sp', 'ma_tuy_chon', 'giasanpham' , 'image_tag', 'anhdaidien']
    readonly_fields = ['image_tag']
    list_display = ('ma_sp', 'ma_tuy_chon', 'giasanpham', 'soluong')
    search_fields = ('ma_sp__tensp', 'giasanpham', 'ma_tuy_chon__mausac', 'ma_tuy_chon__bonhotrong',)


class ketnoiAdmin(admin.ModelAdmin):
    list_display = ('wlan', 'bluetooth', 'gps')
    fields = ['wlan', 'bluetooth', 'gps']
    search_fields = ('wlan', 'bluetooth', 'gps',)
    
    
class thongsocameraAdmin(admin.ModelAdmin):
    list_display = ('diemmanh', 'thongsocoban', 'dacdiem')
    fields = ['diemmanh', 'thongsocoban', 'dacdiem']
    search_fields = ('diemmanh', 'thongsocoban', 'dacdiem',)

class tuychonAdmin(admin.ModelAdmin):
    list_display = ('mausac', 'bonhotrong')
    fields = ['mausac', 'bonhotrong']
    search_fields = ('mausac', 'bonhotrong')

class sanphamAdmin(admin.ModelAdmin):
    list_display = ('tensp', 'kichthuocman', 'thoidiemramat', 'hedieuhanh', 'dongsp_catalog')
    search_fields = ('tensp', 'kichthuocman', 'thongsoman', 'pin', 'kichthuoc', 
        'khoiluong', 'thoidiemramat', 'chipset', 'tscpu', 'bonhoram',
        'hedieuhanh', 'baomatvantay', 'chongnuoc', 'dongsp_catalog',
        'ketnoi__wlan', 'ketnoi__bluetooth', 'ketnoi__gps',
        'macameratruoc__diemmanh', 'macameratruoc__thongsocoban', 'macameratruoc__dacdiem',
        'macamerasau__diemmanh', 'macamerasau__thongsocoban', 'macamerasau__dacdiem',
    )
    raw_id_fields = ('macameratruoc', 'macamerasau', 'ketnoi')
    empty_value_display = '-empty-'

class Themhoadonchitiet(admin.StackedInline):
    model = hoadonchitiet
    extra = 3

class  hoadonAdmin(admin.ModelAdmin):
    list_display = ('user_khachhang', 'usernhanvien', 'tonggia', 'ngaylap', 'trangthai',)
    fieldsets = [
        ('Hoa don', {'fields': ['user_khachhang', 'usernhanvien', 'tonggia', 'ngaylap', 'trangthai', 'locked', 'ghichu']}),
    ]
    search_fields = ('user_khachhang__username', 'user_khachhang__hovaten', 'usernhanvien__username', 'trangthai',)
    readonly_fields = ['tonggia', 'ngaylap']
    inlines = [Themhoadonchitiet]


class hoadonchitietAdmin(admin.ModelAdmin):
    list_display = ('mahoadon', 'masanphamtuychon', 'gia', 'soluong', 'locked',)
    search_fields = ('mahoadon__user_khachhang__username', 'masanphamtuychon__ma_sp__tensp', 'gia', 'soluong',)
   
class phieunhapAdmin(admin.ModelAdmin):
    list_display = ('masanphamtuychon',  'imei_may', 'gia', 'usernhanvien','locked')
    search_fields = ('masanphamtuychon__ma_sp__tensp', 'imei_may', 'gia', 'usernhanvien__username')
    

class khoAdmin(admin.ModelAdmin):
    list_display = ('imei_may', 'masanphamtuychon', 'trangthaiban',)
    search_fields = ('masanphamtuychon__ma_sp__tensp', 'imei_may__imei_may', 'trangthaiban')
    raw_id_fields = ('imei_may', 'masanphamtuychon')

    def delete_view(request, object=True):
        return redirect()


class phieuxuatAdmin(admin.ModelAdmin):
    list_display = ('mahoadon', 'imei_may', 'ngaylap', 'manguoilap',)
    search_fields = ('mahoadon__user_khachhang__username', 'imei_may__imei_may__imei_may', 'ngaylap', 'manguoilap__username',)

admin.site.register(sanpham, sanphamAdmin)
admin.site.register(tuychon, tuychonAdmin)
admin.site.register(sanphamtuychon, sanphamtuychonAdmin)
admin.site.register(ketnoi, ketnoiAdmin)
admin.site.register(thongsocamera, thongsocameraAdmin)
admin.site.register(taikhoan, taikhoanAdmin)
admin.site.register(hoadon, hoadonAdmin)
admin.site.register(hoadonchitiet, hoadonchitietAdmin)
admin.site.register(phieuxuat, phieuxuatAdmin)
admin.site.register(kho, khoAdmin)
admin.site.register(phieunhap, phieunhapAdmin)

