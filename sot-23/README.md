
SOT-23 breakouts
================

This directory contains kicad project files and camera-ready gerber files for SOT-23-6 and
SOT-23-8 breakout board PCBs.

Order PCBs
----------

Look in the `panelized/rtm/` directory and select the subdirectory with the highest
version number.  There are separate subdirectories in there for SOT-23-6 and SOT-23-8
breakout boards. Take all the files in one of those subdirectories (gerber files and
Excellon drill files) and zip them together. 

Order PCBs from jlcpcb.com:
* upload the zip file
* Set PCB Qty as you desire
* Panel By Customer
  * SOT-23-6: 10 cols, 6 rows
  * SOT-23-8: 7 cols, 6 rows
* Surface Finish: HASL (with lead) or LeadFree HASL as you desire
* All other options as-default.


To adjust board layouts
-----------------------

There is a source schematic which was used to create the sot-23 (6) and sot-23-8 kicad_pcb
files.  The schematic contains both breakouts; half of this was deleted on each PCB,
leaving each kicad_pcb file with a single sot-23-6 or sot-23-8 breakout. 

The panel PCBs in the `panelized/` subdirectory were derived from these using the KiKit
panelization plugin. JSON config files for each board are in the panelized/ directory and
can be imported into the KiKit configuration dialog to reproduce the same settings used to
generate the current panels.
