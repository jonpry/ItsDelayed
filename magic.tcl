tech load sw130
gds read foo
load TOP
flatten foo
load foo
set SUB VSS
ext all
ext2sim label on
extresist all
ext2spice cthresh 0
ext2spice rthresh 0
ext2spice extresist on
ext2spice
load TOP
ext all
ext2spice lvs
ext2spice scale on
ext2spice extresist off
ext2spice hierarchy on
ext2spice cthresh 0
ext2spice

