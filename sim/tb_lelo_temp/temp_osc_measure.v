

module temp_osc_measure #(
                          parameter WIDTH = 10                // Counter resolution
                          )(
                            input wire               lfClk,  // 32.768 kHz reference
                            input wire               start,
                            input wire               clkOsc, // Temperature-dependent oscillator
                            input wire               rst_n,
                            output logic             done,
                            output logic             pwrupOsc,  // Enables analog osc (1 lfClk period)
                            output logic [WIDTH-1:0] cycles   // Measured cycles
                            );

   logic                                             reset;


   //- FSM
   parameter IDLE = 0, PWRUP = 1, PWRDWN = 2, CAPTURE = 3;
   logic [1:0] state;
   logic [1:0] next_state;

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
         reset <= 1;
         done <= 1;
         cycles <= 0;
      end
      else begin
         state <= next_state;
         case (state)
           IDLE: begin
              pwrupOsc <= 0;
              reset <= 1;
              done <= 1;
           end
           PWRUP: begin
              pwrupOsc <= 1;
              reset <= 0;
              done <= 0;
           end
           PWRDWN: begin
              pwrupOsc <= 0;
              reset <= 0;
              done <= 0;
           end
           CAPTURE: begin
              pwrupOsc <= 0;
              reset <= 0;
              cycles[WIDTH-1] <= ~ reg_count[WIDTH-1];
              cycles[WIDTH-2:0] <= reg_count[WIDTH-2:0];
              done <= 0;
           end
         endcase
      end
   end

endmodule
