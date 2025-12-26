//====================================================================
//        Copyright (c) 2025 Carsten Wulff Software, Norway
// ===================================================================
// Created       : wulff at 2025-11-23
// ===================================================================
//  The MIT License (MIT)
//
//  Permission is hereby granted, free of charge, to any person obtaining a copy
//  of this software and associated documentation files (the "Software"), to deal
//  in the Software without restriction, including without limitation the rights
//  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//  copies of the Software, and to permit persons to whom the Software is
//  furnished to do so, subject to the following conditions:
//
//  The above copyright notice and this permission notice shall be included in all
//  copies or substantial portions of the Software.
//
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//  SOFTWARE.
//
//====================================================================
`timescale 1 ns / 1 ps

module test;
   //- Clock period is set to 1/(32768 Hz) ns
   //- Most micro controllers will have a real time clock of this frequency
   int lfclk_period = 30517;

   //- Initialize
   logic rst_n = 0;
   logic lfClk = 0;
   logic ena = 0;
   logic [7:0] ui_in;

   //- Our real time clock
   always #(lfclk_period/2) lfClk = ~lfClk;



   //- Default temperature
   integer     temperature;
   wire        pwrupOsc;
   wire        clkOsc;

   //- Temperature sensor output
   `LELO_DESIGN  dut_ana (.PWRUP_1V8(pwrupOsc),
                          .VDD_1V8(1'b1),
                          .VSS(1'b0),
                          .OSC_TEMP_1V8(clkOsc)
                          //- Magic to feed the temperature into the verilog model
`ifdef ANA_TYPE_REAL
                          ,.temperature(temperature)
`endif
                          );



   parameter   WIDTH = 8;

   wire [7:0]  delta;
   wire [WIDTH-1:0]  cycles;
   wire [WIDTH-1:0] count;
   logic       start;
   wire        done;
   wire        resetCount;


   tempCounter  #(.WIDTH(WIDTH)) u1_count (.clk(clkOsc),
                                 .reset(resetCount),
                                 .count(count)
                                 );

   tempFsm #(.WIDTH(WIDTH)) u1_fsm  (.lfClk(lfClk),
                              .start(start),
                              .clkOsc(clkOsc),
                              .rst_n(rst_n),
                              .done(done),
                                     .resetCount(resetCount),
                              .pwrupOsc(pwrupOsc),
                                     .count(count),
                              .cycles(cycles)
                              );



   integer     file;
   initial
     begin
        //- Output a file that can be opened in GTKWave
        $dumpfile("tb.vcd");
        $dumpvars(0,test);

        //- Create a CSV file
        file = $fopen("tb.csv","w");
        $fwrite(file,"temperature,count\n");
        #10 start = 0;

        #10 rst_n = 1;
        #10 rst_n = 0;
        #10 rst_n = 1;

        #(lfclk_period*9) start = 1;
        #(lfclk_period) start = 0;

        //Wait for temperature sweep to continue
        for (temperature=-40;temperature<126;temperature++) begin
           @(posedge done)
             #(lfclk_period) start = 1;
             #(lfclk_period) start = 0;
             $fwrite(file,"%d,%d\n",temperature,cycles );
           $display("Temperature =%d",temperature);
        end

        #(lfclk_period*2) $stop;
     end
endmodule
