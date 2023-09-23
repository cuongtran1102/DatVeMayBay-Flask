from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Text, Enum, DateTime, Time
from sqlalchemy.orm import relationship, backref
from datetime import datetime, timedelta
from flask_login import UserMixin
from app import db, app
from enum import Enum as UserEnum


class UserRole(UserEnum):
    ADMIN = 1
    EMPLOYEE = 2


class BaseMoDel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class ChiTietSBTG(BaseMoDel):
    __tablename__ = 'ChiTietSBTG'

    id_sanbay_tg = Column(ForeignKey('SanBay.id'), primary_key=True)
    id_chuyenbay = Column(ForeignKey('ChuyenBay.id'), primary_key=True)
    tg_dung = Column(Time, nullable=False)
    ghi_chu = Column(Text)

    def __str__(self):
        return str(self.id_chuyenbay)


chi_tiet_san_bay = db.Table('chi_tiet_san_bay',
                            Column('id_sanbay', Integer, ForeignKey('SanBay.id'), primary_key=True),
                            Column('id_chuyenbay', Integer, ForeignKey('ChuyenBay.id'), primary_key=True))


class SanBay(BaseMoDel):
    __tablename__ = 'SanBay'

    ten_San_bay = Column(String(50), nullable=False)
    dia_diem = Column(String(100), nullable=False)
    chuyen_bay = relationship('ChiTietSBTG', backref='san_bay_tg', lazy=True)

    def __str__(self):
        return self.ten_San_bay


class ChuyenBay(BaseMoDel):
    __tablename__ = 'ChuyenBay'

    ten_chuyen_bay = Column(String(100), nullable=False)
    tg_khoihanh = Column(DateTime, nullable=False)
    tg_bay = Column(Time, nullable=False)
    giave_hv1 = Column(Float, nullable=False)
    giave_hv2 = Column(Float, nullable=False)
    sanbay_tg = relationship("ChiTietSBTG", backref='chuyen_bay_tg', lazy=True)
    san_bay = relationship('SanBay', secondary='chi_tiet_san_bay', lazy='subquery', backref=backref('chi_tiet_cb', lazy=True))
    customer = relationship("Ve", backref='chuyen_bay')
    id_nv = Column(Integer, ForeignKey('User.id'), nullable=False)

    def __str__(self):
        return self.ten_chuyen_bay


class Ve(BaseMoDel):
    __tablename__ = 'Ve'

    id_chuyenbay = Column(ForeignKey('ChuyenBay.id'), primary_key=True)
    id_khach_hang = Column(ForeignKey('Customer.id'), primary_key=True)
    id_hangve = Column(Integer, ForeignKey('HangVe.id'), nullable=False)
    id_ghe = Column(Integer, ForeignKey('Ghe.id'), nullable=False)
    id_nv = Column(Integer, ForeignKey('User.id'))
    GiaVe = Column(Float, nullable=False)
    ngay_xuat_ve = Column(DateTime, default=datetime.now())

    def __str__(self):
        return str(self.id)


class Customer(BaseMoDel):
    __tablename__ = 'Customer'

    ho_ten = Column(String(50), nullable=False)
    so_cccd = Column(String(15), nullable=False)
    sdt = Column(String(12), nullable=False)
    chuyenbay = relationship("Ve", backref='customer')

    def __str__(self):
        return self.ho_ten


class HangVe(BaseMoDel):
    __tablename__ = 'HangVe'

    ten_hang_ve = Column(String(10), nullable=False)
    ve = relationship('Ve', backref='hang_ve', lazy=True)
    ghe = relationship('Ghe', backref='hang_ve', lazy=True)

    def __str__(self):
        return self.ten_hang_ve


# Ghe(ID-Ghe, SoGhe, ID-HangVe)
class Ghe(BaseMoDel):
    __tablename__ = 'Ghe'

    id_hangve = Column(Integer, ForeignKey('HangVe.id'), nullable=False)
    so_ghe = Column(Integer, nullable=False)
    ve = relationship('Ve', backref='ghe', lazy=True)

    def __str__(self):
        return str(self.id)


# User(User-ID, UserName, Password)
class User(BaseMoDel, UserMixin):
    __tablename__ = 'User'

    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)
    ho_ten = Column(String(50), nullable=False)
    so_cccd = Column(String(15), nullable=False)
    sdt = Column(String(12), nullable=False)
    chuyen_bay = relationship('ChuyenBay', backref='nhan_vien', lazy=True)
    ve = relationship('Ve', backref='nhan_vien', lazy=True)

    def __str__(self):
        return str(self.id)


# if __name__ == '__main__':
#     with app.app_context():
        # ten_San_bay = Column(String(50), nullable=False)
        # dia_diem = Column(String(100), nullable=False)
        # chuyen_bay = relationship('ChiTietSBTG', backref='san_bay_tg', lazy=True)
        # sb1 = SanBay(ten_San_bay='Tân Sơn Nhất', dia_diem='Thành phố Hồ Chí Minh')
        # sb2 = SanBay(ten_San_bay='Nội Bài', dia_diem='Thanh Hóa')
        # sb3 = SanBay(ten_San_bay='Jakatah', dia_diem='India')
        # sb4 = SanBay(ten_San_bay='Tokyo', dia_diem='Japan')
        # sb5 = SanBay(ten_San_bay='London', dia_diem='London')
        # sb6 = SanBay(ten_San_bay='Madrid', dia_diem='Madrid')
        # sb7 = SanBay(ten_San_bay='Madagatsca', dia_diem='Hawwai')
        # sb8 = SanBay(ten_San_bay='Land City', dia_diem='USA')
        # sb9 = SanBay(ten_San_bay='Bangkok', dia_diem='Thailand')
        # sb10 = SanBay(ten_San_bay='Rio', dia_diem='Brazil')
        # hv1 = HangVe(ten_hang_ve='Hạng vé 1')
        # hv2 = HangVe(ten_hang_ve='Hạng vé 2')
        # g1 = Ghe(id_hangve=1, so_ghe=1)
        # g2 = Ghe(id_hangve=1, so_ghe=2)
        # g3 = Ghe(id_hangve=1, so_ghe=3)
        # g4 = Ghe(id_hangve=1, so_ghe=4)
        # g5 = Ghe(id_hangve=1, so_ghe=5)
        # g6 = Ghe(id_hangve=1, so_ghe=6)
        # g7 = Ghe(id_hangve=1, so_ghe=7)
        # g8 = Ghe(id_hangve=1, so_ghe=8)
        # g9 = Ghe(id_hangve=1, so_ghe=9)
        # g10 = Ghe(id_hangve=1, so_ghe=10)
        # g11 = Ghe(id_hangve=2, so_ghe=11)
        # g12 = Ghe(id_hangve=2, so_ghe=12)
        # g13 = Ghe(id_hangve=2, so_ghe=13)
        # g14 = Ghe(id_hangve=2, so_ghe=14)
        # g15 = Ghe(id_hangve=2, so_ghe=15)
        # g16 = Ghe(id_hangve=2, so_ghe=16)
        # g17 = Ghe(id_hangve=2, so_ghe=17)
        # g18 = Ghe(id_hangve=2, so_ghe=18)
        # g19 = Ghe(id_hangve=2, so_ghe=19)
        # g20 = Ghe(id_hangve=2, so_ghe=20)
        #
        #
        # db.session.add(g1)
        # db.session.add(g2)
        # db.session.add(g3)
        # db.session.add(g4)
        # db.session.add(g5)
        # db.session.add(g6)
        # db.session.add(g7)
        # db.session.add(g8)
        # db.session.add(g9)
        # db.session.add(g10)
        # db.session.add(g11)
        # db.session.add(g12)
        # db.session.add(g13)
        # db.session.add(g14)
        # db.session.add(g15)
        # db.session.add(g16)
        # db.session.add(g17)
        # db.session.add(g18)
        # db.session.add(g19)
        # db.session.add(g20)
        #
        # db.session.commit()
