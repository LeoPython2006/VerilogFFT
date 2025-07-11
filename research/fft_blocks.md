# Популярные open-source FFT-ядра (Verilog/VHDL) — июль 2025

## Критерии популярности
* **GitHub ★** и fork’и  
* Недавняя активность коммитов (2024-2025 гг.)  
* Использование в реальных проектах, открытые issues / PR.

---

## Сравнительная таблица

| ★ GitHub (июль 2025) | Проект / репозиторий | HDL | Ключевые особенности |
| --- | --- | --- | --- |
| **242** | [dblclockfft](https://github.com/ZipCPU/dblclockfft) | Verilog + C++ | Генератор FFT/IFFT, 1–2 выб/такт, любой `N = 2ᵏ`, потоковая обработка |
| **122** | [r22sdf](https://github.com/nanamake/r22sdf) | Verilog | Radix-2² SDF, фикс-точка, 64–4096 точек, режим «resource saving» |
| **115** | [fpga-fft](https://github.com/owocomm-0/fpga-fft) | VHDL | Bailey 4-step до 65 536 точек, AXI-интерфейс, примеры cocotb |
| **65** | [FFT_ChipDesign](https://github.com/VenciFreeman/FFT_ChipDesign) | Verilog | 16-точечный Radix-4 FFT, полный ASIC-поток *(RTL → GDS)* |
| **60** | [fp23fftk](https://github.com/hukenovs/fp23fftk) | VHDL / Verilog | Плавающая точка (FP-23), конвейерный FFT/IFFT для Xilinx 6/7/UltraScale |
| **54** | [32-point-FFT-DIT](https://github.com/AhmedAalaaa/32-point-FFT-DIT) | Verilog | 32-точечный Radix-2 DIT, тайм-шеринг; удобен для учебных проектов |

---

## Как выбрать ядро под задачу

| Требование | Рекомендованное ядро |
| --- | --- |
| **Гибко менять размер** и быстро генерировать RTL | `dblclockfft` |
| **Минимум ресурсов на фикс-точке** (малые FPGA, OFDM) | `r22sdf` |
| **Очень большие N (4 k – 64 k)**, непрерывный поток | `fpga-fft` |
| **Плавающая точка без платных IP** | `fp23fftk` |
| **Учебный пример RTL→GDS** | `FFT_ChipDesign` или `32-point-FFT-DIT` |

