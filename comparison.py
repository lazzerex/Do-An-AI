"""
Script so sánh hiệu năng SA và WOA
"""
import time
import numpy as np
from tsp_problem import TSProblem
from simulated_annealing import SimulatedAnnealing
from woa_algorithm import WOA
def run_comparison(num_cities, num_runs=5):
    """
    So sánh SA và WOA trên bài toán TSP
    
    Args:
        num_cities: Số thành phố
        num_runs: Số lần chạy
    """
    results = {
        'SA': {'distances': [], 'times': []},
        'WOA': {'distances': [], 'times': []}
    }
    
    seeds = [42, 123, 456, 789, 1000]
    
    # Tham số dựa trên kích thước bài toán
    if num_cities == 20:
        sa_params = {'initial_temp': 10000, 'cooling_rate': 0.995, 'max_iterations': 10000}
        woa_params = {'num_whales': 30, 'max_iterations': 1000}
    elif num_cities == 50:
        sa_params = {'initial_temp': 15000, 'cooling_rate': 0.997, 'max_iterations': 20000}
        woa_params = {'num_whales': 40, 'max_iterations': 1500}
    else:  # 100
        sa_params = {'initial_temp': 20000, 'cooling_rate': 0.998, 'max_iterations': 30000}
        woa_params = {'num_whales': 50, 'max_iterations': 2000}
    
    print(f"\n{'='*60}")
    print(f"So sánh trên bài toán {num_cities} thành phố")
    print(f"{'='*60}\n")
    
    for run_id in range(num_runs):
        seed = seeds[run_id]
        print(f"Run {run_id + 1}/{num_runs} (seed={seed}):")
        
        # ===== TEST SIMULATED ANNEALING =====
        np.random.seed(seed)
        tsp = TSProblem(num_cities=num_cities)
        
        sa = SimulatedAnnealing(
            tsp, 
            initial_temp=sa_params['initial_temp'],
            cooling_rate=sa_params['cooling_rate'],
            max_iterations=sa_params['max_iterations']
        )
        
        start_time = time.time()
        sa_best_route, sa_best_distance, _ = sa.solve()
        sa_time = time.time() - start_time
        
        results['SA']['distances'].append(sa_best_distance)
        results['SA']['times'].append(sa_time)
        
        print(f"  SA  - Distance: {sa_best_distance:.2f}, Time: {sa_time:.2f}s")
        
        # ===== TEST WOA =====
        np.random.seed(seed)
        tsp = TSProblem(num_cities=num_cities)
        
        woa = WOA(
            tsp,
            num_whales=woa_params['num_whales'],
            max_iterations=woa_params['max_iterations']
        )
        
        start_time = time.time()
        woa_best_route, woa_best_distance, _ = woa.solve()
        woa_time = time.time() - start_time
        
        results['WOA']['distances'].append(woa_best_distance)
        results['WOA']['times'].append(woa_time)
        
        print(f"  WOA - Distance: {woa_best_distance:.2f}, Time: {woa_time:.2f}s")
        print()
    
    # Tính toán thống kê
    print(f"\n{'='*60}")
    print(f"KẾT QUẢ TỔNG HỢP ({num_cities} thành phố)")
    print(f"{'='*60}\n")
    
    for algo in ['SA', 'WOA']:
        distances = results[algo]['distances']
        times = results[algo]['times']
        
        print(f"{algo}:")
        print(f"  Khoảng cách:")
        print(f"    - Trung bình: {np.mean(distances):.2f}")
        print(f"    - Tốt nhất: {np.min(distances):.2f}")
        print(f"    - Tệ nhất: {np.max(distances):.2f}")
        print(f"    - Độ lệch chuẩn: {np.std(distances):.2f}")
        print(f"  Thời gian:")
        print(f"    - Trung bình: {np.mean(times):.2f}s")
        print(f"    - Độ lệch chuẩn: {np.std(times):.2f}s")
        print()
    
    # So sánh
    sa_avg_dist = np.mean(results['SA']['distances'])
    woa_avg_dist = np.mean(results['WOA']['distances'])
    sa_avg_time = np.mean(results['SA']['times'])
    woa_avg_time = np.mean(results['WOA']['times'])
    
    print(f"SO SÁNH:")
    print(f"  Chất lượng giải pháp:")
    if sa_avg_dist < woa_avg_dist:
        improvement = ((woa_avg_dist - sa_avg_dist) / woa_avg_dist) * 100
        print(f"    ✓ SA tốt hơn {improvement:.2f}%")
    else:
        improvement = ((sa_avg_dist - woa_avg_dist) / sa_avg_dist) * 100
        print(f"    ✓ WOA tốt hơn {improvement:.2f}%")
    
    print(f"  Thời gian chạy:")
    speedup = woa_avg_time / sa_avg_time
    print(f"    ✓ SA nhanh hơn {speedup:.2f}x")
    print()
    
    return results

if __name__ == "__main__":
    # Chạy so sánh cho các kích thước khác nhau
    for num_cities in [20, 50, 100]:
        results = run_comparison(num_cities, num_runs=5)
        
        # Lưu kết quả ra file
        with open(f'results_{num_cities}_cities.txt', 'w', encoding='utf-8') as f:
            f.write(f"Kết quả so sánh {num_cities} thành phố\n")
            f.write(f"{'='*60}\n\n")
            
            for algo in ['SA', 'WOA']:
                f.write(f"{algo}:\n")
                f.write(f"Distances: {results[algo]['distances']}\n")
                f.write(f"Times: {results[algo]['times']}\n\n")