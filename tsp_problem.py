"""
Module định nghĩa bài toán TSP (Traveling Salesman Problem)
Bài toán người bán hàng - tìm đường đi ngắn nhất qua tất cả thành phố
"""
import numpy as np
from typing import List, Optional, Tuple


class TSProblem:
    """
    Class mô tả bài toán Traveling Salesman Problem
    
    Attributes:
        num_cities: Số lượng thành phố
        city_coords: Mảng numpy chứa tọa độ (x, y) của các thành phố
        distance_matrix: Ma trận khoảng cách giữa các cặp thành phố
    """
    
    MIN_CITIES = 3
    MAX_CITIES = 500
    COORD_RANGE = 100.0
    
    def __init__(self, num_cities: int = 20, city_coords: Optional[np.ndarray] = None):
        """
        Khởi tạo bài toán TSP
        
        Args:
            num_cities: Số thành phố cần tạo (mặc định 20)
            city_coords: Tọa độ cho trước (nếu None sẽ tạo ngẫu nhiên)
            
        Raises:
            ValueError: Nếu tham số không hợp lệ
        """
        self._validate_and_init(num_cities, city_coords)
        self.distance_matrix = self._build_distance_matrix()
    
    def _validate_and_init(self, num_cities: int, city_coords: Optional[np.ndarray]) -> None:
        """Kiểm tra tham số và khởi tạo tọa độ thành phố"""
        
        if city_coords is not None:
            coords = np.asarray(city_coords)
            self._check_coords_valid(coords)
            self.city_coords = coords
            self.num_cities = coords.shape[0]
        else:
            self._check_num_cities_valid(num_cities)
            self.num_cities = num_cities
            self.city_coords = self._generate_random_coords()
    
    def _check_num_cities_valid(self, n: int) -> None:
        """Kiểm tra số thành phố có hợp lệ không"""
        if n < self.MIN_CITIES:
            raise ValueError(
                f"Cần tối thiểu {self.MIN_CITIES} thành phố, nhận được: {n}\n"
                f"Lý do: Với ít hơn 3 thành phố, bài toán không có ý nghĩa tối ưu."
            )
        if n > self.MAX_CITIES:
            raise ValueError(
                f"Tối đa {self.MAX_CITIES} thành phố, nhận được: {n}\n"
                f"Lý do: Số thành phố lớn sẽ gây tốn tài nguyên và thời gian."
            )
    
    def _check_coords_valid(self, coords: np.ndarray) -> None:
        """Kiểm tra tọa độ có hợp lệ không"""
        if coords.ndim != 2 or coords.shape[1] != 2:
            raise ValueError(
                f"Tọa độ phải có shape (n, 2), nhận được: {coords.shape}"
            )
        if coords.shape[0] < self.MIN_CITIES:
            raise ValueError(
                f"Cần tối thiểu {self.MIN_CITIES} thành phố, nhận được: {coords.shape[0]}"
            )
    
    def _generate_random_coords(self) -> np.ndarray:
        """Sinh tọa độ ngẫu nhiên cho các thành phố"""
        return np.random.uniform(0, self.COORD_RANGE, size=(self.num_cities, 2))
    
    def _build_distance_matrix(self) -> np.ndarray:
        """
        Xây dựng ma trận khoảng cách Euclidean
        Sử dụng broadcasting để tính nhanh hơn
        """
        # Tính khoảng cách dùng broadcasting (nhanh hơn vòng lặp)
        diff = self.city_coords[:, np.newaxis, :] - self.city_coords[np.newaxis, :, :]
        return np.sqrt(np.sum(diff ** 2, axis=2))
    
    def calculate_route_distance(self, route: List[int]) -> float:
        """
        Tính tổng độ dài của một tuyến đường
        
        Args:
            route: Danh sách chỉ số thành phố theo thứ tự đi
            
        Returns:
            Tổng khoảng cách của tuyến đường (bao gồm quay về điểm đầu)
            
        Raises:
            ValueError: Nếu tuyến đường không hợp lệ
        """
        self._validate_route(route)
        
        # Tính tổng khoảng cách
        route_arr = np.array(route)
        next_cities = np.roll(route_arr, -1)  # Dịch sang trái 1 vị trí
        
        return np.sum(self.distance_matrix[route_arr, next_cities])
    
    def _validate_route(self, route: List[int]) -> None:
        """Kiểm tra tuyến đường có hợp lệ không"""
        if not route:
            raise ValueError("Tuyến đường rỗng")
        
        if len(route) != self.num_cities:
            raise ValueError(
                f"Tuyến đường cần {self.num_cities} thành phố, nhận được: {len(route)}"
            )
        
        route_set = set(route)
        if len(route_set) != len(route):
            raise ValueError("Tuyến đường có thành phố trùng lặp")
        
        if min(route) < 0 or max(route) >= self.num_cities:
            raise ValueError(
                f"Chỉ số thành phố phải trong [0, {self.num_cities - 1}]"
            )
    
    def generate_random_route(self) -> List[int]:
        """
        Tạo một tuyến đường ngẫu nhiên
        
        Returns:
            Danh sách chỉ số thành phố được xáo trộn ngẫu nhiên
        """
        route = list(range(self.num_cities))
        np.random.shuffle(route)
        return route
    
    def get_city_coords(self) -> np.ndarray:
        """
        Lấy bản sao tọa độ các thành phố
        
        Returns:
            Mảng numpy shape (num_cities, 2)
        """
        return self.city_coords.copy()
    
    def get_distance(self, city1: int, city2: int) -> float:
        """
        Lấy khoảng cách giữa 2 thành phố
        
        Args:
            city1: Chỉ số thành phố thứ nhất
            city2: Chỉ số thành phố thứ hai
            
        Returns:
            Khoảng cách Euclidean
        """
        return self.distance_matrix[city1, city2]
    
    def __repr__(self) -> str:
        return f"TSProblem(num_cities={self.num_cities})"
    
    def __str__(self) -> str:
        return f"Bài toán TSP với {self.num_cities} thành phố"