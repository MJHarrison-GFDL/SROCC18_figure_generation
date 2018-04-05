#!/usr/bin/env python

from midas.rectgrid import *
from midas.rectgrid_gen import *
import netCDF4
import numpy

def ice9it(i, j, depth, minD=0.):
  """
  Recursive implementation of "ice 9".
  Returns 1 where depth>minD and is connected to depth[j,i], 0 otherwise.
  """
  wetMask = 0*depth

  (nj,ni) = wetMask.shape
  stack = set()
  stack.add( (j,i) )
  while stack:
    (j,i) = stack.pop()
    if wetMask[j,i] or depth[j,i] <= minD: continue
    wetMask[j,i] = 1

    if i>0: stack.add( (j,i-1) )
    else: stack.add( (j,ni-1) ) # Periodic beyond i=0

    if i<ni-1: stack.add( (j,i+1) )
    else: stack.add( (j,0) ) # Periodic beyond i=ni-1

    if j>0: stack.add((j-1,i))

    if j<nj-1: stack.add( (j+1,i) )
    else: stack.add( (j,ni-1-i) ) # Tri-polar fold beyond j=nj-1

  return wetMask

def ice9(x, y, depth, xy0):
  ji = nearestJI(x, y, xy0)
  print ji
  return ice9it(ji[1], ji[0], depth)

def nearestJI(x, y, (x0, y0)):
  """
  Find (j,i) of cell with center nearest to (x0,y0).
  """
  return numpy.unravel_index( ((x-x0)**2 + (y-y0)**2).argmin() , x.shape)

def southOf(x, y, xy0, xy1):
  """
  Returns 1 for point south/east of the line that passes through xy0-xy1, 0 otherwise.
  """
  x0 = xy0[0]; y0 = xy0[1]; x1 = xy1[0]; y1 = xy1[1]
  dx = x1 - x0; dy = y1 - y0
  Y = (x-x0)*dy - (y-y0)*dx
  Y[Y>=0] = 1; Y[Y<=0] = 0
  return Y

# Rewrite
print 'Reading grid ...',
grid=quadmesh('woa.r360x180.nc',var='thetao')
grid.D=netCDF4.Dataset('woa_depths.r360x180.nc').variables['depth'][:]
grid.wet=numpy.zeros(grid.D.shape)
grid.wet[grid.D>0.]=1.0
grid.lath=grid.y_T[:,grid.im/4]  # should not be needed
grid.latq=grid.y_T_bounds[:,grid.im/4+1] # ditto

x = grid.x_T
y = grid.y_T

print 'reading topography ...',
depth = grid.D
print 'done.'

print 'Generating global wet mask ...',
wet = ice9(x, y, depth, (0,-35)) # All ocean points seeded from South Atlantic

#plt.pcolormesh(x,y,wet)
#plt.colorbar()
#plt.show()


print 'done.'

code = 0*wet

print 'Finding Cape of Good Hope ...',
tmp = 1 - wet; #tmp[x<330] = 0

tmp = ice9(x, y, tmp, (20.,-30))
yCGH = (tmp*y).min()
print 'done.', yCGH


print 'Finding Melbourne ...',
tmp = 1 - wet; #tmp[x>180] = 0
tmp = ice9(x, y, tmp, (140,-25.))
yMel = (tmp*y).min()
print 'done.', yMel



print 'Processing Persian Gulf ...'
tmp = wet*( 1-southOf(x, y, (55.,23.), (56.5,27.)) )
tmp = ice9(x, y, tmp, (53.,25.))
code[tmp>0] = 11
wet = wet - tmp # Removed named points

print 'Processing Red Sea ...'
tmp = wet*( 1-southOf(x, y, (40.,11.), (45.,13.)) )
tmp = ice9(x, y, tmp, (40.,18.))
code[tmp>0] = 10
wet = wet - tmp # Removed named points

print 'Processing Black Sea ...'
tmp = wet*( 1-southOf(x, y, (26.,42.), (32.,40.)) )
tmp = ice9(x, y, tmp, (32.,43.))
code[tmp>0] = 7
wet = wet - tmp # Removed named points

print 'Processing Mediterranean ...'
tmp = wet*( southOf(x, y, (354.3,35.5), (354.3,36.5)) + southOf(x, y, (50,60), (50,10)) )
tmp = ice9(x, y, tmp, (4.,38.))
code[tmp>0] = 6
wet = wet - tmp # Removed named points

print 'Processing Baltic ...'
tmp = wet*( southOf(x, y, (8.6,56.), (8.6,60.)) )
tmp = ice9(x, y, tmp, (10.,58.))
code[tmp>0] = 9
wet = wet - tmp # Removed named points

print 'Processing Hudson Bay ...'
tmp = wet*(
           ( 1-(1-southOf(x, y, (265.,66.), (276.5,67.5)))
              *(1-southOf(x, y, (276.5,67.5), (276.,71.)))
           )*( 1-southOf(x, y, (290.,58.), (290.,65.)) ) )
tmp = ice9(x, y, tmp, (275.,60.))



code[tmp>0] = 8
wet = wet - tmp # Removed named points

print 'Processing Arctic ...'
tmp = wet*(0
     +     southOf(x, y, (100.,0.), (100.,65.))*(1-southOf(x, y, (150.,0.), (150.,90.)))*(1-southOf(x, y, (189.,60.), (194.,60.))) # Russian Arctic
     +     southOf(x, y, (150.,0.), (150.,65.))*(1-southOf(x, y, (310.,0.), (310.,90.)))*(1-southOf(x, y, (189.,66.), (194.,65.5))) * (1-southOf(x, y, (296.,66.4), (310.,68.5))) # Baffin Bay and Arctic
     +     southOf(x, y, (20.,0.), (20.,65.))*(1-southOf(x, y, (100.,0.), (100.,90.)))*(1-southOf(x, y, (20.,50.), (100.,50.)))  # Barents Sea
     +     southOf(x, y, (310.,0.), (310.,90.)) * (1- southOf(x, y, (0.,65.5), (360.,65.5))  ) # Denmark Strait
     +     (1-southOf(x, y, (20.,0.), (20.,65.))) * (1- southOf(x, y, (80.,55), (160.,65))  ) # Scotland-Sweden
     +     (southOf(x, y, (320.,0.), (320.,65.))) * (1-southOf(x, y, (358.,0.), (358.,65.))) * southOf(x, y, (0.,65.5), (360.,65.5)) * (1-southOf(x, y, (342.,66), (354.,58))  ) # Iceland-Scotland
     +     (southOf(x, y, (358.,0.), (358.,65.))) *  southOf(x, y, (0.,65.5), (360.,65.5)) * (1-southOf(x, y, (350.,52.), (360.,52.))  ) # North Sea
          )


tmp = ice9(x, y, tmp, (0.,85.))

code[tmp>0] = 4
wet = wet - tmp # Removed named points

print 'Processing Pacific ...'
tmp = wet*( (1-southOf(x, y, (0.,yMel), (360.,yMel)))*southOf(x,y,(99,0),(99,1))
           -southOf(x, y, (101,1), (101,0))*southOf(x, y, (0,3), (1,3))
           -southOf(x, y, (105.75,1), (105.75,0))*southOf(x, y, (0,-5), (1,-5))
           -southOf(x, y, (116.3,1), (116.3,0))*southOf(x, y, (0,-8.4), (1,-8.4))
           -southOf(x, y, (125.5,1), (125.5,0))*southOf(x, y, (0,-8.9), (1,-8.9))
          )

tmp = ice9(x, y, tmp, (210.,0.))


code[tmp>0] = 3
wet = wet - tmp # Removed named points

print 'Processing Atlantic ...'
tmp = wet*(1-southOf(x, y, (0.,yCGH), (360.,yCGH)))
tmp = ice9(x, y, tmp, (-20.,0.))

code[tmp>0] = 2
wet = wet - tmp # Removed named points

print 'Processing Indian ...'
tmp = wet*(1-southOf(x, y, (0.,yCGH), (360.,yCGH)))
tmp = ice9(x, y, tmp, (55.,0.))

code[tmp>0] = 5
wet = wet - tmp # Removed named points

print 'Processing Southern Atlantic Ocean ...'
tmp = wet*(0
  + (southOf(x, y, (290.,0), (290.,1)))
  + (1-southOf(x, y, (20.,0), (20.,1)))
  )

tmp = ice9(x, y, tmp, (0.,-55.))
code[tmp>0] = 2
wet = wet - tmp # Removed named points

print 'Processing Southern Pacific Ocean ...'
tmp = wet*(0
  + (southOf(x, y, (145.,0), (145.,1)))
  )

tmp = ice9(x, y, tmp, (180.,-55.))
code[tmp>0] = 3
wet = wet - tmp # Removed named points

print 'Processing Southern Indian Ocean ...'
tmp = ice9(x, y, wet, (90.,-55.))
code[tmp>0] = 5
wet = wet - tmp # Removed named points

code[wet>0] = -9
(j,i) = numpy.unravel_index( wet.argmax(), x.shape)
if j:
  print 'There are leftover points unassigned to a basin code'
  while j:
    print x[j,i],y[j,i],[j,i]
    wet[j,i]=0
    (j,i) = numpy.unravel_index( wet.argmax(), x.shape)
#    code[j,i]=-99
else: print 'All points assigned a basin code'


plt.pcolormesh(grid.x_T_bounds,grid.y_T_bounds,numpy.ma.masked_where(code==0,code))
plt.colorbar()
#plt.contour(x,y,wet,[0.5,0.51])
plt.show()


mask=code

S=state(grid=grid)
var_dict={}
var_dict['X']='Longitude'
var_dict['xax_data']= grid.lonh
var_dict['xunits']= 'degrees_E'
var_dict['Y']='Latitude'
var_dict['yax_data']= grid.lath
var_dict['yunits']= 'degrees_N'
var_dict['Z']=None
var_dict['T']=None
var_dict['_FillValue']=None
var_dict['missing_value']=None
var_dict['flag_values']='1,2,3,4,5,6,7,8,9,10,11'
var_dict['flag_meanings']='1:Southern Ocean, 2:Atlantic Ocean, 3:Pacific Ocean, 4:Arctic Ocean, 5:Indian Ocean, 6:Mediterranean Sea, 7:Black Sea, 8:Hudson Bay, 9:Baltic Sea, 10:Red Sea, 11:Persian Gulf'

S.add_field_from_array(mask,'basin',var_dict=var_dict)

S.write_nc('basin_codes.nc',['basin'])
