#!/usr/bin/python3

import klayout.db as db
import klayout.lib

layout = db.Layout()
layout.dbu = .001

layers = { "m1" : layout.layer(68,20), "m1.con" : layout.layer(67,44),
           "m1.pin" : layout.layer(68,16), "m1.label" : layout.layer(68,5),

           "m2" : layout.layer(69,20), "m2.con" : layout.layer(68,44),
           "m2.pin" : layout.layer(69,16), "m2.label" : layout.layer(69,5),
          
           "li" : layout.layer(67,20),
           "li.pin" : layout.layer(67,16), "li.label" : layout.layer(67,5),
           "li.con" : layout.layer(66,44),
           "poly" : layout.layer(66,20),
           "npc" : layout.layer(95,20)}


def make_rect(cell,org,sz,layer):
   if isinstance(layer,list):
      for l in layer:
         make_rect(cell,org,sz,l)
      return
   r = db.DBox.new(org[0],org[1],org[0]+sz[0],org[1]+sz[1]).to_itype(0.001)
   r = cell.shapes(layers[layer]).insert(r)

def make_pin(cell,org,layer,label):
   if isinstance(cell,list):
      for e in cell:
         make_pin(e,org,layer,label)
      return
   make_rect(cell,org,[.17,.17],layer)
   make_rect(cell,org,[.17,.17],layer + ".pin")
   region = db.DText.new(label,org[0] + .085,org[1] + .085)
   region.height = 1
   cell.shapes(layers[layer + ".label"]).insert(region)

def make_bone(cell,org,length,layer,vert=False,ps=.33,ol=None,two_sided=True):
   if vert:
      make_rect(cell,[org[0]-.085,org[1]-.085],[.17,.17],layer+".con")
      if two_sided:
         make_rect(cell,[org[0]-.085,org[1]-.085+length],[.17,.17],layer+".con")
         make_rect(cell,[org[0]-.085 - (ps - .17)/2,org[1]-.085-(ps - .17)/2+length],[ps,ps],layer)
      make_rect(cell,[org[0]-.085 - (ps - .17)/2,org[1]-.085-(ps - .17)/2],[ps,ps],layer)
      if ol:
         make_rect(cell,[org[0]-.085 - (ps - .17)/2,org[1]-.085-(ps - .17)/2],[ps,ps],ol)
         if two_sided:
            make_rect(cell,[org[0]-.085 - (ps - .17)/2,org[1]-.085-(ps - .17)/2+length],[ps,ps],ol)
      make_rect(cell,[org[0]-.095,org[1]-.085],[.17,length],layer)
   else:
      make_rect(cell,[org[0]-.085,org[1]-.085],[.17,.17],layer+".con")
      if two_sided:
         make_rect(cell,[org[0]-.085+length,org[1]-.085],[.17,.17],layer+".con")
         make_rect(cell,[org[0]-.085-(ps - .17)/2+length,org[1]-.085-(ps - .17)/2],[ps,ps],layer)
      make_rect(cell,[org[0]-.085-(ps - .17)/2,org[1]-.085-(ps - .17)/2],[ps,ps],layer)
      make_rect(cell,[org[0]-.095,org[1]-.085],[length,.17],layer)
      if ol:
         make_rect(cell,[org[0]-.085 - (ps - .17)/2,org[1]-.085-(ps - .17)/2],[ps,ps],ol)
         if two_sided:
            make_rect(cell,[org[0]-.085 - (ps - .17)/2+length,org[1]-.085-(ps - .17)/2],[ps,ps],ol)



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

scs8hs_buf_2= layout.create_cell("scs8hs_buf_2")
src = db.Layout()
src.read("scs8hs_buf_2.gds")
scs8hs_buf_2.copy_tree(src.top_cell())

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
eight_delay = layout.create_cell("eight_delay")
unit_delay = layout.create_cell("unit_delay")
quad_delay = layout.create_cell("quad_delay")

dcell = db.DCellInstArray.new(scs8hs_tap_1.cell_index(),db.DTrans.R0)
dcell.trans = db.DTrans.new(0,False,-.48*2,0) * dcell.trans
quad_delay.insert(dcell)

dcell = db.DCellInstArray.new(scs8hs_tap_1.cell_index(),db.DTrans.M0)
dcell.trans = db.DTrans.new(0,False,-.48*2,0) * dcell.trans
quad_delay.insert(dcell)

dcell = db.DCellInstArray.new(scs8hs_tap_1.cell_index(),db.DTrans.M0)
dcell.trans = db.DTrans.new(0,False,-.48*2,6.745 - .085) * dcell.trans
quad_delay.insert(dcell)


#dcell = db.DCellInstArray.new(scs8hs_fill_4.cell_index(),db.DTrans.R0)
#dcell.trans = db.DTrans.new(0,False,0.48*7,0) * dcell.trans
#top.insert(dcell)


emux = layout.create_cell("emux")

dcell = db.DCellInstArray.new(pfet_small.cell_index(),db.DTrans.R0)
dcell.trans = db.DTrans.new(0,False,.48,1.845+.15) * dcell.trans
emux.insert(dcell)

dcell = db.DCellInstArray.new(nfet_small.cell_index(),db.DTrans.M0)
dcell.trans = db.DTrans.new(0,False,0.48,0.960) * dcell.trans
emux.insert(dcell)


dcell = db.DCellInstArray.new(scs8hs_fill_4_none.cell_index(),db.DTrans.R0)
dcell.trans = db.DTrans.new(0,False,-0.48,0) * dcell.trans
emux.insert(dcell)

make_rect(emux,[0.255,0.370],[0.17,2.6],"li")
make_rect(emux,[0.255+.430,0.370],[0.17,2.6],"li")
make_rect(emux,[0.255+.430*2,0.370],[0.17,2.6],"li")
#make_rect(unit_delay,[0.255+.430*2,0.370+2.6],[0.17,1],"li")
#make_rect(unit_delay,[0-.35,2.6],[0.17,2.4],"li")
#make_rect(unit_delay,[0-.3,2.6],[0.56,.3],"li")


make_rect(unit_delay,[-.025,2.69],[0.15,1],"poly")
make_rect(unit_delay,[-.025-.18,2.69],[0.18,.33],"poly")
make_rect(unit_delay,[-.025-.18+.07,2.69+.08],[0.17,.17],"li.con")
make_rect(unit_delay,[-.025-.18,2.69],[0.6,.33],"li")

make_rect(unit_delay,[-.025-.18+2.23,3.69-.15],[0.5,.15],"poly")
make_rect(unit_delay,[-.025-.18+2.23,3.69-.15],[0.15,-.85],"poly")
make_rect(unit_delay,[-.025-.18+2.23-.18,2.69],[0.18,.33],"poly")
make_rect(unit_delay,[-.025-.18+2.23-.18+.08,2.69+.08],[0.17,.17],"li.con")
make_rect(unit_delay,[-.025-.18+2.23-.18+.33,2.69],[-.9,.33],"li")


make_rect(emux,[-.54+.095+1.355,1.240-.115-.08],[1.17-.095+.03-.3,0.15],"poly")
make_rect(emux,[-.54+.095-.03+.34,1.240+.325+.2],[1.17-.095+.03-.34,0.15],"poly")

make_rect(emux,[-.54+.095+.925,1.240-.115+.28],[0.580,0.15],"poly")
make_rect(emux,[-.54+.095+1.355,1.240-.115+.3],[0.15,0.48],"poly")
make_rect(emux,[-.54+.095+.925,1.240-.115+.28],[0.15,-0.3],"poly")
make_rect(emux,[-.54+.095+.27,1.240-.115-.08],[1.17-.095-.27,0.15],"poly")

make_rect(emux,[-.54+.095-.03+.29,1.240+.275+.25],[0.33,0.35],"poly")
make_rect(emux,[-.54+.095+1.73+.1,1.195],[0.34,0.90],"poly")
make_rect(emux,[-.54+.095-.03+.29,1.195],[0.33,0.35],"poly")

make_rect(emux,[-.54+.095-.03+.30-.1,1.240+.275+.25-.82],[0.33+.2,0.35+.92+.95],"npc")

make_rect(emux,[-.54+.095+1.73-.1+0.1,1.195-.25],[0.7+.2-.37,0.25+.35+.65],"npc")
make_rect(emux,[-.54+.095+1.73-.1+0.5,1.195-.25+1],[0.7+.2-.37,0.25+.35+.65],"npc")

make_rect(emux,[-.54+.095+.1+.17,1.240+.275+.25],[.25,.33],"li")
make_rect(emux,[-.54+.095+.1+.25-.035,1.240+.275+.33],[.17,.17],"li.con")
make_rect(emux,[-.54+.095+.1+.17,1.240+.275+.25],[.25,.33],"m1")
make_rect(emux,[-.54+.095+.1+.25-.035,1.240+.275+.33],[.17,.17],"m1.con")

make_rect(emux,[-.54+.095+.1+.17-.03,1.195],[.27,.37],"li")
make_rect(emux,[-.54+.095+.1+.25-.035,1.195+.08],[.17,.17],"li.con")
make_rect(emux,[-.54+.095+.1+.17-.05,1.195+.13-.07],[.32,.32],"m1")
make_rect(emux,[-.54+.095+.1+.25-.05,1.195+.13],[.17,.17],"m1.con")


make_rect(emux,[-.54+.095+1.73+.1+.08,1.240+.275+.25],[.25,.33],"li")
make_rect(emux,[-.54+.095+1.73+.1+.12,1.240+.275+.33],[.17,.17],"li.con")
make_rect(emux,[-.54+.095+1.73+.1+.08,1.240+.275+.25],[.25,.33],"m1")
make_rect(emux,[-.54+.095+1.73+.1+.12,1.240+.275+.33],[.17,.17],"m1.con")

make_rect(emux,[0,1.8],[1.7,.20],"m1")
#make_rect(emux,[-.48,.96],[.48*10,.20],"m1")

make_rect(emux,[0.255+.430-.06,1.390-.06],[0.29,0.29],"li")
make_rect(emux,[0.255+.430-.06,1.390-.06],[0.29,0.29],"m1")
make_rect(emux,[0.255+.430,1.390],[0.17,0.17],"m1.con")
make_rect(emux,[0.255+.430,1.390],[1.7,0.17],"m1")
make_rect(emux,[0.255+.430-.06+1.7,1.390-.06],[0.29,0.29],"m1")
make_rect(emux,[0.255+.430+1.7,1.390],[0.17,0.17],"m1.con")

#make_rect(emux,[-.54+.095+1.73+.17,1.195-.15],[0.7-.17,0.40],"li")

#make_rect(emux,[-.54+.095+.02,1.240+.275+.12],[0.17,0.17],"li.con")
#make_rect(emux,[-.54+.095+.36,1.240+.275+.12],[0.17,0.17],"li.con")

#make_rect(emux,[-.54+.095+1.73-.1+.27,1.195-.25+.22],[0.17,0.17],"li.con")
#make_rect(emux,[-.54+.095+1.73-.1+.27+.34,1.195-.25+.22],[0.17,0.17],"li.con")

#make_rect(emux,[-.54+.095+.02,1.240+.275+.12],[0.17,0.17],"m1.con")
#make_rect(emux,[-.54+.095+.36,1.240+.275+.12],[0.17,0.17],"m1.con")

#make_rect(emux,[-.54+.095+1.73-.1+.27,1.195-.25+.22],[0.17,0.17],"m1.con")
#make_rect(emux,[-.54+.095+1.73-.1+.27+.34,1.195-.25+.22],[0.17,0.17],"m1.con")

#make_rect(emux,[-.54+.095-.05,1.240+.275],[0.7-.17+.1,0.40],"m1")
#make_rect(emux,[-.54+.095+1.73+.17-.05,1.195-.15],[0.7-.17+.1,0.40],"m1")
#make_rect(emux,[-.54+.095-.05,1.240+.275-.1],[2.53,0.17],"m1")

dcell = db.DCellInstArray.new(scs8hs_buf_2.cell_index(),db.DTrans.R180)
dcell.trans = db.DTrans.new(0,False,0.48*4,6.745 - .085) * dcell.trans
unit_delay.insert(dcell)

dcell = db.DCellInstArray.new(scs8hs_buf_2.cell_index(),db.DTrans.R180)
dcell.trans = db.DTrans.new(0,False,0.48*9,6.745 - .085) * dcell.trans
unit_delay.insert(dcell)

dcell = db.DCellInstArray.new(scs8hs_inv_1_mod.cell_index(),db.DTrans.R0)
dcell.trans = db.DTrans.new(0,False,0.48*4,0) * dcell.trans
emux.insert(dcell)

dcell = db.DCellInstArray.new(scs8hs_fill_1.cell_index(),db.DTrans.R0)
dcell.trans = db.DTrans.new(0,False,0.48*3,0) * dcell.trans
emux.insert(dcell)

dcell = db.DCellInstArray.new(scs8hs_fill_1.cell_index(),db.DTrans.R0)
dcell.trans = db.DTrans.new(0,False,0.48*8,0) * dcell.trans
emux.insert(dcell)

dcell = db.DCellInstArray.new(scs8hs_fill_1.cell_index(),db.DTrans.R0)
dcell.trans = db.DTrans.new(0,False,0.48*7,0) * dcell.trans
emux.insert(dcell)


dcell = db.DCellInstArray.new(emux.cell_index(),db.DTrans.R0)
dcell.trans = db.DTrans.new(0,False,0,0) * dcell.trans
unit_delay.insert(dcell)


def make_pins(cell,x=True):
    make_pin(cell,[3.035,1.21],"li","OUTD")

    make_pin(cell,[-0.13,1.845],"m1","S")
    make_pin(cell,[-0.145,1.325],"m1","SB")

    make_pin(cell,[0.155,-.085],"m1","VSS")
    make_pin(cell,[0.155,3.245],"m1","VDD")

    if x:
       make_pin(cell,[-.325,4.91],"li","IN")
       make_pin(cell,[3.035,4.54],"li","OUT")
       make_pin(cell,[0.155,6.575],"m1","VSS")
#       make_pin(cell,[0.07,3.76],"li","TP1")
#       make_pin(cell,[1.07,3.76],"li","TP2")


make_pins(unit_delay)
make_pins(quad_delay)
make_pins(eight_delay)
make_pins(top)
make_pins(emux,False)


make_pin(top,[0.155,9.905],"m1","VDD")
make_pin(top,[0.155,13.235],"m1","VSS")
make_pin(top,[0.155,16.565],"m1","VDD")


make_rect(quad_delay,[-.96,1.8],[.48*42,.20],"m1")
make_rect(quad_delay,[-.96,.96],[.48*42,.20],"m1")

make_rect(quad_delay,[-.96,-1.08],[.48*42,.17],"m1")
make_rect(quad_delay,[-.96,-2.435],[.48*42,.17],"m1")


for i in range(7):
   make_pin(quad_delay,[i*.48*5 + 1.115-.43,1.08+.47+.08+3.4],"m1","OUT" + str(i))
   make_rect(quad_delay,[i*.48*5 + 1.115-.43,.47+1.08+.08+3.4],[.17,.17],"m1.con")
   make_rect(quad_delay,[i*.48*5 + 2.555-.43,1.58+3.4],[.17,.17],"m1.con")
   make_rect(quad_delay,[i*.48*5 + 1.115-.43-.08,.47+1.08+3.4],[.33,.33],"m1")
   make_rect(quad_delay,[i*.48*5 + 2.555-.43-.08,1.58-.08+3.4],[.33,.33],"m1")
   make_rect(quad_delay,[i*.48*5 + 1.115-.43,.47+1.08+3.4],[1.57,.17],"m1")


make_pin(eight_delay,[7*.48*5 + 1.115-.43,1.08+.47+.08+3.4],"m1","OUT" + str(7))
make_rect(eight_delay,[7*.48*5 + 1.115-.43,.47+1.08+.08+3.4],[.17,.17],"m1.con")
make_rect(eight_delay,[7*.48*5 + 2.555-.43+.48,1.58+3.4],[.17,.17],"m1.con")
make_rect(eight_delay,[7*.48*5 + 1.115-.43-.08,.47+1.08+3.4],[.33,.33],"m1")
make_rect(eight_delay,[7*.48*5 + 2.555-.43-.08+.48,1.58-.08+3.4],[.33,.33],"m1")
make_rect(eight_delay,[7*.48*5 + 1.115-.43,.47+1.08+3.4],[1.57+.48,.17],"m1")


make_bone(eight_delay,[7*.48*4-.48*1-.23,-2.77],7.33,"m1")
make_bone(eight_delay,[7*.48*4-.48*1-.23+8.11,-2.77],11.50,"m1")

make_rect(eight_delay,[7*.48*5 + 1.115-.43,.47+1.08+.08+3.4],[.17,.17],"m1.con")
make_rect(eight_delay,[7*.48*5 + 2.555-.43+.48,1.58+3.4],[.17,.17],"m1.con")
make_rect(eight_delay,[7*.48*5 + 1.115-.43-.08,.47+1.08+3.4],[.33,.33],"m1")
make_rect(eight_delay,[7*.48*5 + 2.555-.43-.08+.48,1.58-.08+3.4],[.33,.33],"m1")
make_rect(eight_delay,[7*.48*5 + 1.115-.43,.47+1.08+3.4],[1.57+.48,.17],"m1")

make_rect(eight_delay,[6.875+.48*2+.48*31,-1.38-.37],[.17,.17],["m1.con","m2.con"])
make_rect(eight_delay,[6.875+.48*2+.48*31-.09,-1.38-.37-.09],[.35,.35],["m1","m2"])
make_rect(eight_delay,[6.875+.48*2+.48*31,-1.38-.37-1],[.17,1],"m2")

make_rect(eight_delay,[1.12,-2.825],[.17,.17],["m1.con","m2.con"])
make_rect(eight_delay,[1.12-.09,-2.825-.08],[.35,.33],["m1","m2"])
make_rect(top,[1.12,-1.38-.37-1-.11],[21.765,.17],"m2")

make_rect(top,[0.255,16.05],[14.95,.17],"m2")
make_rect(top,[0.255,16.05],[.17,-18.91],"m2")
make_rect(eight_delay,[0.255,-2.825],[.17,.17],["m1.con","m2.con"])
make_rect(eight_delay,[0.255-.09,-2.825-.08],[.35,.33],["m1","m2"])
#make_rect(eight_delay,[0.255+14.95-.17,16.0],[.17,.17],["m1.con","m2.con"])
#make_rect(eight_delay,[0.255+14.95-.09-.17,16.0-.08],[.35,.33],["m1","m2"])

#make_rect(eight_delay,[6.875+.48*2+.48*31-.09,-1.38-.37-.09],[.35,.35],["m1","m2"])
#make_rect(eight_delay,[6.875+.48*2+.48*31,-1.38-.37-1],[.17,1],"m2")

for i in range(4):
   dcell = db.DCellInstArray.new(unit_delay.cell_index(),db.DTrans.R0)
   dcell.trans = db.DTrans.new(0,False,10*i*.48,0) * dcell.trans
   quad_delay.insert(dcell)

   dcell = db.DCellInstArray.new(emux.cell_index(),db.DTrans.M0)
   dcell.trans = db.DTrans.new(0,False,i*10*.48,0) * dcell.trans
   quad_delay.insert(dcell)

   make_rect(quad_delay,[i*.48*10-.54+.095+.1+.12,1.195+.05-.10],[.32,.43],"m1")

   if i % 2 == 0:
      make_rect(quad_delay,[i*.48*10 + .48*7-.2,.5],[.49,.17],"li")
      make_rect(quad_delay,[i*.48*10 + .48*7+.3-.09,.5+.17],[.17,-1.2],"li")
      make_rect(quad_delay,[i*.48*10 + .48*7+.3-.09,.5+.17-1.2-.17],[1.5,.17],"li")

   else:
      make_rect(quad_delay,[i*.48*10 + 2.98500-.08, .43-.08+.08], [.33,.33],"li")
      make_rect(quad_delay,[i*.48*10 + 2.98500-.08, .43-.08+.08], [.33,.33],"m1")
      make_rect(quad_delay,[i*.48*10 + 2.98500, .43+.08], [.17,.17],"m1.con")
      make_rect(quad_delay,[i*.48*10 + 2.98500-1.37, .43+.08], [.17,.17],"m1.con")
      make_rect(quad_delay,[i*.48*10 + 2.98500-1.37-.08, .43-.08+.08], [.33,.33],"li")
      make_rect(quad_delay,[i*.48*10 + 2.98500-1.37-.08, .43-.08+.08], [.33,.33],"m1")
      make_rect(quad_delay,[i*.48*10 + 2.98500-1.37, .43+.08], [1.37+.17,.17],"m1")
      make_rect(quad_delay,[i*.48*10 + 2.98500-1.37,.5+.17],[.17,-1.2],"li")
      make_rect(quad_delay,[i*.48*10 + 2.98500-1.37+.17,.5+.17-1.2-.17],[-.6,.17],"li")

      make_rect(quad_delay,[i*.48*10-.54+.095+.1+.12,-1.5],[.32,.43],"m1")
      make_rect(quad_delay,[i*.48*10-.54+.095+.1+.12,-2.4],[.32,.6],"m1")


make_rect(quad_delay,[1*.48*10 + 2.98500+.08, .43+.08-1.17], [2.1,.17],"m1")
make_rect(quad_delay,[1*.48*10 + 2.98500, .43-1.17+.08], [.17,.17],"m1.con")
make_rect(quad_delay,[1*.48*10 + 2.98500+.08+2.1-.11, .43+.08-1.17], [.17,.17],"m1.con")
make_rect(quad_delay,[1*.48*10 + 2.98500-.08, .43-1.17], [.33,.33],"m1")
make_rect(quad_delay,[1*.48*10 + 2.98500+.08+2.1-.11-.08, .43-1.17], [.33,.33],"m1")

make_rect(quad_delay,[1*.48*10 + 6, .43+.08-1.17], [6.75,.17],"m1")
make_rect(quad_delay,[1*.48*10 + 6-.085, .43+.08-1.17], [.17,.17],"m1.con")
make_rect(quad_delay,[1*.48*10 + 6-.16+6.75, .43+.08-1.17], [.17,.17],"m1.con")
make_rect(quad_delay,[1*.48*10 + 6-.085-.08, .43+.08-1.17-.08], [.33,.33],"m1")
make_rect(quad_delay,[1*.48*10 + 6-.16+6.75-.08, .43+.08-1.17-.08], [.33,.33],"m1")

make_pin([quad_delay],[-0.145+0*.48,-1.435],"m1","S4B")
make_pin([quad_delay],[-0.145+0*.48,-2.015],"m1","S4")

make_pin([top,eight_delay,quad_delay],[-0.145+10*.48,-1.435],"m1","S2B")
make_pin([top,eight_delay,quad_delay],[-0.145+10*.48,-2.015],"m1","S2")
make_pin([top,eight_delay,quad_delay],[-0.145+20*.48,-1.435],"m1","S3B")
make_pin([top,eight_delay,quad_delay],[-0.145+20*.48,-2.015],"m1","S3")
make_pin([top,eight_delay],[-0.145+41*.48,-1.435],"m1","S4B")
make_pin([top,eight_delay],[-0.145+41*.48,-2.015],"m1","S4")

make_pin([top,eight_delay],[-0.145+0*.48,-1.435],"m1","S5B")
make_pin([top,eight_delay],[-0.145+0*.48,-2.015],"m1","S5")

make_pin([top,eight_delay,quad_delay],[6.875-.48*8,-1.38],"li","OUTDDDDD")
make_pin([quad_delay],[6.875+.48*22,-1.38],"li","OUTDDDD")

make_pin([top,eight_delay,quad_delay],[0.155,-3.415],"m1","VDD")
make_pin([top,eight_delay,quad_delay],[6.875+.48*2,-1.38],"li","OUTDD")
make_pin([top,eight_delay,quad_delay],[6.875+.48*12,-1.38],"li","OUTDDD")
make_pin([top,eight_delay],[6.875+.48*2+.48*31,-1.38],"li","OUTDDDD")

make_pin([top,eight_delay,quad_delay],[11.12,-2],"m1","TP1")


make_rect(top,[37.83,6.5],[.15,.5],"poly")
make_rect(top,[37.83,6.5],[.25,.15],"poly")
make_rect(top,[38,6.0],[.33,.65],"poly")
make_rect(top,[38,6.0-.1],[.33,.85],"npc")
make_rect(top,[38+.08,6.08],[.17,.17],"li.con")
make_rect(top,[38-.2+.255,6.0],[.265,.33],"li")
make_bone(top,[38-.7,6.0],.88,"m1")

make_bone(top,[38.3,1.06],11.2,"m2",True,ps=.35,ol="m1")
make_bone(top,[38.3-.57,1.06+.85],11.2-.85*2,"m2",True,ps=.35,ol="m1")
make_bone(top,[36.11,-2.35],18.09,"m2",True,ps=.35,ol="m1")
make_bone(top,[36.61,-1.01],17.09-1.76,"m2",True,ps=.35,ol="m1")

make_bone(eight_delay,[9.53,-1.41],2,"m2",False,ps=.35,ol="m1",two_sided=False)
make_bone(eight_delay,[9.53+19.69,-1.41],-2,"m2",False,ps=.35,ol="m1",two_sided=False)
make_rect(eight_delay,[9.55+2-.17,-1.41-.085],[.17,2],"m2")
make_rect(eight_delay,[9.55+19.69-2-.17,-1.41-.085],[.17,2],"m2")
make_bone(eight_delay,[9.55+2-.075+7.13,-1.41+2],-7.13,"m2",False,ps=.35,ol="m1",two_sided=False)
make_bone(eight_delay,[9.55+15.45,-1.41+2],2.335,"m2",False,ps=.35,ol="m1",two_sided=False)
make_rect(eight_delay,[9.55+2.45+6.5,-1.41+2-.085],[2.335+4.1,.17],"m1")

#make_rect(eight_delay,[9.55+2-.17,-1.41-.085+2],[19.69-4+.17,.17],"m2")

make_bone(eight_delay,[9.55+1.64,-1.92],4,"m2",False,ps=.35,ol="m1",two_sided=False)
make_bone(eight_delay,[9.55+1.64+19.7,-1.92],-5,"m2",False,ps=.35,ol="m1",two_sided=False)
make_rect(eight_delay,[9.55+1.64+4-.17,-1.92-.085],[.17,1.345],"m2")
make_rect(eight_delay,[9.55+1.64+19.7-5-.17,-1.92-.085],[.17,1.345],"m2")
make_bone(eight_delay,[9.55+1.64+4-.085+3.5,-1.92+1.345],-3.5,"m2",False,ps=.35,ol="m1",two_sided=False)
make_bone(eight_delay,[9.55+1.64+4-.085+9.88,-1.92+1.345],1,"m2",False,ps=.35,ol="m1",two_sided=False)
make_rect(eight_delay,[9.55+2.45+6.5,-1.92+1.345-.085],[2.335+4.1,.17],"m1")
#make_bone(eight_delay,[9.55+1.64+4-.085,-1.92-.085+1.345],19.7-9+.17,"m2",False,ps=.35,ol="m1",two_sided=False)

make_rect(top,[9.55+19-.17,-1.41-.085],[.17,20-3.6],"m2")
make_rect(top,[9.55+21.5-.17,-1.41-.085-.6],[.17,20-3.6+.92],"m2")
make_rect(top,[9.55+21.5,-1.41-.085-.6+20-3.6+.92-.07],[-5,.17],"m2")

make_bone(eight_delay,[19.62,-1.44],8.2,"m2",True,ps=.35,ol="m1",two_sided=False)
make_rect(top,[19.695,-1.44+8.08],[-1.47,.17],"m2")
make_rect(top,[19.62,-2.0],[-.5,0.17],"m1")
make_bone(top,[19.12,-2+.085],8.2,"m2",True,ps=.35,ol="m1",two_sided=False)
make_bone(top,[16.64,15.21],-8.2-.725,"m2",True,ps=.35,ol="m1",two_sided=False)
make_rect(top,[19.12,-1.44+7.47],[-2.47-.105,.17],"m2")

dcell = db.DCellInstArray.new(scs8hs_tap_1.cell_index(),db.DTrans.R0)
dcell.trans = db.DTrans.new(0,False,.48*39,0) * dcell.trans
quad_delay.insert(dcell)

dcell = db.DCellInstArray.new(scs8hs_tap_1.cell_index(),db.DTrans.M0)
dcell.trans = db.DTrans.new(0,False,.48*39,6.745 - .085) * dcell.trans
quad_delay.insert(dcell)

dcell = db.DCellInstArray.new(scs8hs_tap_1.cell_index(),db.DTrans.M0)
dcell.trans = db.DTrans.new(0,False,.48*39,0) * dcell.trans
quad_delay.insert(dcell)


dcell = db.DCellInstArray.new(quad_delay.cell_index(),db.DTrans.R0)
eight_delay.insert(dcell)

dcell = db.DCellInstArray.new(quad_delay.cell_index(),db.DTrans.R0)
dcell.trans = db.DTrans.new(0,False,.48*41,0) * dcell.trans
eight_delay.insert(dcell)


dcell = db.DCellInstArray.new(eight_delay.cell_index(),db.DTrans.R0)
top.insert(dcell)

dcell = db.DCellInstArray.new(eight_delay.cell_index(),db.DTrans.R180)
dcell.trans = db.DTrans.new(0,False,0.48*79,14-.68) * dcell.trans
top.insert(dcell)

#m1


#m1 pin


#li pin



#inst=db.CellInstArry

layout.write("foo.gds")
