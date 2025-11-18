# Chương trình giải bài toán Travelling Salesman Problem (TSP)

## Mô tả
Chương trình giải bài toán người du lịch (TSP) sử dụng 2 thuật toán tối ưu hóa:
1. **Simulated Annealing (SA)** - Thuật toán mô phỏng luyện kim
2. **Whale Optimization Algorithm (WOA)** - Thuật toán tối ưu hóa bầy cá voi

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

```bash
pip install -r requirements.txt
```

## Chạy chương trình

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
- **Simulated Annealing**: Phù hợp cho bài toán nhỏ và trung bình, tìm kiếm cẩn thận
- **WOA (Whale Optimization)**: Mô phỏng hành vi săn mồi của cá voi, cân bằng tốt giữa khám phá và khai thác

### 3. Tùy chỉnh tham số

#### Simulated Annealing:
- **Nhiệt độ ban đầu**: Càng cao cho phép khám phá rộng hơn (đề xuất: 10000)
- **Tốc độ làm nguội**: 0 < giá trị < 1, càng gần 1 càng chậm (đề xuất: 0.995)
- **Số vòng lặp**: Số lần lặp tối đa (đề xuất: 10000)

#### WOA (Whale Optimization Algorithm):
- **Số cá voi**: Số lượng cá voi trong quần thể (đề xuất: 30)
- **Số vòng lặp**: Số thế hệ tiến hóa (đề xuất: 1000)
- **Hằng số spiral (b)**: Hằng số xác định hình dạng xoắn ốc logarit (đề xuất: 1.0)
- **Giá trị a_max**: Giá trị tối đa của tham số a, giảm dần về 0 (đề xuất: 2.0)

### 4. Chạy và xem kết quả
- Nhấn "Chạy thuật toán" để bắt đầu
- Quan sát quá trình tối ưu hóa real-time trên đồ thị
- Có thể nhấn "Dừng" để dừng thuật toán bất kỳ lúc nào

## Giải thích thuật toán

### Simulated Annealing
Mô phỏng quá trình ủ kim loại:
- Bắt đầu với nhiệt độ cao, chấp nhận cả giải pháp xấu hơn
- Dần dần giảm nhiệt độ, chỉ chấp nhận giải pháp tốt hơn
- Giúp tránh bị mắc kẹt ở cực tiểu địa phương

### PSO (Particle Swarm Optimization)
Mô phỏng hành vi bầy đàn:
- Mỗi hạt là một giải pháp tiềm năng
- Hạt di chuyển dựa trên kinh nghiệm bản thân và kinh nghiệm tập thể
- Quần thể dần hội tụ về giải pháp tốt nhất

### WOA (Whale Optimization Algorithm)
Mô phỏng hành vi săn mồi của cá voi lưng gù:
- **Bao vây con mồi (Encircling Prey)**: Cá voi di chuyển về phía giải pháp tốt nhất
- **Tấn công bọt khí (Bubble-net attacking)**: Sử dụng chuyển động xoắn ốc
- **Tìm kiếm con mồi (Search for prey)**: Khám phá không gian tìm kiếm rộng hơn
- Cân bằng tốt giữa exploitation (khai thác) và exploration (khám phá)

## Kết quả hiển thị

1. **Bản đồ thành phố**: Hiển thị vị trí các thành phố và tuyến đường tốt nhất
2. **Đồ thị hội tụ**: Thể hiện quá trình cải thiện giải pháp theo thời gian
3. **Thông tin kết quả**: Khoảng cách tốt nhất, thời gian chạy, tuyến đường

## Lưu ý

### Về số thành phố
- **5-30 thành phố**: Lý tưởng để test và học tập, chạy nhanh
- **30-50 thành phố**: Cân bằng tốt giữa độ phức tạp và tốc độ
- **50-100 thành phố**: Thời gian chạy lâu hơn, tiêu tốn CPU và RAM nhiều hơn
- **100-200 thành phố**: Có thể làm máy chậm, giao diện lag khi cập nhật
- **> 200 thành phố**: Không khuyến nghị trừ phi có máy mạnh

### Về thuật toán
- WOA thường cân bằng tốt giữa tốc độ và chất lượng giải pháp
- SA có thể tìm được giải pháp tốt hơn nhưng mất nhiều thời gian hơn
- WOA sử dụng 3 cơ chế khác nhau (bao vây, xoắn ốc, tìm kiếm) để tối ưu hóa
- Có thể thử nghiệm với các tham số khác nhau để tìm cấu hình tốt nhất

## Xu ly loi (Error Handling)

Chuong trinh da duoc tich hop xu ly loi toan dien de dam bao trai nghiem nguoi dung tot hon va tranh cac loi runtime.

### Cac loai loi duoc xu ly

#### 1. Loi nhap lieu khong hop le (Input Validation)

**So thanh pho:**
- Gia tri hop le: 3 den 500
- Thong bao loi: Hien thi khi gia tri nam ngoai pham vi hoac khong phai so nguyen
- Canh bao dac biet:
  - 3-4 thanh pho: Bai toan qua don gian
  - >= 50 thanh pho: Anh huong den hieu suat
  - >= 100 thanh pho: Canh bao ve tac dong len may tinh

**Giai thich ve so thanh pho:**

1. **So thanh pho = 1 hoac 2**:
   - Khong duoc phep
   - So thanh pho = 1: Khong co tuyen duong
   - So thanh pho = 2: Chi co 1 cach duy nhat (A -> B -> A), khong can toi uu hoa
   - He thong se tu dong tu choi va giai thich ly do

2. **So thanh pho = 3**:
   - Duoc phep nhung he thong se canh bao
   - Chi co 1 cach sap xep duy nhat (A -> B -> C -> A)
   - Thuat toan se tim duoc ket qua ngay lap tuc ma khong can toi uu hoa
   - Canh bao: "Bai toan voi 3 thanh pho chi co 1 cach sap xep duy nhat. Khong can thuat toan toi uu hoa. Khuyen nghi su dung >= 5 thanh pho."

3. **So thanh pho = 4**:
   - Duoc phep nhung he thong se canh bao
   - Chi co 3 cach sap xep khac nhau (4!/2 = 12 nhung do tinh doi xung chi con 3)
   - Bai toan qua don gian, co the thu toan bo cac truong hop
   - Canh bao: "Bai toan voi 4 thanh pho chi co 3 cach sap xep. Co the thu toan bo. Khuyen nghi su dung >= 5 thanh pho."

4. **So thanh pho >= 5**:
   - Khuyen nghi su dung
   - So luong hoan vi tang nhanh: 5! = 120, 6! = 720, 7! = 5040...
   - Thuat toan toi uu hoa bat dau the hien hieu qua ro ret
   - Khong gian tim kiem du lon de cac thuat toan meta-heuristic (SA, WOA) hoat dong hieu qua

**Ket luan**: He thong cho phep >= 3 thanh pho de linh hoat, nhung se canh bao chi tiet cho cac truong hop dac biet (3-4 thanh pho) de nguoi dung hieu ro ban chat bai toan va han che cua thuat toan trong cac truong hop nay.

**Tham so Simulated Annealing (SA):**
- Nhiet do ban dau: 100 den 100,000
- Toc do lam nguoi: 0.8 den 0.9999 (phai la so thap phan)
- So vong lap: 100 den 100,000
- Thong bao loi: Hien thi cu the cho tung tham so

**Tham so WOA (Whale Optimization Algorithm):**
- So ca voi: 5 den 100
- So vong lap: 100 den 10,000
- Hang so spiral (b): 0.1 den 10.0
- Gia tri a_max: 0.5 den 5.0
- Thong bao loi: Hien thi cu the cho tung tham so

#### 2. Loi dinh dang du lieu
- Kiem tra: Cac gia tri phai la so nguyen hoac so thuc tuy theo yeu cau
- Xu ly: Thong bao ro rang loai du lieu mong doi va gia tri da nhap

#### 3. Loi khi chay thuat toan

**ValueError:**
- Tham so khong hop le
- Thong bao huong dan kiem tra lai tham so

**MemoryError:**
- Khong du bo nho
- Khuyen nghi giam so thanh pho hoac so vong lap

**General Exception:**
- Cac loi khong xac dinh khac
- Hien thi ten loi va thong diep chi tiet

#### 4. Xac nhan voi nguoi dung
- So thanh pho > 50: Yeu cau xac nhan vi co the mat nhieu thoi gian
- Chua tao bai toan: Nhac nho tao bai toan truoc khi chay thuat toan

### Cac tinh nang Error Handling

#### 1. Validation tu dong
Tat ca cac input duoc validate truoc khi xu ly. Vi du:
```python
# Kiem tra so thanh pho
if not self._validate_input(num_cities, "So thanh pho", min_val=5, max_val=100, data_type=int):
    return  # Dung xu ly va hien thi loi
```

#### 2. Thong bao loi ro rang
Cac thong bao loi bao gom:
- Ten tham so bi loi
- Gia tri da nhap
- Gia tri hop le mong doi
- Huong dan khac phuc

#### 3. Bao ve runtime
Tat ca cac class thuat toan co validation trong `__init__()`:
```python
# TSProblem
if num_cities < 3:
    raise ValueError(f"So thanh pho phai >= 3, nhan duoc: {num_cities}")

# SimulatedAnnealing
if not 0 < cooling_rate < 1:
    raise ValueError(f"Toc do lam nguoi phai trong khoang (0, 1), nhan duoc: {cooling_rate}")

# WOA
if num_whales < 2:
    raise ValueError(f"So ca voi phai >= 2, nhan duoc: {num_whales}")
```

#### 4. Xu ly loi trong thread
Thuat toan chay trong thread rieng voi try-catch toan dien de tranh crash ung dung.

### Cach su dung

**Khi nhap tham so sai:**
1. Nhap gia tri vao o input
2. Nhan "Tao bai toan moi" hoac "Chay thuat toan"
3. Neu gia tri khong hop le, mot dialog loi se hien thi
4. Doc thong bao loi va nhap lai gia tri dung

**Khi chay thuat toan:**
1. Dam bao da tao bai toan
2. Nhap cac tham so thuat toan
3. Nhan "Chay thuat toan"
4. Neu co loi, kiem tra thong bao va dieu chinh

### Vi du su dung

**Vi du 1: So thanh pho khong hop le**
```
Input: 2
Loi: "So thanh pho phai >= 5
Gia tri nhap: 2"
```

**Vi du 2: Toc do lam nguoi sai**
```
Input: 1.5
Loi: "Toc do lam nguoi phai <= 0.9999
Gia tri nhap: 1.5"
```

**Vi du 3: Input khong phai so**
```
Input: "abc"
Loi: "So thanh pho phai la so nguyen
Gia tri nhap: abc"
```

### Khuyen nghi

1. **Luon kiem tra thong bao loi**: Chung cung cap thong tin cu the ve van de
2. **Bat dau voi gia tri nho**: Khi test, dung so thanh pho nho (<30) de tranh cho lau
3. **Luu y bo nho**: Voi so thanh pho lon (>50), ung dung se hoi xac nhan
4. **Tham so mac dinh**: Cac gia tri mac dinh da duoc toi uu, chi thay doi khi can thiet

## Tac gia
Chuong trinh duoc phat trien cho do an mon AI

## License
MIT License
