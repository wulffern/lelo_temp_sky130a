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
`default_nettype none

module LELO_TEMP(
                     input wire  PWRUP_1V8,
                     input wire  VDD_1V8,
                     input wire  VSS,
                     output wire OSC_TEMP_1V8
`ifdef ANA_TYPE_REAL
                     ,input real temperature
`endif
                     );
   //- Define the clock
   logic                         oclk = 0;

   assign OSC_TEMP_1V8 = PWRUP_1V8 &oclk;

   //- Pre-calcualted k/q
   real                          k_q = 8.61733e-5;
   real                          deltaV,id,vd;

   //- Resistance
   real                          rd = 70e3;
   real                          res_temp = rd;

   //- Capacitor to charge
   real                          cap = 100e-15;

   //- Delta time for output clock
   real                          dt = 1000;
   real                          to_ns = 1e9;

   //- Generate the output clock
   always begin
         //- Calculate diode voltage
         //- https://analogicus.com/aic2025/2024/10/25/Diodes.html
         vd = k_q*(273.15 + temperature)*(3 - 3 *$ln(273.15 + temperature)) + 1.12;

         //- Calculate the delta voltage across the resistance
         deltaV = k_q*(273.15 + temperature)*$ln(8);

         //Model temperture dependent resistance
         res_temp = (rd + (273.15 + temperature)/300*rd/20);

         //- Calculate the time to reach the diode voltage
         id = deltaV/res_temp;

         dt = cap*vd/id*to_ns;

         #(dt) oclk = ~oclk;
   end

endmodule // LELO_TEMP_ANA
