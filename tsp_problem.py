"""
Module định nghĩa bài toán TSP (Travelling Salesman Problem)
"""
import numpy as np
import random


class TSProblem:
    """Lớp đại diện cho bài toán người du lịch"""
    
    def __init__(self, num_cities=20, city_coords=None):
        """
        Khởi tạo bài toán TSP
        
        Args:
            num_cities: Số lượng thành phố
            city_coords: Tọa độ các thành phố (nếu có)
        """
        self.num_cities = num_cities
        
        if city_coords is not None:
            self.city_coords = np.array(city_coords)
            self.num_cities = len(city_coords)
        else:
            # Tạo ngẫu nhiên tọa độ các thành phố trong khoảng [0, 100]
            self.city_coords = np.random.rand(num_cities, 2) * 100
        
        # Tính ma trận khoảng cách
        self.distance_matrix = self._calculate_distance_matrix()
    
    def _calculate_distance_matrix(self):
        """Tính ma trận khoảng cách giữa các thành phố"""
        n = self.num_cities
        dist_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.sqrt(
                    (self.city_coords[i][0] - self.city_coords[j][0]) ** 2 +
                    (self.city_coords[i][1] - self.city_coords[j][1]) ** 2
                )
                dist_matrix[i][j] = dist
                dist_matrix[j][i] = dist
        
        return dist_matrix
    
    def calculate_route_distance(self, route):
        """
        Tính tổng khoảng cách của một tuyến đường
        
        Args:
            route: Danh sách thứ tự các thành phố
            
        Returns:
            Tổng khoảng cách
        """
        total_distance = 0
        for i in range(len(route)):
            city1 = route[i]
            city2 = route[(i + 1) % len(route)]
            total_distance += self.distance_matrix[city1][city2]
        return total_distance
    
    def generate_random_route(self):
        """Tạo một tuyến đường ngẫu nhiên"""
        route = list(range(self.num_cities))
        random.shuffle(route)
        return route
    
    def get_city_coords(self):
        """Lấy tọa độ các thành phố"""
        return self.city_coords.copy()
