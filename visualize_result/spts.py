import matplotlib.pyplot as plt

# Dữ liệu
steps = [355, 360, 365, 370]
proposed = [0.7816, 0.7872, 0.7797, 0.7884]
baseline = [0.7699, 0.7712, 0.7697, 0.7718]
method1 = [0.7843, 0.7898, 0.7821, 0.7816]
# method2 = [0.7609, 0.7178, 0.6635, 0.5648]
method3 = [0.7798, 0.7892, 0.7820, 0.7827]

# Tạo biểu đồ
plt.figure(figsize=(12, 8))
plt.plot(steps, proposed, marker='o', label='Proposed Method')
plt.plot(steps, baseline, marker='s', label='Baseline')
plt.plot(steps, method1, marker='^', label='Method 1')
# plt.plot(steps, method2, marker='D', label='Method 2')
plt.plot(steps, method3, marker='*', label='Method 3')

# Đặt tên cho các trục và tiêu đề
plt.xlabel('Training Steps')
plt.ylabel('H mean')
plt.title('Comparison of Different Methods')

# Thêm lưới
plt.grid(True, linestyle='--', alpha=0.7)

# Thêm chú thích
plt.legend()

# Điều chỉnh layout
plt.tight_layout()

# Lưu biểu đồ thành file PDF
plt.savefig('data/comparison_chart_5methods.pdf')

print("Biểu đồ đã được lưu thành công vào file 'comparison_chart_5methods.pdf'")