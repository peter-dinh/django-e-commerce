
-- sau khi nhap san pham, tu dong them san pham vao kho cung thay doi so luong ton cua san pham

DROP TRIGGER IF EXISTS AFTER_phieunhap_insert;
DELIMITER $$

 CREATE TRIGGER AFTER_phieunhap_insert

 AFTER INSERT ON phieunhap

 FOR EACH ROW

BEGIN

 INSERT INTO kho

SET

 imei_may_id = new.imei_may,

 masanphamtuychon_id = new.masanphamtuychon_id,

 trangthaiban = 0;

 update sanphamtuychon set
 soluong = soluong +1
 where id = new.masanphamtuychon_id;

END$$

 DELIMITER ;


 --  khi thay doi trang thai lock cua phieu nhap,  se xoa san pham trong kho va chap nhap so luong ton

 DROP TRIGGER IF EXISTS AFTER_phieunhap_update;
DELIMITER $$

 CREATE TRIGGER AFTER_phieunhap_update

 AFTER update ON phieunhap

 FOR EACH ROW

BEGIN

if old.imei_may != new.imei_may then
begin
	SIGNAL SQLSTATE '45000'
	SET MESSAGE_TEXT = 'Ban khong duoc phep chinh sua Imei_may!';
end;
end if;

if old.masanphamtuychon_id != new.masanphamtuychon_id then
begin
	update sanphamtuychon set
	soluong = soluong - 1
	where id = old.masanphamtuychon_id;

	update sanphamtuychon set
	soluong = soluong + 1
	where id = new.masanphamtuychon_id;

	update kho set masanphamtuychon_id = new.masanphamtuychon_id
	where imei_may_id = old.imei_may;
end;
end if;

 if new.locked = 1 then
 begin
	if exists (select * from kho where imei_may_id = old.imei_may and masanphamtuychon_id = old.masanphamtuychon_id) then
	begin
		 update sanphamtuychon set
		 soluong = soluong - 1
		 where id = old.masanphamtuychon_id;

		 delete from kho where imei_may_id = old.imei_may;
	 end;
	 end if;

 end;
 end if;

 --  khong cho phep doi trang thai lock
  if new.locked = 0 then
 begin
	 SIGNAL SQLSTATE '45000'
	SET MESSAGE_TEXT = 'Ban khong duoc phep lock lai phieu nhap nua!';
 end;
 end if;
END$$

 DELIMITER ;


 -- khong cho phep xoa phieu nhap

  DROP TRIGGER IF EXISTS Before_phieunhap_delete;
DELIMITER $$

 CREATE TRIGGER Before_phieunhap_delete

 before delete ON phieunhap

 FOR EACH ROW

BEGIN
	SIGNAL SQLSTATE '45000'
	SET MESSAGE_TEXT = 'Ban khong duoc phep xoa phieu nhap!';
END$$

 DELIMITER ;




 -- khi insert hoa don chi tiet, se thay doi so luong ton va tong gia

 DROP TRIGGER IF EXISTS AFTER_hoadonchitiet_insert;
DELIMITER $$

 CREATE TRIGGER AFTER_hoadonchitiet_insert

 AFTER insert ON hoadonchitiet

 FOR EACH ROW

BEGIN
	update sanphamtuychon set
	 soluong = soluong - new.soluong
	 where id = new.masanphamtuychon_id;
	 update hoadon set
	 tonggia = tonggia + (new.gia * new.soluong)
	 where id = new.mahoadon_id;

END$$

 DELIMITER ;

 -- khi locked hoa don chi tiet se thay doi so luong ton va tong tien

  DROP TRIGGER IF EXISTS AFTER_hoadonchitiet_update;
DELIMITER $$

 CREATE TRIGGER AFTER_hoadonchitiet_update

 AFTER update ON hoadonchitiet

 FOR EACH ROW

BEGIN
	if old.locked = 1 then
	begin
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Hoa don chi tiet khong the bi sua!';
	end;
	end if;

	if new.locked = 1 then
	begin
		if exists (select  * from hoadon where id = old.mahoadon_id and trangthai = 0) then
		begin
		update sanphamtuychon set
		 soluong = soluong + old.soluong
		 where id = new.masanphamtuychon_id;

		 delete from phieuxuat where phieuxuat.imei_may_id in (select kho.imei_may_id from kho  where kho.imei_may_id = phieuxuat.imei_may_id and phieuxuat.mahoadon_id = old.mahoadon_id and kho.masanphamtuychon_id = old.masanphamtuychon_id);
		end;	
		end if;
	end;
	end if;

END$$

 DELIMITER ;



  
 drop trigger if exists before_hoadonchitiet_delete;
 DELIMITER $$
 create trigger before_hoadonchitiet_delete
 before delete on hoadonchitiet
  for each row
 begin
	if exists (select  * from hoadon where id = old.mahoadon_id and trangthai!=2) then
	begin
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Ban khong duoc phep xoa hoa don chi tiet!';
	end;
	else
	begin
		update sanphamtuychon set
		 soluong = soluong + old.soluong
		 where id = old.masanphamtuychon_id;
		 update hoadon set
		 tonggia = tonggia - (old.gia * old.soluong)
		 where id = old.mahoadon_id;
	end;
	end if;
	
 end$$
 DELIMITER ;



 -- khi hoa don huy se thay doi trang thai hoadonchitiet

 drop trigger IF EXISTS after_hoadon_update_status;
 DELIMITER $$
 
 Create trigger after_hoadon_update_status
 after update on hoadon
 for each row
 begin
	if old.trangthai != 2 then
	begin
		 SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Ban khong duoc phep chinh sua trang thai cua hoa don!';
	end;
	end if;

	if new.trangthai = 1 then
	begin
		-- bo qua kiem tra loai san pham co dung yeu cau
		declare soluong_phieuxuat int(11);
		declare soluong_sanpham int(11);
		select count(*) into soluong_phieuxuat from phieuxuat where mahoadon_id = old.id;
		select sum(soluong) into soluong_sanpham from hoadon as a join hoadonchitiet as b on a.id = b.mahoadon_id where a.id = old.id;
		if soluong_phieuxuat = soluong_sanpham then 
		begin
			update kho set kho.trangthaiban = 1 where kho.imei_may_id in (select phieuxuat.imei_may_id from phieuxuat where phieuxuat.mahoadon_id = old.id);
			update hoadonchitiet set locked = 1 where mahoadon_id = old.id;
		end;
		else
			begin
			 SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Kiem tra lai phieu xuat!';
		end;
		end if;
	end;
	end if;

	if new.trangthai = 0 then
	begin
		update hoadonchitiet set locked = 1 where mahoadon_id = old.id;
		-- delete from phieuxuat where mahoadon_id = old.id;
		-- sau khi update hoa don chi tien trigger AFTER_hoadonchitiet_update_lock chay theo
	end;
	end if;
 end$$
 DELIMITER ;

 -- khong cho xoa hoa don
 drop trigger if exists before_hoadon_delete;
 DELIMITER $$
 create trigger before_hoadon_delete
 before delete on hoadon
  for each row
 begin
	SIGNAL SQLSTATE '45000'
	SET MESSAGE_TEXT = 'Ban khong duoc phep xoa hoa don!';
 end$$
 DELIMITER ;

