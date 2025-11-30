
module LELO_TEMP_ANA(
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
