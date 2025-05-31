# Hệ Thống Quản Lý Nuôi Cấy Mô

Ứng dụng web được phát triển bằng Flask để quản lý quy trình nuôi cấy mô thực vật.

## Tính năng

- Quản lý mẫu nuôi cấy
- Theo dõi thông số môi trường (nhiệt độ, độ ẩm, ánh sáng)
- Quản lý phòng nuôi cấy
- Upload và quản lý hình ảnh
- Xuất báo cáo và biểu đồ thống kê
- Backup/Restore dữ liệu
- API cho mobile app
- Xác thực và phân quyền người dùng

## Yêu cầu

- Python 3.8+
- Flask
- SQLAlchemy
- Các thư viện khác được liệt kê trong requirements.txt

## Cài đặt

1. Clone repository:
```bash
git clone https://github.com/your-username/tissue-culture-app.git
cd tissue-culture-app
```

2. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Cài đặt các dependencies:
```bash
pip install -r requirements.txt
```

4. Tạo file .env với các biến môi trường:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///app.db
```

5. Khởi tạo database:
```bash
flask db upgrade
```

6. Chạy ứng dụng:
```bash
flask run
```

## Cấu trúc thư mục

```
tissue-culture-app/
├── app/
│   ├── api/
│   │   └── v1/
│   ├── models/
│   ├── routes/
│   ├── templates/
│   ├── static/
│   └── utils/
├── migrations/
├── tests/
├── venv/
├── .env
├── .gitignore
├── config.py
├── requirements.txt
└── run.py
```

## API Documentation

API endpoints được bảo vệ bằng JWT token. Để sử dụng API:

1. Đăng nhập để lấy token:
```
POST /api/v1/auth/login
{
    "email": "user@example.com",
    "password": "password"
}
```

2. Sử dụng token trong header:
```
Authorization: Bearer <token>
```

Chi tiết các API endpoints có thể xem tại `/api/v1/docs`

## Backup & Restore

- Tính năng backup tự động lưu trữ cả database và media files
- File backup được nén dạng ZIP
- Có thể khôi phục (restore) từ file backup bất kỳ
- Chỉ admin mới có quyền truy cập tính năng này

## Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Liên hệ

Your Name - email@example.com

Project Link: [https://github.com/your-username/tissue-culture-app](https://github.com/your-username/tissue-culture-app) 