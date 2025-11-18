# Chương trình giải bài toán Travelling Salesman Problem (TSP)

## Mô tả
Chương trình giải bài toán người du lịch (TSP) sử dụng 2 thuật toán tối ưu hóa:
1. Simulated Annealing (SA) - Thuật toán mô phỏng luyện kim
2. Whale Optimization Algorithm (WOA) - Thuật toán tối ưu hóa bầy cá voi

## Cấu trúc dự án

```
Do-An-AI/
│
├── tsp_problem.py           # Module định nghĩa bài toán TSP
├── simulated_annealing.py   # Thuật toán Simulated Annealing
├── woa_algorithm.py         # Thuật toán WOA (Whale Optimization)
├── gui_application.py       # Giao diện GUI (tkinter)
├── requirements.txt         # Các thư viện cần thiết
└── README.md               # File hướng dẫn này
```

## Cài đặt

1. Cài đặt Python 3.7 trở lên
2. Cài đặt các thư viện cần thiết:

**Trên macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

**Trên Windows:**
```bash
pip install -r requirements.txt
```

## Chạy chương trình

**Cách 1: Sử dụng script helper (Khuyến nghị)**
```bash
./run.sh
```

**Cách 2: Chạy trực tiếp**

**Trên macOS/Linux:**
```bash
python3 gui_application.py
```

**Trên Windows:**
```bash
python gui_application.py
```

## Hướng dẫn sử dụng

### 1. Cấu hình bài toán
- Chọn số lượng thành phố (3-500)
- Nhấn "Tạo bài toán mới" để tạo một bộ dữ liệu ngẫu nhiên
- Lưu ý: 
  - Với 3-4 thành phố: Hệ thống sẽ cảnh báo vì bài toán quá đơn giản
  - Với >= 50 thành phố: Hệ thống sẽ thông báo về ảnh hưởng hiệu suất
  - Với >= 100 thành phố: Cảnh báo về tác động lên máy tính

### 2. Chọn thuật toán
- Simulated Annealing: Phù hợp cho bài toán nhỏ và trung bình, tìm kiếm cẩn thận
- WOA (Whale Optimization): Mô phỏng hành vi săn mồi của cá voi, cân bằng tốt giữa khám phá và khai thác

### 3. Tùy chỉnh tham số

#### Simulated Annealing:
- Nhiệt độ ban đầu: Càng cao cho phép khám phá rộng hơn (đề xuất: 10000)
- Tốc độ làm nguội: 0 < giá trị < 1, càng gần 1 càng chậm (đề xuất: 0.995)
- Số vòng lặp: Số lần lặp tối đa (đề xuất: 10000)

#### WOA (Whale Optimization Algorithm):
- Số cá voi: Số lượng cá voi trong quần thể (đề xuất: 30)
- Số vòng lặp: Số thế hệ tiến hóa (đề xuất: 1000)
- Hằng số spiral (b): Hằng số xác định hình dạng xoắn ốc logarit (đề xuất: 1.0)
- Giá trị a_max: Giá trị tối đa của tham số a, giảm dần về 0 (đề xuất: 2.0)

### 4. Chạy và xem kết quả
- Nhấn "Chạy thuật toán" để bắt đầu
- Quan sát quá trình tối ưu hóa theo thời gian thực trên đồ thị
- Có thể nhấn "Dừng" để dừng thuật toán bất kỳ lúc nào

## Giải thích thuật toán

### Simulated Annealing
Mô phỏng quá trình ủ kim loại:
- Bắt đầu với nhiệt độ cao, chấp nhận cả giải pháp xấu hơn
- Dần dần giảm nhiệt độ, chỉ chấp nhận giải pháp tốt hơn
- Giúp tránh bị mắc kẹt ở cực tiểu địa phương

### Whale Optimization Algorithm (WOA)
Mô phỏng hành vi săn mồi của cá voi lưng gù:
- Bao vây con mồi (Encircling Prey): Cá voi di chuyển về phía giải pháp tốt nhất
- Tấn công bọt khí (Bubble-net attacking): Sử dụng chuyển động xoắn ốc
- Tìm kiếm con mồi (Search for prey): Khám phá không gian tìm kiếm rộng hơn
- Cân bằng tốt giữa exploitation (khai thác) và exploration (khám phá)

## Kết quả hiển thị

1. Bản đồ thành phố: Hiển thị vị trí các thành phố và tuyến đường tốt nhất
2. Đồ thị hội tụ: Thể hiện quá trình cải thiện giải pháp theo thời gian
3. Thông tin kết quả: Khoảng cách tốt nhất, thời gian chạy, tuyến đường

## Lưu ý

### Về số thành phố
- 5-30 thành phố: Lý tưởng để test và học tập, chạy nhanh
- 30-50 thành phố: Cân bằng tốt giữa độ phức tạp và tốc độ
- 50-100 thành phố: Thời gian chạy lâu hơn, tiêu tốn CPU và RAM nhiều hơn
- 100-200 thành phố: Có thể làm máy chậm, giao diện lag khi cập nhật
- Trên 200 thành phố: Không khuyến nghị trừ phi có máy mạnh

### Về thuật toán
- WOA thường cân bằng tốt giữa tốc độ và chất lượng giải pháp
- SA có thể tìm được giải pháp tốt hơn nhưng mất nhiều thời gian hơn
- WOA sử dụng 3 cơ chế khác nhau (bao vây, xoắn ốc, tìm kiếm) để tối ưu hóa
- Có thể thử nghiệm với các tham số khác nhau để tìm cấu hình tốt nhất

## Xử lý lỗi

### Lỗi khi cài đặt/chạy

1. **Lỗi "command not found: pip" hoặc "command not found: python"**: 
   - Trên macOS/Linux, sử dụng `pip3` và `python3` thay vì `pip` và `python`
   
2. **Lỗi "ModuleNotFoundError"**: 
   - Chạy lại `pip3 install -r requirements.txt` (macOS/Linux) hoặc `pip install -r requirements.txt` (Windows)
   
3. **Lỗi tkinter**: 
   - Trên Linux có thể cần cài `python3-tk`: `sudo apt-get install python3-tk`
   - Trên macOS thường đã có sẵn
   
4. **Lỗi "macOS 26 required" hoặc "Abort trap: 6"**:
   - Cập nhật matplotlib: `pip3 install --upgrade matplotlib`
   - Cài đặt lại dependencies: `pip3 install --upgrade -r requirements.txt`
   - Nếu vẫn lỗi, thử cập nhật Python lên phiên bản mới hơn

5. **Lỗi import**: 
   - Đảm bảo đang ở đúng thư mục dự án
   - Kiểm tra các file `.py` có trong thư mục

### Lỗi khi sử dụng chương trình

Chương trình đã được tích hợp xử lý lỗi toàn diện để đảm bảo trải nghiệm người dùng tốt hơn và tránh các lỗi runtime.

### Các loại lỗi được xử lý

#### 1. Lỗi nhập liệu không hợp lệ

Số thành phố:
- Giá trị hợp lệ: 3 đến 500
- Thông báo lỗi: Hiển thị khi giá trị nằm ngoài phạm vi hoặc không phải số nguyên
- Cảnh báo đặc biệt:
  - 3-4 thành phố: Bài toán quá đơn giản
  - Từ 50 thành phố trở lên: Ảnh hưởng đến hiệu suất
  - Từ 100 thành phố trở lên: Cảnh báo về tác động lên máy tính

Giải thích về số thành phố:

1. Số thành phố = 1 hoặc 2:
   - Không được phép
   - Số thành phố = 1: Không có tuyến đường
   - Số thành phố = 2: Chỉ có 1 cách duy nhất (A -> B -> A), không cần tối ưu hóa
   - Hệ thống sẽ tự động từ chối và giải thích lý do

2. Số thành phố = 3:
   - Được phép nhưng hệ thống sẽ cảnh báo
   - Chỉ có 1 cách sắp xếp duy nhất (A -> B -> C -> A)
   - Thuật toán sẽ tìm được kết quả ngay lập tức mà không cần tối ưu hóa
   - Cảnh báo: "Bài toán với 3 thành phố chỉ có 1 cách sắp xếp duy nhất. Không cần thuật toán tối ưu hóa. Khuyến nghị sử dụng >= 5 thành phố."

3. Số thành phố = 4:
   - Được phép nhưng hệ thống sẽ cảnh báo
   - Chỉ có 3 cách sắp xếp khác nhau (4!/2 = 12 nhưng do tính đối xứng chỉ còn 3)
   - Bài toán quá đơn giản, có thể thử toàn bộ các trường hợp
   - Cảnh báo: "Bài toán với 4 thành phố chỉ có 3 cách sắp xếp. Có thể thử toàn bộ. Khuyến nghị sử dụng >= 5 thành phố."

4. Số thành phố >= 5:
   - Khuyến nghị sử dụng
   - Số lượng hoán vị tăng nhanh: 5! = 120, 6! = 720, 7! = 5040...
   - Thuật toán tối ưu hóa bắt đầu thể hiện hiệu quả rõ rệt
   - Không gian tìm kiếm đủ lớn để các thuật toán meta-heuristic (SA, WOA) hoạt động hiệu quả

Kết luận: Hệ thống cho phép >= 3 thành phố để linh hoạt, nhưng sẽ cảnh báo chi tiết cho các trường hợp đặc biệt (3-4 thành phố) để người dùng hiểu rõ bản chất bài toán và hạn chế của thuật toán trong các trường hợp này.

Tham số Simulated Annealing (SA):
- Nhiệt độ ban đầu: 100 đến 100,000
- Tốc độ làm nguội: 0.8 đến 0.9999 (phải là số thập phân)
- Số vòng lặp: 100 đến 100,000
- Thông báo lỗi: Hiển thị cụ thể cho từng tham số

Tham số WOA (Whale Optimization Algorithm):
- Số cá voi: 5 đến 100
- Số vòng lặp: 100 đến 10,000
- Hằng số spiral (b): 0.1 đến 10.0
- Giá trị a_max: 0.5 đến 5.0
- Thông báo lỗi: Hiển thị cụ thể cho từng tham số

#### 2. Lỗi định dạng dữ liệu
- Kiểm tra: Các giá trị phải là số nguyên hoặc số thực tùy theo yêu cầu
- Xử lý: Thông báo rõ ràng loại dữ liệu mong đợi và giá trị đã nhập

#### 3. Lỗi khi chạy thuật toán

ValueError:
- Tham số không hợp lệ
- Thông báo hướng dẫn kiểm tra lại tham số

MemoryError:
- Không đủ bộ nhớ
- Khuyến nghị giảm số thành phố hoặc số vòng lặp

General Exception:
- Các lỗi không xác định khác
- Hiển thị tên lỗi và thông điệp chi tiết

#### 4. Xác nhận với người dùng
- Số thành phố > 50: Yêu cầu xác nhận vì có thể mất nhiều thời gian
- Chưa tạo bài toán: Nhắc nhở tạo bài toán trước khi chạy thuật toán

### Các tính năng xử lý lỗi

#### 1. Validation tự động
Tất cả các input được validate trước khi xử lý. Ví dụ:
```python
# Kiểm tra số thành phố
if not self._validate_input(num_cities, "Số thành phố", min_val=5, max_val=100, data_type=int):
    return  # Dừng xử lý và hiển thị lỗi
```

#### 2. Thông báo lỗi rõ ràng
Các thông báo lỗi bao gồm:
- Tên tham số bị lỗi
- Giá trị đã nhập
- Giá trị hợp lệ mong đợi
- Hướng dẫn khắc phục

#### 3. Bảo vệ runtime
Tất cả các class thuật toán có validation trong phương thức khởi tạo:
```python
# TSProblem
if num_cities < 3:
    raise ValueError(f"Số thành phố phải >= 3, nhận được: {num_cities}")

# SimulatedAnnealing
if not 0 < cooling_rate < 1:
    raise ValueError(f"Tốc độ làm nguội phải trong khoảng (0, 1), nhận được: {cooling_rate}")

# WOA
if num_whales < 2:
    raise ValueError(f"Số cá voi phải >= 2, nhận được: {num_whales}")
```

#### 4. Xử lý lỗi trong thread
Thuật toán chạy trong thread riêng với try-catch toàn diện để tránh crash ứng dụng.

### Cách sử dụng

Khi nhập tham số sai:
1. Nhập giá trị vào ô input
2. Nhấn "Tạo bài toán mới" hoặc "Chạy thuật toán"
3. Nếu giá trị không hợp lệ, một dialog lỗi sẽ hiển thị
4. Đọc thông báo lỗi và nhập lại giá trị đúng

Khi chạy thuật toán:
1. Đảm bảo đã tạo bài toán
2. Nhập các tham số thuật toán
3. Nhấn "Chạy thuật toán"
4. Nếu có lỗi, kiểm tra thông báo và điều chỉnh

### Ví dụ sử dụng

Ví dụ 1: Số thành phố không hợp lệ
```
Input: 2
Lỗi: "Số thành phố phải >= 5
Giá trị nhập: 2"
```

Ví dụ 2: Tốc độ làm nguội sai
```
Input: 1.5
Lỗi: "Tốc độ làm nguội phải <= 0.9999
Giá trị nhập: 1.5"
```

Ví dụ 3: Input không phải số
```
Input: "abc"
Lỗi: "Số thành phố phải là số nguyên
Giá trị nhập: abc"
```

### Khuyến nghị

1. Luôn kiểm tra thông báo lỗi: Chúng cung cấp thông tin cụ thể về vấn đề
2. Bắt đầu với giá trị nhỏ: Khi test, dùng số thành phố nhỏ (<30) để tránh chờ lâu
3. Lưu ý bộ nhớ: Với số thành phố lớn (>50), ứng dụng sẽ hỏi xác nhận
4. Tham số mặc định: Các giá trị mặc định đã được tối ưu, chỉ thay đổi khi cần thiết

## Tác giả
Chương trình được phát triển cho đồ án môn AI

## Giấy phép
MIT License
