module fft_basic_dut (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        start,
    input  wire [7:0]  data_in_real,
    input  wire [7:0]  data_in_imag,
    input  wire [9:0]  addr_in,
    output wire [7:0]  data_out_real,
    output wire [7:0]  data_out_imag,
    output wire [9:0]  addr_out,
    output wire        valid_out,
    output wire        busy
);

    reg [7:0] data_real [0:1023];
    reg [7:0] data_imag [0:1023];
    reg [9:0] addr_counter;
    reg valid_reg;
    reg busy_reg;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            addr_counter <= 0;
            valid_reg <= 0;
            busy_reg <= 0;
        end else begin
            if (start) begin
                busy_reg <= 1;
                addr_counter <= 0;
                valid_reg <= 0;
            end else if (busy_reg) begin
                if (addr_counter < 1023) begin
                    addr_counter <= addr_counter + 1;
                    valid_reg <= 1;
                end else begin
                    busy_reg <= 0;
                    valid_reg <= 0;
                end
            end
        end
    end

    always @(posedge clk) begin
        if (start) begin
            data_real[addr_in] <= data_in_real;
            data_imag[addr_in] <= data_in_imag;
        end
    end

    assign data_out_real = data_real[addr_counter];
    assign data_out_imag = data_imag[addr_counter];
    assign addr_out = addr_counter;
    assign valid_out = valid_reg;
    assign busy = busy_reg;

endmodule 