# Panelization script for SOIC-DW breakouts
#
# 0. Finish updating the main PCB.
# 1. Edit the parameters in the 'configuration section' at the top of this file
# 2. Open a KiCad Command Prompt to this dir
# 3. Run `python panelize.py`. This will write to the output file (out\soic.kicad_pcb)
#    which you can then open with `start pcbnew out\soic.kicad_pcb` to generate Gerbers.


from kikit.units import *
from kikit.panelize import Panel, extractSourceAreaByAnnotation, Origin
from pcbnewTransition.pcbnew import (LoadBoard, VECTOR2I, BOX2I)
from shapely.geometry import (LineString, box)

import os
import os.path
import sys

### CONFIGURATION SECTION ###
#
# Adjust these to make the script do what you want.

# File to read input boards from
IN_FILENAME="soic-dw.kicad_pcb"

# File to save to.
OUT_FILENAME = "out\\soic-dw-panel.kicad_pcb"

# Position of the (0, 0) board in the output drawing sheet
START_X = 50*mm
START_Y = 50*mm

# Pick one set.
SOIC_BOARD_REFS = ["B1","B2"]
BOARD_REFS = SOIC_BOARD_REFS

# Layout: 4 cols of B1 (2 rows each), then 3 cols of B2 (2 rows each)
B1_COLS = 4
B1_ROWS = 2
B2_COLS = 3
B2_ROWS = 2

TITLE = "SOIC-DW 16/20 breakout rev 1"

FOOTER = "JLCJLCJLCJLC"

# Airgap between columns
COL_SPACE = 2*mm

# Ht of top/bottom edge rails.
RAIL_THICKNESS = 5*mm

# mouse bite size config
BITE_WIDTH = 5*mm
BITE_DIA = 0.5*mm
BITE_SPACING = 0.7*mm
BITE_PROLONG = 2*mm
TAB_SIZE = 2*mm # height of mouse-bitten spacer between adj. boards

### End configuration section ###

print(f"Creating panel from board references: {BOARD_REFS}")

out_dir = os.path.dirname(OUT_FILENAME)
if out_dir:
	os.makedirs(out_dir, exist_ok=True)

panel = Panel(OUT_FILENAME)

# Determine the bounding boxes of the sub-boards we want to include.
board_in = pcbnew.LoadBoard(IN_FILENAME)

# src_areas are the bounding boxes of the subboards in the same order as BOARD_REFS.
src_areas = []
for ref in BOARD_REFS:
	area = extractSourceAreaByAnnotation(board_in, ref)
	src_areas.append(area)

# Bottom spacer for B1 so its bottom tabs reach the rail (derived from actual board heights)
b1_height = src_areas[0].GetHeight()
b2_height = src_areas[1].GetHeight()
B1_BOTTOM_SPACER = 2 * (b2_height - b1_height)

cur_col_x = START_X
cur_row_y = START_Y

next_col_x = -1
next_row_y = -1

def place_column(panel, ref, src_area, cur_col_x, cur_row_y_start, num_rows, c, bottom_spacer_height=0):
	"""Place num_rows of one board type in a column; returns (next_col_x, next_row_y)."""
	cur_row_y = cur_row_y_start
	next_col_x = -1
	for r in range(num_rows):
		print(f"Adding board {ref} col={c} row={r}")
		bb = panel.appendBoard(filename=IN_FILENAME,
			destination=pcbnew.VECTOR2I(cur_col_x, cur_row_y),
			sourceArea=src_area,
			origin=Origin.TopLeft,
			tolerance=2*mm)
		next_row_y = max(cur_row_y, bb.GetBottom())
		next_col_x = max(cur_col_x, bb.GetRight()) if next_col_x < 0 else max(next_col_x, bb.GetRight())

		board_ctr_x = int((bb.GetRight() - bb.GetLeft()) / 2 + bb.GetLeft())
		x1 = int(board_ctr_x - BITE_WIDTH/2)
		x2 = int(board_ctr_x + BITE_WIDTH/2)

		# Spacer tab and mouse bite below this board
		y1 = bb.GetBottom()
		y2 = bb.GetBottom() + TAB_SIZE
		panel.appendSubstrate(box(x1, y1, x2, y2))
		cut = LineString([[x1, int(bb.GetBottom() - BITE_DIA/4)], [x2, int(bb.GetBottom() - BITE_DIA/4)]])
		panel.makeMouseBites([cut], BITE_DIA, BITE_SPACING, prolongation=BITE_PROLONG)

		# For shorter board types (e.g. B1), add a big spacer below bottom row so tab reaches the bottom rail
		if r == num_rows - 1 and bottom_spacer_height > 0:
			panel.appendSubstrate(box(x1, y2, x2, int(y2 + bottom_spacer_height)))

		if r > 0:
			top_y = bb.GetTop()
			cut = LineString([[x1, int(top_y - 3 * BITE_DIA / 4)], [x2, int(top_y - 3 * BITE_DIA / 4)]])
			panel.makeMouseBites([cut], BITE_DIA, BITE_SPACING, prolongation=BITE_PROLONG)
		else:
			top_y = bb.GetTop()
			panel.appendSubstrate(box(x1, top_y - TAB_SIZE, x2, top_y))
			cut = LineString([[x1, int(top_y - 3 * BITE_DIA / 4)], [x2, int(top_y - 3 * BITE_DIA / 4)]])
			panel.makeMouseBites([cut], BITE_DIA, BITE_SPACING, prolongation=BITE_PROLONG)

		cur_row_y = next_row_y + TAB_SIZE
	return next_col_x, cur_row_y

# Block 1: 4 columns of B1 (SOIC-DW-16), 2 rows each; add bottom spacer so tabs reach rail
for c in range(B1_COLS):
	next_col_x, _ = place_column(panel, BOARD_REFS[0], src_areas[0], cur_col_x, START_Y, B1_ROWS, c, bottom_spacer_height=B1_BOTTOM_SPACER)
	cur_col_x = next_col_x + COL_SPACE

# Block 2: 3 columns of B2 (SOIC-DW-20), 2 rows each
for c in range(B2_COLS):
	next_col_x, _ = place_column(panel, BOARD_REFS[1], src_areas[1], cur_col_x, START_Y, B2_ROWS, c)
	cur_col_x = next_col_x + COL_SPACE


# Final polish
print("Finishing up...")

# If we just add the automatic rails directly, it gets confused about the board substrate
# chunks we added above the top-most row for mouse-bite purposes, and fuses them all together.
# Manually add a small full-width header above that.
final_x = cur_col_x - COL_SPACE # the iterator above left us positioned for a col we didn't render.
header_box = box(START_X, int(START_Y - TAB_SIZE - 0.5 * mm), final_x, START_Y - TAB_SIZE)
panel.appendSubstrate(header_box)

panel.makeRailsTb(thickness=RAIL_THICKNESS)

(panel_min_x, panel_min_y, panel_max_x, panel_max_y) = panel.panelBBox()
ctr_x = int((panel_max_x - panel_min_x) / 2 + panel_min_x)

panel.addCornerFiducials(fidCount=4, horizontalOffset=6*mm,
	verticalOffset=3.85*mm,
	copperDiameter=1*mm, openingDiameter=2*mm)
panel.addCornerTooling(holeCount=4,
	horizontalOffset=3*mm, verticalOffset=2.5*mm,
	diameter=2*mm)
panel.addMillFillets(millRadius=int(0.55*mm))


panel.addText(TITLE, VECTOR2I(ctr_x, int(panel_min_y + 2.5*mm)))
panel.addText(FOOTER, VECTOR2I(ctr_x, int(panel_max_y - 2.5*mm)),
	width=1*mm, height=1*mm, thickness=int(0.15*mm))


#panel.debugRenderBoundingBoxes()
#panel.debugRenderBackboneLines()
#panel.debugRenderPartitionLines()

# Commit the output
print(f"Saving output board: {OUT_FILENAME}")
panel.save(refillAllZones=True)

if panel.hasErrors():
	print("Error: the panel has recorded at least one error:\n")
	for err in panel.errors:
		print(err)

	sys.exit(1)

print("Finished!")







