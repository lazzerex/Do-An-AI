# Quick Start Guide - Hướng dẫn nhanh

## Chạy nhanh (3 bước)

### 1. Cài đặt dependencies (chỉ cần làm 1 lần)
```bash
pip3 install -r requirements.txt
```

### 2. Chạy ứng dụng
```bash
./run.sh
```

hoặc

```bash
python3 gui_application.py
```

### 3. Sử dụng
- Chọn số thành phố (khuyến nghị: 20-30 để bắt đầu)
- Nhấn "Tạo bài toán mới"
- Chọn thuật toán (SA hoặc WOA)
- Nhấn "Chạy thuật toán"

## Lưu ý

- **macOS/Linux**: Dùng `python3` và `pip3`
- **Windows**: Dùng `python` và `pip`
- Bắt đầu với 20-30 thành phố để test nhanh

## Xử lý lỗi

### Lỗi "macOS 26 required" hoặc "Abort trap: 6"

Nếu gặp lỗi này khi chạy GUI, thử các cách sau:

1. **Cập nhật matplotlib:**
```bash
pip3 install --upgrade matplotlib
```

2. **Cài đặt lại dependencies:**
```bash
pip3 install --upgrade -r requirements.txt
```

3. **Chạy trực tiếp không qua script:**
```bash
python3 gui_application.py
```

4. **Nếu vẫn lỗi, thử cập nhật Python:**
   - Cài đặt Python mới hơn từ python.org hoặc dùng Homebrew:
   ```bash
   brew install python3
   ```

## Xem hướng dẫn chi tiết

Xem file `README.md` để biết thêm chi tiết về cách sử dụng.

