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
- Chọn số lượng thành phố (5-100)
- Nhấn "Tạo bài toán mới" để tạo một bộ dữ liệu ngẫu nhiên

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
- Với số lượng thành phố lớn (>50), thời gian chạy sẽ lâu hơn
- WOA thường cân bằng tốt giữa tốc độ và chất lượng giải pháp
- SA có thể tìm được giải pháp tốt hơn nhưng mất nhiều thời gian hơn
- WOA sử dụng 3 cơ chế khác nhau (bao vây, xoắn ốc, tìm kiếm) để tối ưu hóa
- Có thể thử nghiệm với các tham số khác nhau để tìm cấu hình tốt nhất

## Tác giả
Chương trình được phát triển cho đồ án môn AI

## License
MIT License
