"""
Module triển khai thuật toán WOA (Whale Optimization Algorithm) cho TSP
"""
import numpy as np
import random
import math


class Whale:
    """Lớp đại diện cho một cá voi trong WOA"""
    
    def __init__(self, num_cities):
        """
        Khởi tạo cá voi
        
        Args:
            num_cities: Số lượng thành phố
        """
        self.position = list(range(num_cities))
        random.shuffle(self.position)
        self.fitness = float('inf')


class WOA:
    """Lớp triển khai thuật toán WOA (Whale Optimization Algorithm) cho TSP"""
    
    def __init__(self, tsp_problem, num_whales=30, max_iterations=1000,
                 b=1.0, a_max=2.0):
        """
        Khởi tạo thuật toán WOA
        
        Args:
            tsp_problem: Đối tượng TSProblem
            num_whales: Số lượng cá voi
            max_iterations: Số vòng lặp tối đa
            b: Hằng số xác định hình dạng spiral logarit
            a_max: Giá trị a tối đa (giảm dần từ a_max về 0)
        """
        self.tsp = tsp_problem
        self.num_whales = num_whales
        self.max_iterations = max_iterations
        self.b = b  # Constant for spiral shape
        self.a_max = a_max  # Maximum value of a
        
        self.whales = []
        self.leader_position = None  # Vị trí của cá voi tốt nhất (con mồi)
        self.leader_fitness = float('inf')
        self.history = []
    
    def _initialize_whales(self):
        """Khởi tạo quần thể cá voi"""
        self.whales = []
        for _ in range(self.num_whales):
            whale = Whale(self.tsp.num_cities)
            fitness = self.tsp.calculate_route_distance(whale.position)
            whale.fitness = fitness
            
            # Cập nhật leader (con mồi - giải pháp tốt nhất)
            if fitness < self.leader_fitness:
                self.leader_fitness = fitness
                self.leader_position = whale.position.copy()
            
            self.whales.append(whale)
    
    def _encircling_prey(self, whale_position, leader_position, a):
        """
        Cơ chế bao vây con mồi (Encircling Prey)
        Cá voi di chuyển về phía con mồi (giải pháp tốt nhất)
        
        Args:
            whale_position: Vị trí hiện tại của cá voi
            leader_position: Vị trí của con mồi (leader)
            a: Hệ số giảm dần
            
        Returns:
            Vị trí mới
        """
        # C = 2 * random [0,1] (hệ số ngẫu nhiên)
        C = 2 * random.random()
        
        # Tính toán các swap operations để di chuyển về leader
        swaps = self._get_swap_sequence(whale_position, leader_position)
        
        # Số lượng swap phụ thuộc vào |A|
        # A = 2*a*random - a
        A = 2 * a * random.random() - a
        
        # Số swap tỷ lệ với |A| và C
        num_swaps = int(abs(A) * C * len(swaps) / 4)
        num_swaps = max(1, min(num_swaps, len(swaps)))
        
        # Áp dụng swaps
        new_position = whale_position.copy()
        for i in range(num_swaps):
            if i < len(swaps):
                pos1, pos2 = swaps[i]
                new_position[pos1], new_position[pos2] = new_position[pos2], new_position[pos1]
        
        return new_position
    
    def _spiral_updating(self, whale_position, leader_position):
        """
        Cơ chế cập nhật xoắn ốc (Spiral Updating Position)
        Mô phỏng chuyển động xoắn ốc của cá voi khi săn mồi
        
        Args:
            whale_position: Vị trí hiện tại của cá voi
            leader_position: Vị trí của con mồi (leader)
            
        Returns:
            Vị trí mới
        """
        # l = random [-1, 1]
        l = random.uniform(-1, 1)
        
        # Tính toán khoảng cách (số lượng swaps cần thiết)
        swaps = self._get_swap_sequence(whale_position, leader_position)
        
        # D' = distance * e^(b*l) * cos(2*pi*l)
        # Số swap tỷ lệ với công thức spiral
        spiral_factor = math.exp(self.b * l) * math.cos(2 * math.pi * l)
        num_swaps = int(abs(spiral_factor) * len(swaps) / 2)
        num_swaps = max(1, min(num_swaps, len(swaps)))
        
        # Áp dụng swaps
        new_position = whale_position.copy()
        for i in range(num_swaps):
            if i < len(swaps):
                pos1, pos2 = swaps[i]
                new_position[pos1], new_position[pos2] = new_position[pos2], new_position[pos1]
        
        return new_position
    
    def _search_for_prey(self, whale_position, random_whale_position, a):
        """
        Cơ chế tìm kiếm con mồi (Search for Prey)
        Cá voi di chuyển về phía một cá voi ngẫu nhiên khác
        
        Args:
            whale_position: Vị trí hiện tại của cá voi
            random_whale_position: Vị trí của cá voi ngẫu nhiên
            a: Hệ số giảm dần
            
        Returns:
            Vị trí mới
        """
        # C = 2 * random [0,1]
        C = 2 * random.random()
        
        # A = 2*a*random - a (với |A| >= 1, khám phá toàn cục)
        A = 2 * a * random.random() - a
        
        # Tính swaps về phía cá voi ngẫu nhiên
        swaps = self._get_swap_sequence(whale_position, random_whale_position)
        
        # Số swap lớn hơn khi khám phá
        num_swaps = int(abs(A) * C * len(swaps) / 3)
        num_swaps = max(2, min(num_swaps, len(swaps)))
        
        # Áp dụng swaps
        new_position = whale_position.copy()
        for i in range(num_swaps):
            if i < len(swaps):
                pos1, pos2 = swaps[i]
                new_position[pos1], new_position[pos2] = new_position[pos2], new_position[pos1]
        
        return new_position
    
    def _get_swap_sequence(self, route1, route2):
        """
        Tạo dãy các phép swap để biến đổi route1 thành route2
        
        Args:
            route1: Tuyến đường nguồn
            route2: Tuyến đường đích
            
        Returns:
            Danh sách các cặp (i, j) cần swap
        """
        route1_copy = route1.copy()
        swaps = []
        
        for i in range(len(route1)):
            if route1_copy[i] != route2[i]:
                j = route1_copy.index(route2[i])
                if i != j:
                    route1_copy[i], route1_copy[j] = route1_copy[j], route1_copy[i]
                    swaps.append((i, j))
        
        return swaps
    
    def _update_whale(self, whale, iteration):
        """
        Cập nhật vị trí của cá voi dựa trên thuật toán WOA
        
        Args:
            whale: Cá voi cần cập nhật
            iteration: Vòng lặp hiện tại
        """
        # a giảm tuyến tính từ a_max về 0
        a = self.a_max - iteration * (self.a_max / self.max_iterations)
        
        # A = 2*a*random - a
        A = 2 * a * random.random() - a
        
        # p = random [0, 1] để chọn giữa encircling và spiral
        p = random.random()
        
        new_position = None
        
        if p < 0.5:
            # Với xác suất 50%: Sử dụng cơ chế bao vây hoặc tìm kiếm
            if abs(A) < 1:
                # |A| < 1: Bao vây con mồi (exploitation)
                new_position = self._encircling_prey(whale.position, self.leader_position, a)
            else:
                # |A| >= 1: Tìm kiếm con mồi (exploration)
                random_whale = random.choice(self.whales)
                new_position = self._search_for_prey(whale.position, random_whale.position, a)
        else:
            # Với xác suất 50%: Sử dụng cơ chế spiral
            new_position = self._spiral_updating(whale.position, self.leader_position)
        
        # Cập nhật vị trí và fitness
        whale.position = new_position
        fitness = self.tsp.calculate_route_distance(whale.position)
        whale.fitness = fitness
        
        # Cập nhật leader nếu tìm được giải pháp tốt hơn
        if fitness < self.leader_fitness:
            self.leader_fitness = fitness
            self.leader_position = whale.position.copy()
    
    def solve(self, callback=None):
        """
        Giải bài toán TSP bằng WOA (Whale Optimization Algorithm)
        
        Args:
            callback: Hàm callback để cập nhật giao diện (route, distance, iteration)
            
        Returns:
            Tuple (best_route, best_distance, history)
        """
        # Khởi tạo quần thể cá voi
        self._initialize_whales()
        self.history = [(0, self.leader_fitness)]
        
        # Vòng lặp chính
        for iteration in range(1, self.max_iterations + 1):
            # Cập nhật từng cá voi
            for whale in self.whales:
                self._update_whale(whale, iteration)
            
            # Lưu lịch sử mỗi 10 iterations
            if iteration % 10 == 0:
                self.history.append((iteration, self.leader_fitness))
                
                # Gọi callback nếu có
                if callback:
                    callback(self.leader_position, self.leader_fitness, iteration)
        
        # Lưu kết quả cuối cùng
        self.history.append((self.max_iterations, self.leader_fitness))
        
        return self.leader_position, self.leader_fitness, self.history
    
    def get_algorithm_info(self):
        """Lấy thông tin về thuật toán"""
        return {
            'name': 'Whale Optimization Algorithm (WOA)',
            'num_whales': self.num_whales,
            'max_iterations': self.max_iterations,
            'spiral_constant': self.b,
            'a_max': self.a_max
        }
