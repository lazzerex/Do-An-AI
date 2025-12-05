"""
Module triển khai thuật toán Simulated Annealing cho TSP
"""
import numpy as np
import random
import math


class SimulatedAnnealing:
    """Lớp triển khai thuật toán Simulated Annealing"""
    
    def __init__(self, tsp_problem, initial_temp=10000, cooling_rate=0.995, 
                 min_temp=1, max_iterations=10000):
        """
        Khởi tạo thuật toán SA
        
        Args:
            tsp_problem: Đối tượng TSProblem
            initial_temp: Nhiệt độ ban đầu
            cooling_rate: Tốc độ làm nguội (0 < cooling_rate < 1)
            min_temp: Nhiệt độ tối thiểu
            max_iterations: Số vòng lặp tối đa
        """
        # Validate parameters
        if tsp_problem is None:
            raise ValueError("tsp_problem không được None")
        
        if initial_temp <= 0:
            raise ValueError(f"Nhiệt độ ban đầu phải > 0, nhận được: {initial_temp}")
        
        if not 0 < cooling_rate < 1:
            raise ValueError(f"Tốc độ làm nguội phải trong khoảng (0, 1), nhận được: {cooling_rate}")
        
        if min_temp <= 0:
            raise ValueError(f"Nhiệt độ tối thiểu phải > 0, nhận được: {min_temp}")
        
        if min_temp >= initial_temp:
            raise ValueError(f"Nhiệt độ tối thiểu ({min_temp}) phải < nhiệt độ ban đầu ({initial_temp})")
        
        if max_iterations <= 0:
            raise ValueError(f"Số vòng lặp phải > 0, nhận được: {max_iterations}")
        
        self.tsp = tsp_problem
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.max_iterations = max_iterations
        
        self.best_route = None
        self.best_distance = float('inf')
        self.history = []  # Lưu lịch sử quá trình tìm kiếm
    
    def _get_neighbor(self, route):
        """
        Tạo láng giềng của tuyến đường hiện tại bằng cách swap 2 thành phố
        
        Args:
            route: Tuyến đường hiện tại
            
        Returns:
            Tuyến đường láng giềng
        """
        neighbor = route.copy()
        i, j = random.sample(range(len(route)), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        return neighbor
    
    def _acceptance_probability(self, current_dist, neighbor_dist, temp):
        """
        Tính xác suất chấp nhận giải pháp xấu hơn
        
        Args:
            current_dist: Khoảng cách hiện tại
            neighbor_dist: Khoảng cách láng giềng
            temp: Nhiệt độ hiện tại
            
        Returns:
            Xác suất chấp nhận
        """
        if neighbor_dist < current_dist:
            return 1.0
        return math.exp((current_dist - neighbor_dist) / temp)
    
    def solve(self, callback=None):
        """
        Giải bài toán TSP bằng Simulated Annealing
        
        Args:
            callback: Hàm callback để cập nhật giao diện (route, distance, iteration)
            
        Returns:
            Tuple (best_route, best_distance, history)
        """
        # Khởi tạo tuyến đường ban đầu
        current_route = self.tsp.generate_random_route()
        current_distance = self.tsp.calculate_route_distance(current_route)
        
        self.best_route = current_route.copy()
        self.best_distance = current_distance
        self.history = [(0, current_distance)]
        
        temp = self.initial_temp
        iteration = 0
        self.actual_iterations = 0  # Track actual completed iterations
        
        while temp > self.min_temp and iteration < self.max_iterations:
            # Tạo láng giềng
            neighbor_route = self._get_neighbor(current_route)
            neighbor_distance = self.tsp.calculate_route_distance(neighbor_route)
            
            # Quyết định có chấp nhận láng giềng không
            if self._acceptance_probability(current_distance, neighbor_distance, temp) > random.random():
                current_route = neighbor_route
                current_distance = neighbor_distance
                
                # Cập nhật best nếu tốt hơn
                if current_distance < self.best_distance:
                    self.best_route = current_route.copy()
                    self.best_distance = current_distance
            
            # Làm nguội
            temp *= self.cooling_rate
            iteration += 1
            self.actual_iterations = iteration
            
            # Lưu lịch sử mỗi 100 iterations
            if iteration % 100 == 0:
                self.history.append((iteration, self.best_distance))
                
                # Gọi callback nếu có
                if callback:
                    callback(self.best_route, self.best_distance, iteration)
        
        # Lưu kết quả cuối cùng
        self.history.append((iteration, self.best_distance))
        
        return self.best_route, self.best_distance, self.history
    
    def get_algorithm_info(self):
        """Lấy thông tin về thuật toán"""
        return {
            'name': 'Simulated Annealing',
            'initial_temp': self.initial_temp,
            'cooling_rate': self.cooling_rate,
            'min_temp': self.min_temp,
            'max_iterations': self.max_iterations
        }
