import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock
import random

@cocotb.test()
async def fft_basic_test(dut):
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
    
    for i in range(10):
        dut.addr_in.value = i
        dut.data_in_real.value = random.randint(0, 255)
        dut.data_in_imag.value = random.randint(0, 255)
        dut.start.value = 1
        await RisingEdge(dut.clk)
        dut.start.value = 0
        
        while dut.busy.value == 1:
            await RisingEdge(dut.clk)
        
        assert dut.valid_out.value == 1, f"Valid output not asserted at iteration {i}"
        print(f"Test {i}: addr_out={dut.addr_out.value}, data_out_real={dut.data_out_real.value}, data_out_imag={dut.data_out_imag.value}")

@cocotb.test()
async def fft_reset_test(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    dut.rst_n.value = 1
    dut.start.value = 0
    await Timer(50, units="ns")
    
    dut.rst_n.value = 0
    await Timer(100, units="ns")
    
    assert dut.busy.value == 0, "Busy should be 0 after reset"
    assert dut.valid_out.value == 0, "Valid should be 0 after reset" 