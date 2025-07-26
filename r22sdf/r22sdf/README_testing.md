# Тестирование TopOverlapFFT128 с cocotb

Этот проект содержит тесты для проверки точности реализации FFT с overlap-add на FPGA.

## Установка зависимостей

```bash
# Установка Python зависимостей
pip install -r requirements.txt

# Установка симулятора (Icarus Verilog)
sudo apt-get install iverilog  # Ubuntu/Debian
# или
brew install icarus-verilog    # macOS
```

## Запуск тестов

```bash
# Запуск всех тестов
make test

# Или пошагово:
make sim
```

## Анализ результатов

После выполнения тестов результаты сохраняются в папку `test_results/`:

### Файлы результатов:
- `reference.txt` - эталонный сигнал
- `fpga_output.txt` - выход FPGA
- `error.txt` - ошибка (reference - fpga_output)
- `rms_stats.txt` - статистика ошибок
- `rms_analysis.png` - графики анализа

### Просмотр результатов:

```bash
# Показать статистику RMS
make results

# Открыть графики
make plot

# Просмотр волновых форм (если есть)
make wave
```

## Метрики качества

### RMS ошибка (Root Mean Square)
Вычисляется как:
```
RMS = sqrt(mean((reference - fpga_output)^2))
```

### Дополнительные метрики:
- **Максимальная ошибка**: max(|error|)
- **Средняя ошибка**: mean(error)
- **Стандартное отклонение**: std(error)

## Тестовые сценарии

1. **test_overlap_fft_rms**: Основной тест с синусоидой + шум
2. **test_impulse_response**: Тест с единичным импульсом
3. **test_noise_rejection**: Тест подавления белого шума

## Интерпретация результатов

- **RMS < 10**: Отличное качество
- **RMS < 50**: Хорошее качество
- **RMS < 100**: Приемлемое качество
- **RMS > 100**: Требует доработки

## Устранение неполадок

### Ошибка "No module named 'cocotb'"
```bash
pip install cocotb
```

### Ошибка "iverilog: command not found"
```bash
sudo apt-get install iverilog
```

### Ошибка "No module named 'matplotlib'"
```bash
pip install matplotlib
```

## Настройка тестов

Для изменения параметров тестов отредактируйте `test_cocotb.py`:

- `sample_rate`: частота дискретизации (по умолчанию 48000)
- `duration`: длительность тестового сигнала (по умолчанию 0.1 сек)
- `test_signal`: тип тестового сигнала

## Пример вывода

```
Тестируем 4800 сэмплов...
Обработано 4800 выходных сэмплов
RMS ошибка: 12.3456
Максимальная ошибка: 45.6789
Средняя ошибка: 0.1234
``` 