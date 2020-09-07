#!/usr/bin/python3

fin = open("TOP.spice", "rt")
olines = []
for line in fin:
   if line.startswith(".option"):
      continue
   if line.startswith("Xscs8hs_fill_"):
      continue
   if line.startswith("Xscs8hs_tapvpwrvgnd"):
      continue

   line=line.replace("w=144","w=148")
   olines.append(line)
fin.close()

fout = open("TOP.spice", "wt")
fout.write("".join(olines))

fout.close()

