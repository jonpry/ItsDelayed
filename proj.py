#!/usr/bin/python3

import klayout.db as db
import klayout.lib

layout = db.Layout()
layout.dbu = .001

layers = { "m1" : layout.layer(68,20), "m1.con" : layout.layer(67,44),
           "m1.pin" : layout.layer(68,16), "m1.label" : layout.layer(68,5),
           "li" : layout.layer(67,20),
           "li.pin" : layout.layer(67,16), "li.label" : layout.layer(67,5),
           "li.con" : layout.layer(66,44),
           "poly" : layout.layer(66,20),
           "npc" : layout.layer(95,20)}


def make_rect(cell,org,sz,layer):
   r = db.DBox.new(org[0],org[1],org[0]+sz[0],org[1]+sz[1]).to_itype(0.001)
   r = cell.shapes(layers[layer]).insert(r)

def make_pin(cell,org,layer,label):
   make_rect(cell,org,[.17,.17],layer)
   make_rect(cell,org,[.17,.17],layer + ".pin")
   region = db.DText.new(label,org[0] + .085,org[1] + .085)
   cell.shapes(layers[layer + ".label"]).insert(region)



gen = db.TextGenerator()
gen.default_generator()

src = db.Layout()
src.read("scs8hs.gds")

cells = {}
for i in src.top_cell().each_inst():
   i = src.cell(i.cell_index)
   cells[i.name] = i

scs8hs_tap_1 = layout.create_cell("scs8hs_tapvpwrvgnd_1")
scs8hs_tap_1.copy_tree(cells["scs8hs_tapvpwrvgnd_1"])

scs8hs_inv_1 = layout.create_cell("scs8hs_inv_1")
scs8hs_inv_1.copy_tree(cells["scs8hs_inv_1"])

scs8hs_fill_4 = layout.create_cell("scs8hs_fill_4")
scs8hs_fill_4.copy_tree(cells["scs8hs_fill_4"])

pfet_small = layout.create_cell("pfet_small")
src = db.Layout()
src.read("pfet_small.gds")
pfet_small.copy_tree(src.top_cell())

nfet_small = layout.create_cell("nfet_small")
src = db.Layout()
src.read("nfet_small.gds")
nfet_small.copy_tree(src.top_cell())

scs8hs_buf_1 = layout.create_cell("scs8hs_buf_1")
src = db.Layout()
src.read("scs8hs_buf_1.gds")
scs8hs_buf_1.copy_tree(src.top_cell())

scs8hs_fill_1 = layout.create_cell("scs8hs_fill_1")
src = db.Layout()
src.read("scs8hs_fill_1.gds")
scs8hs_fill_1.copy_tree(src.top_cell())


scs8hs_inv_1_mod = layout.create_cell("scs8hs_inv_1_mod")
src = db.Layout()
src.read("scs8hs_inv_1_mod.gds")
scs8hs_inv_1_mod.copy_tree(src.top_cell())

scs8hs_fill_4_none = layout.create_cell("scs8hs_fill_4_none")
src = db.Layout()
src.read("scs8hs_fill_4_none.gds")
scs8hs_fill_4_none.copy_tree(src.top_cell())


scs8hs_tap_1 = layout.create_cell("scs8hs_tapvpwrvgnd_1")
src = db.Layout()
src.read("scs8hs_tapvpwrvgnd_1.gds")
scs8hs_tap_1.copy_tree(src.top_cell())

top = layout.create_cell("TOP")

dcell = db.DCellInstArray.new(scs8hs_tap_1.cell_index(),db.DTrans.R0)
dcell.trans = db.DTrans.new(0,False,-.48*2,0) * dcell.trans
top.insert(dcell)

dcell = db.DCellInstArray.new(scs8hs_tap_1.cell_index(),db.DTrans.M0)
dcell.trans = db.DTrans.new(0,False,-.48*2,6.745 - .085) * dcell.trans
top.insert(dcell)


#dcell = db.DCellInstArray.new(scs8hs_fill_4.cell_index(),db.DTrans.R0)
#dcell.trans = db.DTrans.new(0,False,0.48*7,0) * dcell.trans
#top.insert(dcell)

pcap = layout.create_cell("pcap")

dcell = db.DCellInstArray.new(pfet_small.cell_index(),db.DTrans.R0)
dcell.trans = db.DTrans.new(0,False,.48,1.845+.15) * dcell.trans
pcap.insert(dcell)

dcell = db.DCellInstArray.new(nfet_small.cell_index(),db.DTrans.M0)
dcell.trans = db.DTrans.new(0,False,0.48,0.960) * dcell.trans
pcap.insert(dcell)


dcell = db.DCellInstArray.new(scs8hs_fill_4_none.cell_index(),db.DTrans.R0)
dcell.trans = db.DTrans.new(0,False,-0.48,0) * dcell.trans
pcap.insert(dcell)

make_rect(pcap,[0.255,0.370],[0.17,2.6],"li")
make_rect(pcap,[0.255+.430,0.370],[0.17,2.6],"li")
make_rect(pcap,[0.255+.430*2,0.370],[0.17,3.6],"li")
make_rect(pcap,[0-.35,2.6],[0.17,2.4],"li")
#make_rect(pcap,[0-.13,3.6],[0.17,1],"li")
make_rect(pcap,[0-.3,2.6],[0.56,.3],"li")

make_rect(pcap,[-.54+.095+1.355,1.240-.115-.08],[1.17-.095+.03-.3,0.15],"poly")
make_rect(pcap,[-.54+.095-.03+.34,1.240+.325+.2],[1.17-.095+.03-.34,0.15],"poly")

make_rect(pcap,[-.54+.095+.925,1.240-.115+.28],[0.580,0.15],"poly")
make_rect(pcap,[-.54+.095+1.355,1.240-.115+.3],[0.15,0.48],"poly")
make_rect(pcap,[-.54+.095+.925,1.240-.115+.28],[0.15,-0.3],"poly")
make_rect(pcap,[-.54+.095+.27,1.240-.115-.08],[1.17-.095-.27,0.15],"poly")

make_rect(pcap,[-.54+.095-.03+.29,1.240+.275+.25],[0.33,0.35],"poly")
make_rect(pcap,[-.54+.095+1.73+.1,1.195],[0.34,0.90],"poly")
make_rect(pcap,[-.54+.095-.03+.29,1.195],[0.33,0.35],"poly")

make_rect(pcap,[-.54+.095-.03+.30-.1,1.240+.275+.25-.82],[0.33+.2,0.35+.92],"npc")

make_rect(pcap,[-.54+.095+1.73-.1+0.1,1.195-.25],[0.7+.2-.37,0.25+.35+.65],"npc")

make_rect(pcap,[-.54+.095+.1+.17,1.240+.275+.25],[.25,.33],"li")
make_rect(pcap,[-.54+.095+.1+.25-.035,1.240+.275+.33],[.17,.17],"li.con")
make_rect(pcap,[-.54+.095+.1+.17,1.240+.275+.25],[.25,.33],"m1")
make_rect(pcap,[-.54+.095+.1+.25-.035,1.240+.275+.33],[.17,.17],"m1.con")

make_rect(pcap,[-.54+.095+.1+.17,1.195],[.25,.33],"li")
make_rect(pcap,[-.54+.095+.1+.25-.035,1.195+.08],[.17,.17],"li.con")
make_rect(pcap,[-.54+.095+.1+.17,1.195-.13],[.25,.33+.13],"m1")
make_rect(pcap,[-.54+.095+.1+.25-.035,1.195+.08],[.17,.17],"m1.con")

make_rect(pcap,[-.54+.095+1.73+.1+.08,1.240+.275+.25],[.25,.33],"li")
make_rect(pcap,[-.54+.095+1.73+.1+.12,1.240+.275+.33],[.17,.17],"li.con")
make_rect(pcap,[-.54+.095+1.73+.1+.08,1.240+.275+.25],[.25,.33],"m1")
make_rect(pcap,[-.54+.095+1.73+.1+.12,1.240+.275+.33],[.17,.17],"m1.con")

make_rect(pcap,[-.48,1.8],[.48*8,.20],"m1")
make_rect(pcap,[-.48,.96],[.48*8,.20],"m1")

make_rect(pcap,[0.255+.430-.06,1.390-.06],[0.29,0.29],"li")
make_rect(pcap,[0.255+.430-.06,1.390-.06],[0.29,0.29],"m1")
make_rect(pcap,[0.255+.430,1.390],[0.17,0.17],"m1.con")
make_rect(pcap,[0.255+.430,1.390],[1.7,0.17],"m1")
make_rect(pcap,[0.255+.430-.06+1.7,1.390-.06],[0.29,0.29],"m1")
make_rect(pcap,[0.255+.430+1.7,1.390],[0.17,0.17],"m1.con")

make_rect(pcap,[.48*3-.1,5-.12],[.25,.33],"li")

#make_rect(pcap,[-.54+.095+1.73+.17,1.195-.15],[0.7-.17,0.40],"li")

#make_rect(pcap,[-.54+.095+.02,1.240+.275+.12],[0.17,0.17],"li.con")
#make_rect(pcap,[-.54+.095+.36,1.240+.275+.12],[0.17,0.17],"li.con")

#make_rect(pcap,[-.54+.095+1.73-.1+.27,1.195-.25+.22],[0.17,0.17],"li.con")
#make_rect(pcap,[-.54+.095+1.73-.1+.27+.34,1.195-.25+.22],[0.17,0.17],"li.con")

#make_rect(pcap,[-.54+.095+.02,1.240+.275+.12],[0.17,0.17],"m1.con")
#make_rect(pcap,[-.54+.095+.36,1.240+.275+.12],[0.17,0.17],"m1.con")

#make_rect(pcap,[-.54+.095+1.73-.1+.27,1.195-.25+.22],[0.17,0.17],"m1.con")
#make_rect(pcap,[-.54+.095+1.73-.1+.27+.34,1.195-.25+.22],[0.17,0.17],"m1.con")

#make_rect(pcap,[-.54+.095-.05,1.240+.275],[0.7-.17+.1,0.40],"m1")
#make_rect(pcap,[-.54+.095+1.73+.17-.05,1.195-.15],[0.7-.17+.1,0.40],"m1")
#make_rect(pcap,[-.54+.095-.05,1.240+.275-.1],[2.53,0.17],"m1")

dcell = db.DCellInstArray.new(scs8hs_buf_1.cell_index(),db.DTrans.M0)
dcell.trans = db.DTrans.new(0,False,-0.48,6.745 - .085) * dcell.trans
pcap.insert(dcell)

dcell = db.DCellInstArray.new(scs8hs_buf_1.cell_index(),db.DTrans.M0)
dcell.trans = db.DTrans.new(0,False,0.48*3,6.745 - .085) * dcell.trans
pcap.insert(dcell)

dcell = db.DCellInstArray.new(scs8hs_inv_1_mod.cell_index(),db.DTrans.R0)
dcell.trans = db.DTrans.new(0,False,0.48*4,0) * dcell.trans
pcap.insert(dcell)

dcell = db.DCellInstArray.new(scs8hs_fill_1.cell_index(),db.DTrans.R0)
dcell.trans = db.DTrans.new(0,False,0.48*3,0) * dcell.trans
pcap.insert(dcell)



def make_pins(cell):
    make_pin(cell,[-.325,4.91],"li","IN")
    make_pin(cell,[3.035,4.54],"li","OUT")
    make_pin(cell,[3.035,1.21],"li","OUTD")

    make_pin(cell,[-0.13,1.845],"m1","S")
    make_pin(cell,[-0.13,1.275],"m1","SB")

    make_pin(cell,[0.155,-.085],"m1","VSS")
    make_pin(cell,[0.155,6.575],"m1","VSS")
    make_pin(cell,[0.155,3.245],"m1","VDD")

    make_pin(cell,[0.07,3.76],"li","TP1")
    make_pin(cell,[1.07,3.76],"li","TP2")


make_pins(pcap)

for i in range(8):
   dcell = db.DCellInstArray.new(pcap.cell_index(),db.DTrans.R0)
   dcell.trans = db.DTrans.new(0,False,8*i*.48,0) * dcell.trans
   top.insert(dcell)

make_pins(top)


#m1


#m1 pin


#li pin



#inst=db.CellInstArry

layout.write("foo.gds")