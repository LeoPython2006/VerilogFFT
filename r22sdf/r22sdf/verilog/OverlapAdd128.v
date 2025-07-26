module OverlapAdd128 #(
    parameter N = 128,
    parameter OVERLAP = 64,
    parameter DATA_WIDTH = 16
)(
    input wire clock,
    input wire reset,
    input wire [DATA_WIDTH-1:0] din,
    input wire din_valid,
    input wire din_last, // сигнал конца входного потока
    output reg di_en,
    output reg [DATA_WIDTH-1:0] di_re,
    output reg [DATA_WIDTH-1:0] di_im,
    input wire do_en,
    input wire [DATA_WIDTH-1:0] do_re,
    input wire [DATA_WIDTH-1:0] do_im,
    output reg [DATA_WIDTH-1:0] dout_re,
    output reg [DATA_WIDTH-1:0] dout_im,
    output reg dout_valid,
    output reg done // сигнал "всё обработано"
);

    // Буфер для окна
    reg [DATA_WIDTH-1:0] buffer [0:N-1];
    reg [7:0] wr_ptr = 0;
    reg [7:0] sample_count = 0;
    reg [7:0] fft_ptr = 0;
    reg [7:0] out_ptr = 0;
    reg [1:0] state = 0; // 0: fill, 1: fft out, 2: wait fft, 3: output
    reg [DATA_WIDTH-1:0] overlap_re [0:OVERLAP-1];
    reg [DATA_WIDTH-1:0] overlap_im [0:OVERLAP-1];
    reg [7:0] overlap_ptr = 0;
    reg last_window = 0;
    reg [7:0] tail_zeros = 0;

    integer i;
    always @(posedge clock or posedge reset) begin
        if (reset) begin
            wr_ptr <= 0;
            sample_count <= 0;
            fft_ptr <= 0;
            out_ptr <= 0;
            state <= 0;
            di_en <= 0;
            di_re <= 0;
            di_im <= 0;
            dout_valid <= 0;
            done <= 0;
            last_window <= 0;
            tail_zeros <= 0;
            for (i = 0; i < N; i = i + 1) buffer[i] <= 0;
            for (i = 0; i < OVERLAP; i = i + 1) begin
                overlap_re[i] <= 0;
                overlap_im[i] <= 0;
            end
        end else begin
            di_en <= 0;
            dout_valid <= 0;
            done <= 0;

            case (state)
                0: begin // Fill buffer
                    if (din_valid) begin
                        buffer[wr_ptr] <= din;
                        wr_ptr <= wr_ptr + 1;
                        sample_count <= sample_count + 1;
                        if (wr_ptr == N-1) begin
                            state <= 1;
                            wr_ptr <= 0;
                            fft_ptr <= 0;
                            last_window <= din_last;
                            if (din_last) begin
                                tail_zeros <= 0;
                            end
                        end
                    end
                    // Если пришёл din_last, но окно не заполнено — дополняем нулями
                    if (din_last && wr_ptr != 0 && wr_ptr < N-1) begin
                        buffer[wr_ptr] <= 0;
                        wr_ptr <= wr_ptr + 1;
                        tail_zeros <= tail_zeros + 1;
                        if (wr_ptr == N-2) begin
                            state <= 1;
                            wr_ptr <= 0;
                            fft_ptr <= 0;
                            last_window <= 1;
                        end
                    end
                end
                1: begin // Output window to FFT
                    di_re <= buffer[fft_ptr];
                    di_im <= 0; // только вещественная часть
                    di_en <= 1;
                    fft_ptr <= fft_ptr + 1;
                    if (fft_ptr == N-1) begin
                        state <= 2;
                        fft_ptr <= 0;
                    end
                end
                2: begin // Wait FFT output
                    if (do_en) begin
                        // Overlap-Add: первые OVERLAP отсчётов складываем с overlap[]
                        if (out_ptr < OVERLAP) begin
                            dout_re <= do_re + overlap_re[out_ptr];
                            dout_im <= do_im + overlap_im[out_ptr];
                            overlap_re[out_ptr] <= 0;
                            overlap_im[out_ptr] <= 0;
                        end else begin
                            dout_re <= do_re;
                            dout_im <= do_im;
                        end
                        dout_valid <= 1;
                        // Сохраняем OVERLAP для следующего окна
                        if (out_ptr >= N-OVERLAP) begin
                            overlap_re[out_ptr - (N-OVERLAP)] <= do_re;
                            overlap_im[out_ptr - (N-OVERLAP)] <= do_im;
                        end
                        out_ptr <= out_ptr + 1;
                        if (out_ptr == N-1) begin
                            out_ptr <= 0;
                            // Если это был последний блок — завершить
                            if (last_window) begin
                                state <= 3;
                            end else begin
                                // Сдвигаем buffer: копируем OVERLAP последних отсчётов в начало
                                for (i = 0; i < OVERLAP; i = i + 1) buffer[i] <= buffer[N-OVERLAP+i];
                                wr_ptr <= OVERLAP;
                                sample_count <= OVERLAP;
                                state <= 0;
                            end
                        end
                    end
                end
                3: begin // Done
                    done <= 1;
                    // Остаёмся в этом состоянии
                end
            endcase
        end
    end
endmodule 