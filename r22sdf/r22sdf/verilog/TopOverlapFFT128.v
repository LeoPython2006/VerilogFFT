module TopOverlapFFT128 (
    input wire clock,
    input wire reset,
    input wire [15:0] din,
    input wire din_valid,
    input wire din_last, // сигнал конца входного потока
    output wire [15:0] dout_re,
    output wire [15:0] dout_im,
    output wire dout_valid,
    output wire done
);

    wire di_en;
    wire [15:0] di_re;
    wire [15:0] di_im;
    wire do_en;
    wire [15:0] do_re;
    wire [15:0] do_im;

    FFT128 fft_inst (
        .clock(clock),
        .reset(reset),
        .di_en(di_en),
        .di_re(di_re),
        .di_im(di_im),
        .do_en(do_en),
        .do_re(do_re),
        .do_im(do_im)
    );

    OverlapAdd128 overlap_inst (
        .clock(clock),
        .reset(reset),
        .din(din),
        .din_valid(din_valid),
        .din_last(din_last),
        .di_en(di_en),
        .di_re(di_re),
        .di_im(di_im),
        .do_en(do_en),
        .do_re(do_re),
        .do_im(do_im),
        .dout_re(dout_re),
        .dout_im(dout_im),
        .dout_valid(dout_valid),
        .done(done)
    );
endmodule 