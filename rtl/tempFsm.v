//====================================================================
//        Copyright (c) 2025 Carsten Wulff Software, Norway
// ===================================================================
// Created       : wulff at 2025-12-26
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


module tempFsm #(
                 parameter WIDTH = 10                // Counter resolution
                 )(
                   input wire               lfClk, // 32.768 kHz reference
                   input wire               start,
                   input wire               clkOsc, // Temperature-dependent oscillator
                   input wire               rst_n,
                   input wire [WIDTH-1:0]   count,
                   output logic             resetCount,
                   output logic             done,
                   output logic             pwrupOsc, // Enables analog osc (1 lfClk period)
                   output logic [WIDTH-1:0] cycles   // Measured cycles
                   );

   //- FSM
   parameter                                IDLE = 0, PWRUP = 1, PWRDWN = 2, CAPTURE = 3;
   logic [1:0]                              state;
   logic [1:0]                              next_state;

   //- Decide next state
   always_comb begin
      case (state)
        IDLE: next_state = start ? PWRUP : IDLE;
        PWRUP: next_state = PWRDWN ;
        PWRDWN: next_state = CAPTURE;
        CAPTURE: next_state = IDLE;
        default: next_state = IDLE;
      endcase // case (state)
   end


   //- Control signals
   always_ff @(posedge lfClk or negedge rst_n) begin
      if(~rst_n) begin
         state <= IDLE;
         pwrupOsc <= 0;
         resetCount <= 1;
         done <= 1;
         cycles <= 0;
      end
      else begin
         state <= next_state;
         case (state)
           IDLE: begin
              pwrupOsc <= 0;
              resetCount <= 1;
              done <= 1;
           end
           PWRUP: begin
              pwrupOsc <= 1;
              resetCount <= 0;
              done <= 0;
           end
           PWRDWN: begin
              pwrupOsc <= 0;
              resetCount <= 0;
              done <= 0;
           end
           CAPTURE: begin
              pwrupOsc <= 0;
              resetCount <= 0;
              cycles <= count ;
              done <= 0;
           end
         endcase
      end
   end

endmodule
