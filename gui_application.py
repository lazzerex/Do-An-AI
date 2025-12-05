"""
Module giao diện GUI cho chương trình giải TSP
"""
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time

from tsp_problem import TSProblem
from simulated_annealing import SimulatedAnnealing
from woa_algorithm import WOA


class TSPApplication:
    """Lớp ứng dụng GUI cho bài toán TSP"""
    
    def __init__(self, root):
        """
        Khởi tạo ứng dụng
        
        Args:
            root: Cửa sổ chính Tkinter
        """
        self.root = root
        self.root.title("Giải bài toán Travelling Salesman Problem")
        self.root.geometry("1400x800")
        
        # Biến lưu trữ
        self.tsp_problem = None
        self.current_algorithm = None
        self.is_running = False
        self.best_route = None
        self.best_distance = None
        
        # Tạo giao diện
        self._create_widgets()
        
        # Khởi tạo bài toán mặc định
        self._initialize_problem()
    
    def _create_widgets(self):
        """Tạo các widget cho giao diện"""
        # Panel bên trái: Điều khiển
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5)
        
        # Phần cấu hình bài toán
        problem_frame = ttk.LabelFrame(control_frame, text="Cấu hình bài toán", padding="10")
        problem_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(problem_frame, text="Số thành phố:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.num_cities_var = tk.IntVar(value=20)
        ttk.Spinbox(problem_frame, from_=3, to=500, textvariable=self.num_cities_var, 
                    width=15).grid(row=0, column=1, pady=2)
        
        ttk.Button(problem_frame, text="Tạo bài toán mới", 
                   command=self._initialize_problem).grid(row=1, column=0, columnspan=2, pady=5)
        
        # Phần chọn thuật toán
        algo_frame = ttk.LabelFrame(control_frame, text="Chọn thuật toán", padding="10")
        algo_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.algorithm_var = tk.StringVar(value="SA")
        ttk.Radiobutton(algo_frame, text="Simulated Annealing", 
                        variable=self.algorithm_var, value="SA").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(algo_frame, text="WOA (Whale Optimization)", 
                        variable=self.algorithm_var, value="WOA").grid(row=1, column=0, sticky=tk.W)
        
        # Phần tham số Simulated Annealing
        sa_frame = ttk.LabelFrame(control_frame, text="Tham số Simulated Annealing", padding="10")
        sa_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(sa_frame, text="Nhiệt độ ban đầu:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.sa_temp_var = tk.DoubleVar(value=10000)
        ttk.Entry(sa_frame, textvariable=self.sa_temp_var, width=15).grid(row=0, column=1, pady=2)
        
        ttk.Label(sa_frame, text="Tốc độ làm nguội:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.sa_cooling_var = tk.DoubleVar(value=0.995)
        ttk.Entry(sa_frame, textvariable=self.sa_cooling_var, width=15).grid(row=1, column=1, pady=2)
        
        ttk.Label(sa_frame, text="Số vòng lặp:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.sa_iterations_var = tk.IntVar(value=10000)
        ttk.Entry(sa_frame, textvariable=self.sa_iterations_var, width=15).grid(row=2, column=1, pady=2)
        
        # Phần tham số WOA (Whale Optimization Algorithm)
        woa_frame = ttk.LabelFrame(control_frame, text="Tham số WOA", padding="10")
        woa_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(woa_frame, text="Số cá voi:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.woa_whales_var = tk.IntVar(value=30)
        ttk.Entry(woa_frame, textvariable=self.woa_whales_var, width=15).grid(row=0, column=1, pady=2)
        
        ttk.Label(woa_frame, text="Số vòng lặp:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.woa_iterations_var = tk.IntVar(value=1000)
        ttk.Entry(woa_frame, textvariable=self.woa_iterations_var, width=15).grid(row=1, column=1, pady=2)
        
        ttk.Label(woa_frame, text="Hằng số spiral (b):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.woa_b_var = tk.DoubleVar(value=1.0)
        ttk.Entry(woa_frame, textvariable=self.woa_b_var, width=15).grid(row=2, column=1, pady=2)
        
        ttk.Label(woa_frame, text="Giá trị a_max:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.woa_a_var = tk.DoubleVar(value=2.0)
        ttk.Entry(woa_frame, textvariable=self.woa_a_var, width=15).grid(row=3, column=1, pady=2)
        
        # Nút điều khiển
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.run_button = ttk.Button(button_frame, text="Chạy thuật toán", 
                                      command=self._run_algorithm)
        self.run_button.grid(row=0, column=0, pady=5, padx=2)
        
        self.stop_button = ttk.Button(button_frame, text="Dừng", 
                                       command=self._stop_algorithm, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, pady=5, padx=2)
        
        self.export_button = ttk.Button(button_frame, text="Xuất kết quả", 
                                        command=self._export_results, state=tk.DISABLED)
        self.export_button.grid(row=1, column=0, columnspan=2, pady=5, padx=2, sticky=(tk.W, tk.E))
        
        # Thanh tiến trình
        self.progress_var = tk.StringVar(value="Chưa chạy")
        ttk.Label(control_frame, textvariable=self.progress_var, 
                  font=('Arial', 9)).grid(row=5, column=0, pady=5)
        
        # Kết quả
        result_frame = ttk.LabelFrame(control_frame, text="Kết quả", padding="10")
        result_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.result_text = tk.Text(result_frame, height=8, width=35, font=('Courier', 9))
        self.result_text.grid(row=0, column=0)
        
        # Panel bên phải: Hiển thị đồ thị
        viz_frame = ttk.Frame(self.root, padding="10")
        viz_frame.grid(row=0, column=1, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5)
        
        # Tạo figure cho matplotlib
        self.fig = Figure(figsize=(12, 8))
        
        # Subplot 1: Bản đồ thành phố và tuyến đường
        self.ax_map = self.fig.add_subplot(2, 1, 1)
        self.ax_map.set_title("Bản đồ thành phố và tuyến đường tốt nhất")
        self.ax_map.set_xlabel("X")
        self.ax_map.set_ylabel("Y")
        
        # Subplot 2: Đồ thị hội tụ
        self.ax_convergence = self.fig.add_subplot(2, 1, 2)
        self.ax_convergence.set_title("Đồ thị hội tụ")
        self.ax_convergence.set_xlabel("Iteration")
        self.ax_convergence.set_ylabel("Distance")
        
        self.fig.tight_layout()
        
        # Embed matplotlib vào tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Cấu hình grid weights
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def _validate_input(self, value, param_name, min_val=None, max_val=None, data_type=int):
        """
        Validate input parameters
        
        Args:
            value: Giá trị cần validate
            param_name: Tên tham số (hiển thị trong thông báo lỗi)
            min_val: Giá trị tối thiểu
            max_val: Giá trị tối đa
            data_type: Kiểu dữ liệu (int hoặc float)
            
        Returns:
            True nếu hợp lệ, False nếu không
        """
        try:
            # Kiểm tra kiểu dữ liệu
            if data_type == int:
                val = int(value)
            else:
                val = float(value)
            
            # Kiểm tra giá trị min
            if min_val is not None and val < min_val:
                messagebox.showerror(
                    "Lỗi giá trị",
                    f"Lỗi: {param_name} phải >= {min_val}\n\nBạn đã nhập: {val}"
                )
                return False
            
            # Kiểm tra giá trị max
            if max_val is not None and val > max_val:
                messagebox.showerror(
                    "Lỗi giá trị",
                    f"Lỗi: {param_name} phải <= {max_val}\n\nBạn đã nhập: {val}"
                )
                return False
            
            return True
            
        except (ValueError, TypeError, tk.TclError):
            # Xử lý lỗi khi nhập giá trị không hợp lệ
            messagebox.showerror(
                "Lỗi định dạng",
                f"Lỗi: {param_name} phải là {'số nguyên' if data_type == int else 'số thực'}\n\n"
                f"Bạn đã nhập giá trị không hợp lệ"
            )
            return False
    
    def _initialize_problem(self):
        """Khởi tạo bài toán TSP mới"""
        try:
            # Lấy giá trị số thành phố và bắt lỗi ngay
            try:
                num_cities = self.num_cities_var.get()
            except (ValueError, tk.TclError):
                messagebox.showerror(
                    "Lỗi định dạng",
                    "Lỗi: Số thành phố phải là số nguyên\n\nBạn đã nhập giá trị không hợp lệ"
                )
                return
            
            # Validate số thành phố
            if not self._validate_input(num_cities, "Số thành phố", min_val=3, max_val=500, data_type=int):
                return
            
            # Cảnh báo cho các trường hợp đặc biệt
            warning_message = None
            if num_cities == 3:
                warning_message = (
                    "Cảnh báo: Bài toán với 3 thành phố\n\n"
                    "Với 3 thành phố, chỉ có 1 cách sắp xếp duy nhất (A→B→C→A).\n"
                    "Thuật toán sẽ tìm được kết quả ngay lập tức mà không cần tối ưu hóa.\n\n"
                    "Khuyến nghị: Sử dụng >= 5 thành phố để thấy rõ hiệu quả của thuật toán.\n\n"
                    "Bạn có muốn tiếp tục?"
                )
            elif num_cities == 4:
                warning_message = (
                    "Cảnh báo: Bài toán với 4 thành phố\n\n"
                    "Với 4 thành phố, chỉ có 3 cách sắp xếp khác nhau (do tính đối xứng).\n"
                    "Bài toán này quá đơn giản, có thể thử toàn bộ các trường hợp.\n\n"
                    "Khuyến nghị: Sử dụng >= 5 thành phố để thuật toán thể hiện hiệu quả.\n\n"
                    "Bạn có muốn tiếp tục?"
                )
            elif num_cities >= 100:
                warning_message = (
                    f"Cảnh báo: Bài toán với {num_cities} thành phố\n\n"
                    f"Số thành phố lớn sẽ ảnh hưởng đến hiệu suất:\n"
                    f"- Thời gian tính toán sẽ tăng đáng kể\n"
                    f"- Tiêu tốn nhiều tài nguyên CPU và RAM\n"
                    f"- Có thể làm máy tính chậm trong quá trình chạy\n"
                    f"- Giao diện có thể bị lag khi cập nhật đồ thị\n\n"
                    f"Khuyến nghị: Sử dụng 20-50 thành phố để cân bằng tốc độ và độ phức tạp.\n\n"
                    f"Bạn có muốn tiếp tục?"
                )
            
            if warning_message:
                response = messagebox.askyesno("Cảnh báo", warning_message)
                if not response:
                    return
            
            self.tsp_problem = TSProblem(num_cities=num_cities)
            
            # Vẽ bản đồ ban đầu
            self._draw_map()
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Đã tạo bài toán với {num_cities} thành phố\n")
            
            # Thêm lưu ý cho các trường hợp đặc biệt
            if num_cities <= 4:
                self.result_text.insert(tk.END, f"\nLưu ý: Bài toán với {num_cities} thành phố rất đơn giản.\n")
                self.result_text.insert(tk.END, f"Thuật toán có thể không thể hiện được hiệu quả tối ưu.\n")
            elif num_cities >= 50:
                self.result_text.insert(tk.END, f"\nLưu ý: Số thành phố lớn ({num_cities}) có thể ảnh hưởng:\n")
                self.result_text.insert(tk.END, f"- Thời gian chạy thuật toán sẽ lâu hơn\n")
                self.result_text.insert(tk.END, f"- Tiêu tốn nhiều tài nguyên CPU và RAM\n")
                self.result_text.insert(tk.END, f"- Giao diện có thể lag khi cập nhật đồ thị\n")
                if num_cities >= 100:
                    self.result_text.insert(tk.END, f"- Máy có thể bị chậm trong quá trình tính toán\n")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo bài toán: {str(e)}")
    
    def _draw_map(self, route=None):
        """
        Vẽ bản đồ thành phố và tuyến đường
        
        Args:
            route: Tuyến đường cần vẽ (None nếu chỉ vẽ thành phố)
        """
        self.ax_map.clear()
        
        # Vẽ các thành phố
        coords = self.tsp_problem.get_city_coords()
        self.ax_map.scatter(coords[:, 0], coords[:, 1], c='red', s=100, zorder=5)
        
        # Đánh số thành phố
        for i, (x, y) in enumerate(coords):
            self.ax_map.annotate(str(i), (x, y + 2), fontsize=8, ha='center', va='bottom')
        
        # Vẽ tuyến đường nếu có
        if route is not None:
            for i in range(len(route)):
                city1 = route[i]
                city2 = route[(i + 1) % len(route)]
                x1, y1 = coords[city1]
                x2, y2 = coords[city2]
                self.ax_map.plot([x1, x2], [y1, y2], 'b-', alpha=0.6, linewidth=1.5)
        
        self.ax_map.set_title("Bản đồ thành phố và tuyến đường tốt nhất")
        self.ax_map.set_xlabel("X")
        self.ax_map.set_ylabel("Y")
        self.ax_map.grid(True, alpha=0.3)
        
        self.canvas.draw()
    
    def _draw_convergence(self, history):
        """
        Vẽ đồ thị hội tụ
        
        Args:
            history: Lịch sử quá trình tìm kiếm [(iteration, distance), ...]
        """
        self.ax_convergence.clear()
        
        if len(history) > 0:
            iterations, distances = zip(*history)
            self.ax_convergence.plot(iterations, distances, 'b-', linewidth=2)
            self.ax_convergence.set_title("Đồ thị hội tụ")
            self.ax_convergence.set_xlabel("Iteration")
            self.ax_convergence.set_ylabel("Distance")
            self.ax_convergence.grid(True, alpha=0.3)
        
        self.canvas.draw()
    
    def _update_callback(self, route, distance, iteration):
        """
        Callback để cập nhật giao diện trong quá trình chạy thuật toán
        
        Args:
            route: Tuyến đường hiện tại
            distance: Khoảng cách hiện tại
            iteration: Vòng lặp hiện tại
        """
        if not self.is_running:
            return
        
        self.best_route = route
        self.best_distance = distance
        
        # Cập nhật progress
        self.progress_var.set(f"Iteration: {iteration} | Distance: {distance:.2f}")
        
        # Cập nhật bản đồ
        self._draw_map(route)
        
        # Cập nhật đồ thị hội tụ
        if self.current_algorithm:
            if hasattr(self.current_algorithm, 'history'):
                self._draw_convergence(self.current_algorithm.history)
        
        self.root.update()
    
    def _validate_algorithm_params(self):
        """
        Validate các tham số thuật toán trước khi chạy
        
        Returns:
            True nếu tất cả tham số hợp lệ, False nếu không
        """
        algorithm_type = self.algorithm_var.get()
        
        try:
            if algorithm_type == "SA":
                # Validate Simulated Annealing parameters
                try:
                    sa_temp = self.sa_temp_var.get()
                except (ValueError, tk.TclError):
                    messagebox.showerror(
                        "Lỗi định dạng",
                        "Lỗi: Nhiệt độ ban đầu phải là số thực\n\nBạn đã nhập giá trị không hợp lệ"
                    )
                    return False
                
                if not self._validate_input(sa_temp, "Nhiệt độ ban đầu", 
                                           min_val=100, max_val=100000, data_type=float):
                    return False
                
                try:
                    cooling_rate = self.sa_cooling_var.get()
                except (ValueError, tk.TclError):
                    messagebox.showerror(
                        "Lỗi định dạng",
                        "Lỗi: Tốc độ làm nguội phải là số thực\n\nBạn đã nhập giá trị không hợp lệ"
                    )
                    return False
                
                if not self._validate_input(cooling_rate, "Tốc độ làm nguội", 
                                           min_val=0.8, max_val=0.9999, data_type=float):
                    return False
                
                try:
                    sa_iterations = self.sa_iterations_var.get()
                except (ValueError, tk.TclError):
                    messagebox.showerror(
                        "Lỗi định dạng",
                        "Lỗi: Số vòng lặp SA phải là số nguyên\n\nBạn đã nhập giá trị không hợp lệ"
                    )
                    return False
                
                if not self._validate_input(sa_iterations, "Số vòng lặp SA", 
                                           min_val=100, max_val=100000, data_type=int):
                    return False
            
            else:  # WOA
                # Validate WOA parameters
                try:
                    woa_whales = self.woa_whales_var.get()
                except (ValueError, tk.TclError):
                    messagebox.showerror(
                        "Lỗi định dạng",
                        "Lỗi: Số cá voi phải là số nguyên\n\nBạn đã nhập giá trị không hợp lệ"
                    )
                    return False
                
                if not self._validate_input(woa_whales, "Số cá voi", 
                                           min_val=5, max_val=100, data_type=int):
                    return False
                
                try:
                    woa_iterations = self.woa_iterations_var.get()
                except (ValueError, tk.TclError):
                    messagebox.showerror(
                        "Lỗi định dạng",
                        "Lỗi: Số vòng lặp WOA phải là số nguyên\n\nBạn đã nhập giá trị không hợp lệ"
                    )
                    return False
                
                if not self._validate_input(woa_iterations, "Số vòng lặp WOA", 
                                           min_val=100, max_val=10000, data_type=int):
                    return False
                
                try:
                    woa_b = self.woa_b_var.get()
                except (ValueError, tk.TclError):
                    messagebox.showerror(
                        "Lỗi định dạng",
                        "Lỗi: Hằng số spiral (b) phải là số thực\n\nBạn đã nhập giá trị không hợp lệ"
                    )
                    return False
                
                if not self._validate_input(woa_b, "Hằng số spiral (b)", 
                                           min_val=0.1, max_val=10.0, data_type=float):
                    return False
                
                try:
                    woa_a = self.woa_a_var.get()
                except (ValueError, tk.TclError):
                    messagebox.showerror(
                        "Lỗi định dạng",
                        "Lỗi: Giá trị a_max phải là số thực\n\nBạn đã nhập giá trị không hợp lệ"
                    )
                    return False
                
                if not self._validate_input(woa_a, "Giá trị a_max", 
                                           min_val=0.5, max_val=5.0, data_type=float):
                    return False
            
            return True
            
        except Exception as e:
            messagebox.showerror(
                "Lỗi",
                f"Lỗi khi kiểm tra tham số\n\nBạn đã nhập giá trị không hợp lệ"
            )
            return False
    
    def _run_algorithm_thread(self):
        """Chạy thuật toán trong thread riêng"""
        try:
            algorithm_type = self.algorithm_var.get()
            
            if algorithm_type == "SA":
                # Simulated Annealing
                self.current_algorithm = SimulatedAnnealing(
                    self.tsp_problem,
                    initial_temp=self.sa_temp_var.get(),
                    cooling_rate=self.sa_cooling_var.get(),
                    max_iterations=self.sa_iterations_var.get()
                )
            else:
                # WOA
                self.current_algorithm = WOA(
                    self.tsp_problem,
                    num_whales=self.woa_whales_var.get(),
                    max_iterations=self.woa_iterations_var.get(),
                    b=self.woa_b_var.get(),
                    a_max=self.woa_a_var.get()
                )
            
            # Chạy thuật toán
            start_time = time.time()
            best_route, best_distance, history = self.current_algorithm.solve(
                callback=self._update_callback
            )
            end_time = time.time()
            
            if not self.is_running:
                return
            
            # Hiển thị kết quả
            self.best_route = best_route
            self.best_distance = best_distance
            self._last_run_time = end_time - start_time
            
            self.result_text.delete(1.0, tk.END)
            info = self.current_algorithm.get_algorithm_info()
            self.result_text.insert(tk.END, f"Thuật toán: {info['name']}\n")
            self.result_text.insert(tk.END, f"\n{'='*35}\n")
            self.result_text.insert(tk.END, f"Khoảng cách tốt nhất: {best_distance:.2f}\n")
            self.result_text.insert(tk.END, f"Thời gian: {end_time - start_time:.2f}s\n")
            self.result_text.insert(tk.END, f"Số thành phố: {len(best_route)}\n")
            self.result_text.insert(tk.END, f"\nTuyến đường:\n")
            # Hiển thị tối đa 20 thành phố
            route_str = " -> ".join(map(str, best_route[:20]))
            if len(best_route) > 20:
                route_str += " -> ..."
            self.result_text.insert(tk.END, f"{route_str}\n")
            self.result_text.insert(tk.END, f"\nNhấn 'Xuất kết quả' để xem đầy đủ\n")
            
            # Kích hoạt nút xuất kết quả
            self.export_button.config(state=tk.NORMAL)
            
            # Vẽ kết quả cuối cùng
            self._draw_map(best_route)
            self._draw_convergence(history)
            
            self.progress_var.set("Hoàn thành!")
            
        except ValueError as e:
            messagebox.showerror(
                "Lỗi giá trị",
                f"Giá trị tham số không hợp lệ:\n{str(e)}\n\nVui lòng kiểm tra lại các tham số đầu vào."
            )
            self.progress_var.set("Lỗi: Giá trị không hợp lệ")
        except MemoryError:
            messagebox.showerror(
                "Lỗi bộ nhớ",
                "Không đủ bộ nhớ để chạy thuật toán.\n\nHãy thử giảm số thành phố hoặc số vòng lặp."
            )
            self.progress_var.set("Lỗi: Không đủ bộ nhớ")
        except KeyboardInterrupt:
            self.progress_var.set("Đã dừng bởi người dùng")
        except Exception as e:
            messagebox.showerror(
                "Lỗi",
                f"Có lỗi xảy ra khi chạy thuật toán:\n\n{type(e).__name__}: {str(e)}\n\nVui lòng kiểm tra lại cấu hình."
            )
            self.progress_var.set(f"Lỗi: {type(e).__name__}")
        finally:
            self.is_running = False
            self.run_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def _run_algorithm(self):
        """Bắt đầu chạy thuật toán"""
        # Kiểm tra bài toán đã được tạo chưa
        if self.tsp_problem is None:
            messagebox.showwarning(
                "Cảnh báo",
                "Vui lòng tạo bài toán trước!\n\nNhấn nút 'Tạo bài toán mới' để bắt đầu."
            )
            return
        
        # Validate các tham số thuật toán
        if not self._validate_algorithm_params():
            return
        
        # Xác nhận nếu số thành phố quá lớn
        num_cities = self.tsp_problem.num_cities
        if num_cities > 80:
            response = messagebox.askyesno(
                "Xác nhận",
                f"Bạn đang chạy thuật toán với {num_cities} thành phố.\n\n"
                f"Cảnh báo về hiệu suất:\n"
                f"- Thời gian chạy có thể rất lâu (vài phút đến vài chục phút)\n"
                f"- Tiêu tốn nhiều CPU và RAM\n"
                f"- Máy tính có thể bị chậm hoặc lag\n"
                f"- Giao diện có thể không phản hồi trong quá trình tính\n\n"
                f"Bạn có muốn tiếp tục không?"
            )
            if not response:
                return
        
        self.is_running = True
        self.run_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.export_button.config(state=tk.DISABLED)
        self.progress_var.set("Đang chạy...")
        
        # Chạy trong thread riêng để không block GUI
        thread = threading.Thread(target=self._run_algorithm_thread)
        thread.daemon = True
        thread.start()
    
    def _stop_algorithm(self):
        """Dừng thuật toán"""
        self.is_running = False
        self.progress_var.set("Đã dừng")
        self.run_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def _export_results(self):
        """Xuất kết quả chi tiết ra cửa sổ mới"""
        if self.best_route is None or self.best_distance is None:
            messagebox.showwarning(
                "Cảnh báo",
                "Chưa có kết quả để xuất.\n\nVui lòng chạy thuật toán trước!"
            )
            return
        
        # Tạo cửa sổ mới
        export_window = tk.Toplevel(self.root)
        export_window.title("Kết quả chi tiết")
        export_window.geometry("700x700")
        export_window.configure(bg='#f0f0f0')
        
        # Canvas với scrollbar cho toàn bộ nội dung
        content_frame = tk.Frame(export_window, bg='#f0f0f0')
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(content_frame, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Style cho các section
        style_title = ('Arial', 16, 'bold')
        style_header = ('Arial', 12, 'bold')
        style_normal = ('Arial', 10)
        style_mono = ('Courier New', 9)
        
        # Tiêu đề chính
        title_frame = tk.Frame(scrollable_frame, bg='#2c3e50', pady=15)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(title_frame, text="KẾT QUẢ GIẢI BÀI TOÁN TSP", 
                font=('Arial', 18, 'bold'), fg='white', bg='#2c3e50').pack()
        
        # Thông tin bài toán
        info_frame = tk.LabelFrame(scrollable_frame, text="THÔNG TIN BÀI TOÁN", 
                       font=style_header, bg='white', padx=15, pady=10)
        info_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(info_frame, text=f"Số thành phố:", font=style_normal, bg='white', anchor='w').grid(row=0, column=0, sticky='w', pady=2)
        tk.Label(info_frame, text=f"{self.tsp_problem.num_cities}", font=('Arial', 10, 'bold'), bg='white', fg='#2980b9').grid(row=0, column=1, sticky='w', padx=10)
        
        # Thông tin thuật toán
        if self.current_algorithm:
            algo_frame = tk.LabelFrame(scrollable_frame, text="THUẬT TOÁN", 
                                       font=style_header, bg='white', padx=15, pady=10)
            algo_frame.pack(fill=tk.X, pady=5)
            
            info = self.current_algorithm.get_algorithm_info()
            tk.Label(algo_frame, text=f"Tên thuật toán:", font=style_normal, bg='white', anchor='w').grid(row=0, column=0, sticky='w', pady=2)
            tk.Label(algo_frame, text=f"{info.get('name', 'N/A')}", font=('Arial', 10, 'bold'), bg='white', fg='#27ae60').grid(row=0, column=1, sticky='w', padx=10)
            
            # Tham số
            param_frame = tk.LabelFrame(scrollable_frame, text="THAM SỐ THUẬT TOÁN", 
                                        font=style_header, bg='white', padx=15, pady=10)
            param_frame.pack(fill=tk.X, pady=5)
            
            algorithm_type = self.algorithm_var.get()
            row = 0
            if algorithm_type == "SA":
                params = [
                    ("Nhiệt độ ban đầu:", self.sa_temp_var.get()),
                    ("Tốc độ làm nguội:", self.sa_cooling_var.get()),
                    ("Số vòng lặp:", self.sa_iterations_var.get())
                ]
            else:  # WOA
                params = [
                    ("Số cá voi:", self.woa_whales_var.get()),
                    ("Số vòng lặp:", self.woa_iterations_var.get()),
                    ("Hằng số spiral (b):", self.woa_b_var.get()),
                    ("Giá trị a_max:", self.woa_a_var.get())
                ]
            
            for label, value in params:
                tk.Label(param_frame, text=label, font=style_normal, bg='white', anchor='w').grid(row=row, column=0, sticky='w', pady=2)
                tk.Label(param_frame, text=str(value), font=('Arial', 10, 'bold'), bg='white', fg='#8e44ad').grid(row=row, column=1, sticky='w', padx=10)
                row += 1
        
        # Kết quả
        result_frame = tk.LabelFrame(scrollable_frame, text="KẾT QUẢ", 
                         font=style_header, bg='#ecf0f1', padx=15, pady=10)
        result_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(result_frame, text="Khoảng cách tốt nhất:", font=style_normal, bg='#ecf0f1', anchor='w').grid(row=0, column=0, sticky='w', pady=2)
        tk.Label(result_frame, text=f"{self.best_distance:.2f}", font=('Arial', 14, 'bold'), bg='#ecf0f1', fg='#e74c3c').grid(row=0, column=1, sticky='w', padx=10)
        
        if hasattr(self, '_last_run_time'):
            tk.Label(result_frame, text="Thời gian chạy:", font=style_normal, bg='#ecf0f1', anchor='w').grid(row=1, column=0, sticky='w', pady=2)
            tk.Label(result_frame, text=f"{self._last_run_time:.2f} giây", font=('Arial', 11, 'bold'), bg='#ecf0f1', fg='#16a085').grid(row=1, column=1, sticky='w', padx=10)
        
        # Tuyến đường
        route_frame = tk.LabelFrame(scrollable_frame, text="TUYẾN ĐƯỜNG ĐẦY ĐỦ", 
                        font=style_header, bg='white', padx=15, pady=10)
        route_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Text widget với scrollbar cho tuyến đường
        route_text_frame = tk.Frame(route_frame, bg='white')
        route_text_frame.pack(fill=tk.BOTH, expand=True)
        
        route_scroll = ttk.Scrollbar(route_text_frame)
        route_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        route_text = tk.Text(route_text_frame, height=8, wrap=tk.WORD, 
                            font=style_mono, yscrollcommand=route_scroll.set,
                            bg='#fafafa', relief=tk.FLAT, padx=10, pady=10)
        route_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        route_scroll.config(command=route_text.yview)
        
        # Hiển thị tuyến đường
        route = self.best_route
        route_lines = []
        for i in range(0, len(route), 10):
            chunk = route[i:i+10]
            route_str = " → ".join(map(str, chunk))
            if i + 10 < len(route):
                route_str += " →"
            route_lines.append(route_str)
        route_lines.append(f" → {route[0]} (quay về điểm xuất phát)")
        route_lines.append("")
        route_lines.append(f"Tổng cộng: {len(route)} thành phố")
        
        route_text.insert(tk.END, "\n".join(route_lines))
        route_text.config(state=tk.DISABLED)
        
        # Thống kê hội tụ
        if self.current_algorithm and hasattr(self.current_algorithm, 'history'):
            history = self.current_algorithm.history
            if len(history) > 0:
                stats_frame = tk.LabelFrame(scrollable_frame, text="📊 THỐNG KÊ QUÁ TRÌNH HỘI TỤ", 
                                           font=style_header, bg='white', padx=15, pady=10)
                stats_frame.pack(fill=tk.X, pady=5)
                
                # Số lần lưu lịch sử (history points)
                stats_data = [
                    ("Số lần lưu lịch sử (history points):", len(history)),
                ]
                # Số vòng lặp hoàn thành thực sự (từ thuật toán)
                actual_iterations = None
                if hasattr(self.current_algorithm, 'actual_iterations'):
                    actual_iterations = getattr(self.current_algorithm, 'actual_iterations')
                elif hasattr(self.current_algorithm, 'iterations'):
                    actual_iterations = getattr(self.current_algorithm, 'iterations')
                if actual_iterations is not None:
                    stats_data.append(("Số vòng lặp hoàn thành thực sự:", actual_iterations))

                stats_data.extend([
                    ("Khoảng cách ban đầu:", f"{history[0][1]:.2f}"),
                    ("Khoảng cách cuối cùng:", f"{history[-1][1]:.2f}"),
                ])

                row = 0
                for label, value in stats_data:
                    tk.Label(stats_frame, text=label, font=style_normal, bg='white', anchor='w').grid(row=row, column=0, sticky='w', pady=2)
                    tk.Label(stats_frame, text=str(value), font=('Arial', 10, 'bold'), bg='white', fg='#34495e').grid(row=row, column=1, sticky='w', padx=10)
                    row += 1

                improvement = ((history[0][1] - history[-1][1]) / history[0][1]) * 100
                tk.Label(stats_frame, text="Cải thiện:", font=style_normal, bg='white', anchor='w').grid(row=row, column=0, sticky='w', pady=2)
                improvement_label = tk.Label(stats_frame, text=f"{improvement:.2f}%", font=('Arial', 12, 'bold'), bg='white', fg='#27ae60')
                improvement_label.grid(row=row, column=1, sticky='w', padx=10)
        
        # Chuẩn bị nội dung text để export
        content = []
        content.append("=" * 80)
        content.append("KẾT QUẢ GIẢI BÀI TOÁN TRAVELLING SALESMAN PROBLEM")
        content.append("=" * 80)
        content.append("")
        content.append(f"Số thành phố: {self.tsp_problem.num_cities}")
        
        if self.current_algorithm:
            info = self.current_algorithm.get_algorithm_info()
            content.append(f"\nThuật toán: {info.get('name', 'N/A')}")
            
            algorithm_type = self.algorithm_var.get()
            content.append("\nTham số:")
            if algorithm_type == "SA":
                content.append(f"  - Nhiệt độ ban đầu: {self.sa_temp_var.get()}")
                content.append(f"  - Tốc độ làm nguội: {self.sa_cooling_var.get()}")
                content.append(f"  - Số vòng lặp: {self.sa_iterations_var.get()}")
            else:
                content.append(f"  - Số cá voi: {self.woa_whales_var.get()}")
                content.append(f"  - Số vòng lặp: {self.woa_iterations_var.get()}")
                content.append(f"  - Hằng số spiral (b): {self.woa_b_var.get()}")
                content.append(f"  - Giá trị a_max: {self.woa_a_var.get()}")
        
        content.append(f"\nKhoảng cách tốt nhất: {self.best_distance:.2f}")
        if hasattr(self, '_last_run_time'):
            content.append(f"Thời gian chạy: {self._last_run_time:.2f} giây")
        
        content.append("\nTuyến đường:")
        content.extend(route_lines)
        
        if self.current_algorithm and hasattr(self.current_algorithm, 'history'):
            history = self.current_algorithm.history
            if len(history) > 0:
                content.append(f"\nSố vòng lặp thực tế: {len(history)}")
                content.append(f"Khoảng cách ban đầu: {history[0][1]:.2f}")
                content.append(f"Khoảng cách cuối cùng: {history[-1][1]:.2f}")
                improvement = ((history[0][1] - history[-1][1]) / history[0][1]) * 100
                content.append(f"Cải thiện: {improvement:.2f}%")
        
        content.append("\n" + "=" * 80)
        

        # Nút sao chép, lưu file, đóng - căn ngang dưới cùng
        def copy_to_clipboard():
            export_window.clipboard_clear()
            export_window.clipboard_append("\n".join(content))
            messagebox.showinfo("Thành công", "Đã sao chép kết quả vào clipboard!", parent=export_window)
            # Do not close or hide the window

        def save_to_file():
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile="ket_qua_tsp.txt",
                parent=export_window
            )
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write("\n".join(content))
                    messagebox.showinfo("Thành công", f"Đã lưu kết quả vào:\n{file_path}", parent=export_window)
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể lưu file:\n{str(e)}", parent=export_window)
            # Do not close or hide the window

        # Frame chứa các nút, đặt ở dưới cùng, căn trái
        button_frame = ttk.Frame(export_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10, anchor='sw')

        btn_copy = ttk.Button(button_frame, text="Sao chép", command=copy_to_clipboard)
        btn_save = ttk.Button(button_frame, text="Lưu file", command=save_to_file)
        btn_close = ttk.Button(button_frame, text="Đóng", command=export_window.destroy)

        btn_copy.pack(side=tk.LEFT, fill=tk.X, padx=(0, 5))
        btn_save.pack(side=tk.LEFT, fill=tk.X, padx=(0, 5))
        btn_close.pack(side=tk.LEFT, fill=tk.X)


def main():
    """Hàm main để chạy ứng dụng"""
    root = tk.Tk()
    app = TSPApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
