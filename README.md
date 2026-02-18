
SMD breakout boards
===================

This repo contains Kicad projects and camera-ready gerber files for panelized SMD component breakout boards.
The design of these breakout boards emphasizes narrow breakouts that "waste" fewer rows of pins in breadboards,
at the expense of slightly longer breakout boards that "overhang"  some number of pins to the left or right
of the actual pin header. In most cases, breakout boards are nearly the same width as a comparable THT DIP
component, spanning the gap in the middle of a breadboard plus only a single extra row (beyond the two rows
necessary for the pin headers).

Panels are designed to fit within the 100x100 mm size for a JLCPCB economy "special price" build. In many
cases, the 5 panel minimum will still result in a supply of breakout boards that will last even ambitious
hobbyists a long while. If you require more, the low marginal cost of increasing to 10 or 20 panels likely 
outcompetes the cost of making larger panels that can be ordered at qty=5.

![SOIC breakout board panel PCB CAD drawing](https://github.com/kimballa/breakout-boards/blob/main/soic.png "SOIC breakout board panel")

Directory structure
-------------------

There are a few subdirectories that each contain one or more breakout boards:

* `soic` - Two panels with a mix of SOIC-8, -14, and -16 breakouts, and TSSOP-8, -14, and -16
  breakouts.
* `soic-dw` - A panel with a mix of "widebody" (Texas Instruments drawing "DW") SOIC-16 and
  SOIC-20 breakouts
* `sot-23` - Two panels of SOT-23-6 and SOT-23-8 breakouts
* `qfn-20` - A non-panelized QFN-20 breakout board
* `micromatch-20` - a separate (non-panelized) breakout for the MicroMaTcH 20 pin connector 

All panels were created with KiKit. Each "base" directory contains Kicad project and PCB layout(s)
for singleton breakout boards. Panelized PCBs are in a subdirectory called `out` or `panelized`.

* The SOT-23 breakout boards were made using the KiKit GUI from the plugin. To regenerate, load the JSON config
  file to load the appropriate settings, and identify the input kicad_pcb and target kicad_pcb files.
* The SOIC / TSSOP and SOIC-DW breakout boards were made using the KiKit API. Each directory has a script
  called `panelize.py`. Open a KiCad Command Line terminal and run `python panelize.py` in the directory.
  The output will be generated in the `out/` subdirectory. The same `panelize.py` script in the `soic` 
  directory is used for generating SOIC or TSSOP panel, but some settings at the top of the script must
  be edited to switch from one to the other.

Gerber files are available in the `rtm/` subdirectory of each subproject. If multiple subdirectories exist
within `rtm`, choose the highest-numbered version to get the latest Gerbers.

Ordering breakout panels
------------------------

Zip up the gerber (and .drl) files in a given rtm directory and upload it to JLCPCB.com. The panel size and "2 layers" 
should be auto-selected. Choose "panel by customer", input the number of unique designs in the board file
(3 for SOIC and TSSOP; 2 for SOIC-DW, 1 for SOT-23-6 and SOT-23-8), and the number of rows and columns.

You should also probably select "remove order number", and your choice of HASL or HASL Lead-free surface
finishing. (You could choose ENIG but it will be overkill, *unless you are ordering the QFN*, in which case
it is mandatory.)

The default number of each panel you order is 5; you can also dial this up as-needed. 


Assembly
--------

Arrange your SMT component on the board with pin 1 closest to the dot or triangular arrow mark on the board
in the SMT area. Tack down one pin with your soldering iron, then do the rest. Clip pin headers to length
and place them in the breadboard, then seat the breakout board on top. Solder from above, lightly pressing 
the board down onto the seating plane of the pin headers.  

Any 2.54mm-pitch pin headers will do, but if you're looking for a specific part to order, Amphenol ICC (FCI)
part number `68000-400HLF` is a quality cuttable pin header strip, orderable from Mouser, Digikey, and likely
many others. Order qty is the number of connected pins you'd like; I typically buy by the 500 or so.

Where possible, a "ground plane" is provided on many breakout boards. A separate 1.1mm hole is available
in the middle of the board. After attaching the chip and the pin headers, solder a short piece of jumper 
wire from the hole to the top of whichever pin indicates GND (likely the one in the front right corner, 
but not always; check your datasheet). 

