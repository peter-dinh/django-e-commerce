
-- Danh sach dong san pham
DELIMITER $$ 
drop procedure if exists WSP_DanhSachDongSanPham $$
create procedure WSP_DanhSachDongSanPham()
begin
	select * from dongsanpham;
end; $$
DELIMITER ;

--   Login 

DELIMITER $$ 
drop procedure if exists WSP_Login $$
create procedure WSP_Login(
	in v_username varchar(100),
	in v_password varchar(100)
)
begin
	select count(*) from taikhoan where username = v_username and password = v_password and loaitaikhoan = 0;
end; $$
DELIMITER ;




DELIMITER $$ 
drop procedure if exists WSP_IphoneCatalog $$
create procedure WSP_IphoneCatalog(
	in v_ma_dongsp int(11)
)
begin
	select a.id, a.soluong, a.giasanpham, a.anhdaidien, b.tensp, c.mausac, c.bonhotrong from (sanphamtuychon as a join sanpham as b on a.ma_sp_id = b.id) join tuychon as c on a.ma_tuy_chon_id = c.id where ma_sp_id in (select id from sanpham where dongsp_catalog_id = v_ma_dongsp);
end; $$
DELIMITER ;



DELIMITER $$ 
drop procedure if exists WSP_Iphone5 $$
create procedure WSP_Iphone5()
begin
	select a.id, a.soluong, a.giasanpham, a.anhdaidien, b.tensp, c.mausac, c.bonhotrong from (sanphamtuychon as a join sanpham as b on a.ma_sp_id = b.id) join tuychon as c on a.ma_tuy_chon_id = c.id where ma_sp_id in (select id from sanpham where dongsp_catalog_id = 1) ORDER BY RAND() LIMIT 4;
end; $$
DELIMITER ;


DELIMITER $$ 
drop procedure if exists WSP_Iphone6 $$
create procedure WSP_Iphone6()
begin
	select a.id, a.soluong, a.giasanpham, a.anhdaidien, b.tensp, c.mausac, c.bonhotrong from (sanphamtuychon as a join sanpham as b on a.ma_sp_id = b.id) join tuychon as c on a.ma_tuy_chon_id = c.id where ma_sp_id in (select id from sanpham where dongsp_catalog_id = 2) ORDER BY RAND() LIMIT 1;
end; $$
DELIMITER ;


DELIMITER $$ 
drop procedure if exists WSP_Iphone7 $$
create procedure WSP_Iphone7()
begin
	select a.id, a.soluong, a.giasanpham, a.anhdaidien, b.tensp, c.mausac, c.bonhotrong from (sanphamtuychon as a join sanpham as b on a.ma_sp_id = b.id) join tuychon as c on a.ma_tuy_chon_id = c.id where ma_sp_id in (select id from sanpham where dongsp_catalog_id = 3) ORDER BY RAND() LIMIT 4;
end; $$
DELIMITER ;



DELIMITER $$ 
drop procedure if exists WSP_Iphone8 $$
create procedure WSP_Iphone8()
begin
	select a.id, a.soluong, a.giasanpham, a.anhdaidien, b.tensp, c.mausac, c.bonhotrong from (sanphamtuychon as a join sanpham as b on a.ma_sp_id = b.id) join tuychon as c on a.ma_tuy_chon_id = c.id where ma_sp_id in (select id from sanpham where dongsp_catalog_id = 4)  ORDER BY RAND() LIMIT 4;
end; $$
DELIMITER ;


DELIMITER $$ 
drop procedure if exists WSP_SanPhamBan $$
create procedure WSP_SanPhamBan()
begin
	select a.id, a.soluong, a.giasanpham, a.anhdaidien, b.tensp, c.mausac, c.bonhotrong from (sanphamtuychon as a join sanpham as b on a.ma_sp_id = b.id) join tuychon as c on a.ma_tuy_chon_id = c.id where a.soluong > 0 ORDER BY RAND() LIMIT 6;
end; $$
DELIMITER ;


DELIMITER $$ 
drop procedure if exists WSP_SanPhamMoi $$
create procedure WSP_SanPhamMoi()
begin
	select a.id, a.soluong, a.giasanpham, a.anhdaidien, b.tensp, c.mausac, c.bonhotrong from (sanphamtuychon as a join sanpham as b on a.ma_sp_id = b.id) join tuychon as c on a.ma_tuy_chon_id = c.id ORDER BY id desc LIMIT 8;
end; $$
DELIMITER ;

DELIMITER $$ 
drop procedure if exists WSP_ThongTinSanPham $$
create procedure WSP_ThongTinSanPham(
	in v_id_sanphamtuychon int(11)
)
begin
	select a.id, a.soluong, a.giasanpham, a.anhdaidien, b.tensp, c.mausac, c.bonhotrong 
	from ((sanphamtuychon as a join sanpham as b on a.ma_sp_id = b.id) join tuychon as c on a.ma_tuy_chon_id = c.id)
	where a.id = v_id_sanphamtuychon;
end; $$
DELIMITER ;


DELIMITER $$ 
drop procedure if exists WSP_TimKiem $$
create procedure WSP_TimKiem(
	in keyword varchar(200)
)
begin
	select a.id, a.soluong, a.giasanpham, a.anhdaidien, b.tensp, c.mausac, c.bonhotrong 
	from ((sanphamtuychon as a join sanpham as b on a.ma_sp_id = b.id) join tuychon as c on a.ma_tuy_chon_id = c.id)
	where a.giasanpham like CONCAT('%',keyword,'%') or b.tensp like CONCAT('%',keyword,'%') or c.mausac like CONCAT('%',keyword,'%') or c.bonhotrong like CONCAT('%',keyword,'%');
end; $$
DELIMITER ;

DELIMITER $$ 
drop procedure if exists WSP_SanPhamCungLoai $$
create procedure WSP_SanPhamCungLoai(
	in id_catalog int(11)
)
begin
	select a.id, a.soluong, a.giasanpham, a.anhdaidien, b.tensp, c.mausac, c.bonhotrong 
	from ((sanphamtuychon as a join sanpham as b on a.ma_sp_id = b.id) join tuychon as c on a.ma_tuy_chon_id = c.id)
	where b.dongsp_catalog_id=id_catalog ORDER BY RAND() LIMIT 6;
end; $$
DELIMITER ;