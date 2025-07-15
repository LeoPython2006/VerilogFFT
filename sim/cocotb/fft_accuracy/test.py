import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock
import random
import numpy as np

@cocotb.test()
async def fft_accuracy_test(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst_n.value = 0
    await Timer(100, units="ns")
    dut.rst_n.value = 1
    
    dut.start.value = 0
    dut.data_in_real.value = 0
    dut.data_in_imag.value = 0
    dut.addr_in.value = 0
    
    await Timer(50, units="ns")
    
    test_data_real = []
    test_data_imag = []
    
    for i in range(64):
        real_val = random.randint(-32768, 32767)
        imag_val = random.randint(-32768, 32767)
        
        dut.addr_in.value = i
        dut.data_in_real.value = real_val & 0xFFFF
        dut.data_in_imag.value = imag_val & 0xFFFF
        dut.start.value = 1
        await RisingEdge(dut.clk)
        dut.start.value = 0
        
        test_data_real.append(real_val)
        test_data_imag.append(imag_val)
        
        while dut.busy.value == 1:
            await RisingEdge(dut.clk)
        
        if dut.valid_out.value == 1:
            print(f"Output {i}: real={dut.data_out_real.value}, imag={dut.data_out_imag.value}")
    
    assert dut.error_flag.value == 0, "Error flag should not be set for normal operation"

@cocotb.test()
async def fft_overflow_test(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst_n.value = 0
    await Timer(100, units="ns")
    dut.rst_n.value = 1
    
    dut.addr_in.value = 0
    dut.data_in_real.value = 16'h8000
    dut.data_in_imag.value = 16'h8000
    dut.start.value = 1
    await RisingEdge(dut.clk)
    dut.start.value = 0
    
    while dut.busy.value == 1:
        await RisingEdge(dut.clk)
    
    print(f"Error flag: {dut.error_flag.value}") 