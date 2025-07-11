# Структура тестбенча для FFT модуля

## 1. Общая архитектура

```
sim/
├── fft_tb/
│   ├── test_fft_basic.py          # Базовые тесты FFT
│   ├── test_fft_accuracy.py       # Тесты точности
│   ├── test_fft_performance.py    # Тесты производительности
│   ├── test_fft_edge_cases.py     # Граничные случаи
│   └── test_fft_stress.py         # Стресс-тесты
├── fft_models/
│   ├── golden_model.py            # Эталонная модель FFT (Python/NumPy)
│   ├── test_vectors.py            # Генератор тестовых векторов
│   └── metrics_calculator.py      # Калькулятор метрик качества
├── fft_dut/
│   ├── fft_core.v                 # Основной FFT модуль
│   ├── fft_butterfly.v            # Блок butterfly
│   ├── fft_twiddle.v              # Таблица twiddle factors
│   └── fft_memory.v               # Память для данных
└── config/
    ├── fft_config.py              # Конфигурация тестов
    └── test_scenarios.py          # Сценарии тестирования
```

## 2. Основные компоненты тестбенча

### 2.1 Golden Model (эталонная модель)
```python
# fft_models/golden_model.py
import numpy as np

class FFTGoldenModel:
    def __init__(self, fft_size, data_width):
        self.fft_size = fft_size
        self.data_width = data_width
    
    def compute_fft(self, input_data):
        return np.fft.fft(input_data)
    
    def compute_ifft(self, input_data):
        return np.fft.ifft(input_data)
```

### 2.2 Test Vector Generator
```python
# fft_models/test_vectors.py
class FFTTestVectors:
    def generate_sine_wave(self, frequency, amplitude):
        # Генерация синусоидального сигнала
    
    def generate_impulse(self):
        # Генерация импульсного сигнала
    
    def generate_random_data(self):
        # Генерация случайных данных
    
    def generate_known_pattern(self):
        # Генерация известного паттерна
```

### 2.3 Metrics Calculator
```python
# fft_models/metrics_calculator.py
class FFTMetrics:
    def calculate_snr(self, reference, actual):
        # Вычисление SNR
    
    def calculate_enob(self, snr):
        # Вычисление ENOB
    
    def calculate_rounding_error(self, reference, actual):
        # Вычисление ошибки округления
    
    def calculate_throughput(self, cycles, data_size):
        # Вычисление пропускной способности
```

## 3. Типы тестов

### 3.1 Базовые тесты (test_fft_basic.py)
- Корректность FFT для простых сигналов
- Корректность iFFT
- Проверка FFT → iFFT → исходный сигнал
- Тесты с разными размерами FFT

### 3.2 Тесты точности (test_fft_accuracy.py)
- Сравнение с golden model
- Вычисление SNR/ENOB
- Анализ ошибок округления
- Тесты с разной разрядностью

### 3.3 Тесты производительности (test_fft_performance.py)
- Измерение задержки (latency)
- Измерение пропускной способности
- Анализ использования ресурсов
- Тесты на максимальной частоте

### 3.4 Граничные случаи (test_fft_edge_cases.py)
- Тесты с нулевыми данными
- Тесты с максимальными значениями
- Тесты с минимальными значениями
- Тесты переполнения

### 3.5 Стресс-тесты (test_fft_stress.py)
- Длительные тесты
- Тесты с высокой нагрузкой
- Тесты стабильности
- Тесты восстановления после ошибок

## 4. Конфигурация тестов

### 4.1 FFT Configuration
```python
# config/fft_config.py
FFT_CONFIG = {
    'sizes': [64, 128, 256, 512, 1024],
    'data_widths': [8, 16, 24, 32],
    'test_signals': ['sine', 'impulse', 'random', 'chirp'],
    'frequencies': [1, 10, 100, 1000],
    'amplitudes': [0.1, 0.5, 1.0],
    'simulation_time': 10000,
    'clock_period': 10
}
```

### 4.2 Test Scenarios
```python
# config/test_scenarios.py
TEST_SCENARIOS = {
    'basic_validation': {
        'fft_sizes': [64, 128],
        'data_widths': [16],
        'signals': ['sine', 'impulse'],
        'metrics': ['snr', 'latency']
    },
    'accuracy_analysis': {
        'fft_sizes': [256, 512],
        'data_widths': [8, 16, 24],
        'signals': ['sine', 'random'],
        'metrics': ['snr', 'enob', 'rounding_error']
    },
    'performance_test': {
        'fft_sizes': [1024],
        'data_widths': [16],
        'signals': ['random'],
        'metrics': ['throughput', 'resource_usage']
    }
}
```

## 5. Автоматизация тестирования

### 5.1 Обновленный run-cocotb.py
```python
# Добавить в test_configs:
{
    "name": "FFT Basic Test",
    "verilog_file": "fft_core.v",
    "test_file": "test_fft_basic.py",
    "simulator": "icarus",
    "extra_args": ["--fft-size", "128", "--data-width", "16"]
},
{
    "name": "FFT Accuracy Test",
    "verilog_file": "fft_core.v",
    "test_file": "test_fft_accuracy.py",
    "simulator": "icarus",
    "extra_args": ["--fft-size", "256", "--data-width", "24"]
}
```

## 6. Метрики качества

### 6.1 Основные метрики
- **SNR (Signal-to-Noise Ratio)**: Отношение сигнал/шум
- **ENOB (Effective Number of Bits)**: Эффективное количество бит
- **Latency**: Задержка от входа до выхода
- **Throughput**: Пропускная способность (образцы/сек)
- **Resource Usage**: Использование ресурсов FPGA

### 6.2 Дополнительные метрики
- **Rounding Error**: Ошибка округления
- **Frequency Response**: Частотная характеристика
- **Phase Response**: Фазовая характеристика
- **Dynamic Range**: Динамический диапазон

