import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
import numpy as np
import matplotlib.pyplot as plt
import os

reference_signal = []
fpga_output = []
test_errors = []

@cocotb.test()
async def test_overlap_fft_rms(dut):
    
    clock = Clock(dut.clock, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    dut.reset.value = 1
    await RisingEdge(dut.clock)
    dut.reset.value = 0
    await RisingEdge(dut.clock)
    
    sample_rate = 48000
    duration = 0.1  
    num_samples = int(sample_rate * duration)
    
    t = np.linspace(0, duration, num_samples, False)
    test_signal = np.sin(2 * np.pi * 1000 * t) + 0.1 * np.random.randn(num_samples)
    
    test_signal = np.clip(test_signal * 16384, -32768, 32767).astype(np.int16)
    
    print(f"Тестируем {num_samples} сэмплов...")
    
    sample_count = 0
    for i, sample in enumerate(test_signal):
        dut.din.value = int(sample)
        dut.din_valid.value = 1
        dut.din_last.value = 1 if i == len(test_signal) - 1 else 0
        
        await RisingEdge(dut.clock)
        sample_count += 1
        
        if dut.dout_valid.value == 1:
            fpga_output.append(int(dut.dout_re.value))
            if len(reference_signal) < len(fpga_output):
                reference_signal.append(sample)
    
    while dut.done.value == 0:
        await RisingEdge(dut.clock)
    
    print(f"Обработано {len(fpga_output)} выходных сэмплов")
    
    if len(reference_signal) > 0 and len(fpga_output) > 0:
        min_len = min(len(reference_signal), len(fpga_output))
        ref_slice = reference_signal[:min_len]
        fpga_slice = fpga_output[:min_len]
        
        error = np.array(ref_slice) - np.array(fpga_slice)
        rms_error = np.sqrt(np.mean(error**2))
        
        test_errors.append({
            'reference': ref_slice,
            'fpga_output': fpga_slice,
            'error': error,
            'rms_error': rms_error
        })
        
        print(f"RMS ошибка: {rms_error:.4f}")
        print(f"Максимальная ошибка: {np.max(np.abs(error)):.4f}")
        print(f"Средняя ошибка: {np.mean(error):.4f}")
        
        assert rms_error < 100, f"RMS ошибка слишком велика: {rms_error}"
        
        save_results(ref_slice, fpga_slice, error, rms_error)
        
        plot_results(ref_slice, fpga_slice, error, rms_error)
    else:
        print("Ошибка: нет данных для сравнения")

def save_results(reference, fpga_output, error, rms_error):
    os.makedirs('test_results', exist_ok=True)
    
    np.savetxt('test_results/reference.txt', reference, fmt='%d')
    np.savetxt('test_results/fpga_output.txt', fpga_output, fmt='%d')
    np.savetxt('test_results/error.txt', error, fmt='%d')
    
    with open('test_results/rms_stats.txt', 'w') as f:
        f.write(f"RMS ошибка: {rms_error:.4f}\n")
        f.write(f"Максимальная ошибка: {np.max(np.abs(error)):.4f}\n")
        f.write(f"Средняя ошибка: {np.mean(error):.4f}\n")
        f.write(f"Стандартное отклонение: {np.std(error):.4f}\n")
        f.write(f"Количество сэмплов: {len(reference)}\n")

def plot_results(reference, fpga_output, error, rms_error):
    plt.figure(figsize=(15, 10))
    
    plt.subplot(3, 1, 1)
    plt.plot(reference[:500], label='Эталонный сигнал', linewidth=1)
    plt.plot(fpga_output[:500], label='FPGA выход', linewidth=1, alpha=0.7)
    plt.title(f'Сравнение сигналов (первые 500 сэмплов)')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(3, 1, 2)
    plt.plot(error[:500], color='red', linewidth=1)
    plt.title(f'Ошибка (эталон - FPGA)')
    plt.grid(True)
    
    plt.subplot(3, 1, 3)
    plt.hist(error, bins=50, alpha=0.7, color='blue')
    plt.title(f'Распределение ошибки (RMS = {rms_error:.4f})')
    plt.xlabel('Ошибка')
    plt.ylabel('Частота')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('test_results/rms_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

@cocotb.test()
async def test_impulse_response(dut):
    
    clock = Clock(dut.clock, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    dut.reset.value = 1
    await RisingEdge(dut.clock)
    dut.reset.value = 0
    await RisingEdge(dut.clock)
    
    impulse = [32767] + [0] * 127  
    
    print("Тестируем импульсный отклик...")
    
    for i, sample in enumerate(impulse):
        dut.din.value = sample
        dut.din_valid.value = 1
        dut.din_last.value = 1 if i == len(impulse) - 1 else 0
        await RisingEdge(dut.clock)
    
    while dut.done.value == 0:
        await RisingEdge(dut.clock)
    
    print("Импульсный отклик завершен")

@cocotb.test()
async def test_noise_rejection(dut):
    
    clock = Clock(dut.clock, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    dut.reset.value = 1
    await RisingEdge(dut.clock)
    dut.reset.value = 0
    await RisingEdge(dut.clock)
    
    noise = np.random.randn(256) * 1000
    noise = np.clip(noise, -32768, 32767).astype(np.int16)
    
    print("Тестируем подавление шума...")
    
    for i, sample in enumerate(noise):
        dut.din.value = int(sample)
        dut.din_valid.value = 1
        dut.din_last.value = 1 if i == len(noise) - 1 else 0
        await RisingEdge(dut.clock)
    
    while dut.done.value == 0:
        await RisingEdge(dut.clock)
    
    print("Тест шума завершен")

if __name__ == "__main__":
    print("Запуск тестов cocotb для TopOverlapFFT128")
    print("Результаты будут сохранены в папке test_results/") 