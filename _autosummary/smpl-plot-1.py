from smpl import functions as f
from smpl import plot
param = plot.fit([0,1,2],[0,1,2],f.line)
plot.unv(param).round()[0]
# 1.0
