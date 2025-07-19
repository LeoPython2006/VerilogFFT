# Quartus FFT Blocks Testing

Автоматизированное тестирование open-source FFT блоков в Quartus Prime.

## Структура

```
quartus_test/
├── quartus_test_script.py      # Основной скрипт тестирования
├── download_fft_blocks.py      # Скрипт загрузки FFT блоков
└── README.md                   # Этот файл
```

## Быстрый старт

### 1. Загрузка FFT блоков
```bash
python quartus_test/download_fft_blocks.py
```

Этот скрипт автоматически скачает:
- Pipelined FFT/IFFT 128 points (GitHub)
- Pipelined FFT/IFFT 64 points (GitHub)  
- FFT Generator (GitHub)
- Versatile FFT (OpenCores - ручная загрузка)

### 2. Запуск тестирования
```bash
python quartus_test/quartus_test_script.py
```

## Что тестируется

### Анализ (Analysis)
- Проверка синтаксиса Verilog
- Проверка связности модулей
- Поиск ошибок компиляции

### Синтез (Synthesis)
- Синтез в целевую FPGA (Cyclone V)
- Извлечение ресурсов (LUT, FF, DSP, BRAM)
- Анализ временных характеристик (Fmax)

## Результаты

Скрипт генерирует два отчёта:

### JSON отчёт (`quartus_test_results.json`)
```json
{
  "timestamp": "2025-07-15 18:30:00",
  "quartus_path": "/opt/intelFPGA/21.1/quartus/bin/quartus_sh",
  "results": {
    "Pipelined_FFT_128": {
      "analysis_success": true,
      "synthesis_success": true,
      "resources": {
        "LUT": 4147,
        "FF": 1254,
        "DSP": 4,
        "BRAM_bits": 5120
      },
      "fmax": 215.0
    }
  }
}
```

### HTML отчёт (`quartus_test_results.html`)
Красивый веб-отчёт с таблицей результатов.

## Настройка

### Путь к Quartus Prime
Скрипт автоматически ищет Quartus в стандартных местах:
- Linux: `/opt/intelFPGA/*/quartus/bin/quartus_sh`
- Windows: `C:/intelFPGA/*/quartus/bin64/quartus_sh.exe`

Если не найден, укажите путь вручную.

### Целевая FPGA
По умолчанию используется Cyclone V (5CEBA4F23C7).
Для изменения отредактируйте `create_quartus_project()` в скрипте.

## Добавление новых блоков

1. Добавьте конфигурацию в `test_configs`:
```python
{
    "name": "Your_FFT_Block",
    "files": ["your_fft.v"],
    "top": "your_top_module"
}
```

2. Поместите Verilog файлы в корневую директорию
3. Запустите тестирование

## Требования

- Python 3.6+
- Quartus Prime (20.1 или новее)
- Git (для загрузки с GitHub)

## Примеры использования

### Тестирование одного блока
```python
tester = QuartusTester()
tester.test_fft_block("My_FFT", ["my_fft.v"], "my_top_module")
```

### Пользовательская конфигурация
```python
# Изменение целевой FPGA
qsf_content = """
set_global_assignment -name FAMILY "Arria 10"
set_global_assignment -name DEVICE 10AX115H2F34I1SG
"""
```

## Устранение неполадок

### Quartus не найден
```bash
# Укажите путь вручную
export QUARTUS_PATH="/path/to/quartus/bin/quartus_sh"
python quartus_test_script.py
```

### Ошибки синтеза
- Проверьте совместимость синтаксиса Verilog
- Убедитесь, что все зависимости подключены
- Проверьте ограничения по ресурсам

### Таймауты
- Увеличьте timeout в `run_quartus_synthesis()`
- Проверьте производительность системы 