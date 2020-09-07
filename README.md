# ItsDelayed
SkyWater 130nm digital delay line

32 Tap, ~70ps per tap

![Test Image 4](https://github.com/jonpry/ItsDelayed/blob/master/layout.png?raw=true)

## Usage

Compiled top-level GDS2 is foo.gds

To rebuild:

Make sure you have:  
  klayout w/ Python bindings  
  Magic w/ skywater tech file named sw130  
  ngspice  
  sky130 analog models  

Then:
./proc.py        <--- Builds cell and saves to foo.gds  
magic magic.tcl   <---- Performs LVS  
./procspice.py    <----  Funge the spice a little to make it work  
ngspice tb.spice   <---- Run the testbench, note you will need to modify the bench a little to point to your analog models   
