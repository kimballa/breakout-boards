
SOIC-DW (Wide) Breakouts
========================

Breakout boards for {16, 20}-pin wide-body SOIC (1.27mm pitch) ICs that fit in standard pin
alignment on a breadboard.

The IC itself sits to the side of the pin headers rather than between them, to achieve a
narrow breakout board profile (12.8mm) that straddles only one extra row of pins on one
or the other side of the breadboard centerline.

A separate through-hole exists in the SOIC-16 board, connected to the ground plane. Solder a
resistor leg or other thin wire from the `GND` hole to top of the header pin that
represents ground for the IC. (Or leave floating if there is no appropriate ground pin for
the IC.)

The file name (SOIC-DW) derives from Texas Instruments' name for the wide SOIC package type.

## Gerber files

The latest gerber files for submitting to a board fab are in the `rtm/` directory.

If submitting to JLCPCB, select 'panel by customer', 'number of designs' = 2.

## Panelization

The main project file includes one of each representative breakout board. Panels with 8x
SOIC-16 and 6x SOIC-20 format were generated using KiKit. If you change the main PCB
CAD file, you should then open a KiCad Command Prompt in this directory and run `python
panelize.py`. You can edit `panelize.py` first to set variables related to the output file
to generate.

### Script notes:

The current layout is intended to fit in the 100x100 mm area that offers the best
deal for JLCPCB, but you can extend taller or wider if desired.
