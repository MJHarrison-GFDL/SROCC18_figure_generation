
# coding: utf-8

# ** Figures 2.1.1-2.1.5 for the IPCC Special Report on Oceans and Cryosphere in a Changing Climate **
#
# 2.1.1 (B) Plan-view CMIP5 RCP4.5 mean heat 0-700m, (2013 to 2017) - (2000 to 2004)
# 2.1.1 (C) Plan-view CMIP5 RCP8.5 mean heat 0-700m, (2081 to 2100) - (1986 to 2005)
# ( The time-series line plots in 2.1.1 D & E can wait.)
#
# 2.1.3 (D) Plan-view CMIP5 mean salinity 0-100m, (1996 to 2015) - (1966 to 1985)
# 2.1.3 (E) Plan-view CMIP5 RCP8.5 mean salinity 0-100m, (CMIP6 RCP8.5; (2081 to 2100) - (1986 to 2005))
#
# 2.1.5 Zonal basin mean changes (8 of 12 panels - T & S priority, density as time permits)
# (2081 to 2100) - (1986 to 2005)
#

from midas.rectgrid import *
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy
import netCDF4 as nc
import numpy as np
import dataset
import sys,os
import hashlib
import argparse
from scipy import stats
#####################

parser = argparse.ArgumentParser()
parser.add_argument('--model',type=str,help='model name',default=None)
parser.add_argument('--type',type=str,help='heat_maps,zonal_sections,salt_maps,zonal_density_sections',default=None)
parser.add_argument('--ztop',type=float,help='starting depth',default=0.)
parser.add_argument('--zbot',type=float,help='starting depth',default=0.)
parser.add_argument('--vmin',type=float,help='shading start',default=-5)
parser.add_argument('--vmax',type=float,help='shading end',default=5)
args=parser.parse_args()


def load_tracer(flist,grid,field,z_indices=None):
    S=[]
    for f in flist:
        S.append(state(f,grid=grid,fields=[field],verbose=False,z_indices=z_indices))
    return S

def depth_avg(T,field='thetao',name=None,dz_min=100,normalize=False):
    zmask=None
    vd=T[0].var_dict[field]

    for t in T:
        vd=t.var_dict[field]
        t.volume_integral(field,'Z',normalize=normalize)
        if normalize:
            vars(t)[field+'_zav']=np.ma.masked_where(t.grid.D[np.newaxis,np.newaxis,:]<dz_min,vars(t)[field+'_zav'])
            t.rename_field(field+'_zav',name)
        else:
            vars(t)[field+'_zint']=np.ma.masked_where(t.grid.D[np.newaxis,np.newaxis,:]<dz_min,vars(t)[field+'_zint'])
            t.rename_field(field+'_zint',name)

def load_basin(path):
    f=nc.Dataset(path)
    basin=f.variables['basin']
    return basin

def show_basin(grid,basin,vmin=None,vmax=None,fout='basin.png',show=False):
    plt.pcolormesh(grid.x_T_bounds,grid.y_T_bounds,sq(basin))
    plt.colorbar()
    if show:
        plt.show()
    if fout is not None:
        plt.savefig(fout)
    plt.clf()

def depths_and_basin_codes(path='GEBO_08_v2.nc',target=None,out_path='depths.nc'):
    grid=quadmesh(path,var='depth',cyclic=True)
    D=state(path,grid=grid,fields=['depth'],verbose=False)
    D2=D.horiz_interp('depth',target=target)
    D2.depth=-D2.depth
    D2.write_nc(out_path,['depth'],format='NETCDF3_CLASSIC')
    execfile('make_basin_mask.py')
    basin=nc.Dataset('basin_codes.nc').variables['basin'][:]
    return D2.depth,basin


def load_file_list(R):
    flist=[]
    for r in R:
        flist.append(r['file'])
    return flist

def  load_woa(woa_path='obs.r360x180.nc'):
    #woa_path='/archive/gold/datasets/obs/WOA05_pottemp_salt.nc'
    grid_woa = quadmesh(woa_path,var='thetao',cyclic=True)
    if not os.path.isfile(woa_path):
        WOA=state(woa_path,grid=grid_woa,fields=['thetao','so'],verbose=False)
        WOA.time_avg('thetao',vol_weight=False)
        WOA.rename_field('thetao_tav','thetao')
        WOA.time_avg('so',vol_weight=False)
        WOA.rename_field('so_tav','so')
        WOA.write_nc(woa_path,['thetao','so'])
    else:
        WOA=state(woa_path,grid=grid_woa,fields=['thetao','so','sigma'],verbose=False)
    return grid_woa, WOA

def load_depth_basin():
     """These files were used to generate the depth and basin files
    GEBCO_path='/archive/gold/datasets/topography/GEBCO_08_v2.nc'
    depth,basin=depths_and_basin_codes(GEBCO_path,grid_woa)"""
     depth=nc.Dataset('woa_depths.r360x180.nc').variables['depth'][:]
     basin=nc.Dataset('basin_codes.r360x180.nc').variables['basin'][:]
     return depth,basin

def ensemble_trend(grid,CR,PR,CF,PF,var):
    #Returns mean change between two time periods
    #of the predictive models with respect to corresponding control experiments
    #i.e., change == mean(pf)-mean(pr) - mean(cf)-mean(cr)
    #where lowercase (pf, etc.) are single or multiple realizations of the same model

    def mean_across_ensembles(S):
        ssum=None
        if isinstance(S,(list)):
            slen=len(S)
            sarr=[]
            for s in S:
                sarr.append(vars(s)[var])

            sarr=np.asarray(sarr)
            smean=np.mean(sarr,axis=0)
        else:
            slen=1
            smean=vars(s)[var]
            sarr=smean[np.newaxis,:]
        return smean,sarr

    cr,cr_e=mean_across_ensembles(CR)
    print 'Calculated Ensemble Control Reference Period using ',cr_e.shape[0],' members: ',np.mean(cr)
    pr,pr_e=mean_across_ensembles(PR)
    print 'Calculated Ensemble Predicted Reference Period using ',pr_e.shape[0],' members: ',np.mean(pr)
    cf,cf_e=mean_across_ensembles(CF)
    print 'Calculated Ensemble Control Forecast Period using ',cf_e.shape[0],' members: ',np.mean(cf)
    pf,pf_e=mean_across_ensembles(PF)
    print 'Calculated Ensemble Predicted Forecast Period using ',pf_e.shape[0],' members: ',np.mean(pf)
    trend = pf - pr - cf + cr
    ssize = cr_e.shape[0]+pr_e.shape[0]+cf_e.shape[0]+pf_e.shape[0]-3
    t2,p2 = stats.ttest_ind(pr_e-cr_e,cf_e-pf_e,axis=0)
    p2[np.isnan(p2)]=0.
    print 'pval max/min=',p2.max(),p2.min()
    print 'Calculated Ensemble Mean percentage Change : ',100.0*np.mean(trend)/np.mean(cf)
    return trend,cf-cr,p2

def masked_zonal_avg(s,field=None,basin=None,basin_mask=None,normalize=True):
    fld_out = field+'_masked'
    vd=s.var_dict[field].copy()
    s.add_field_from_array(vars(s)[field],fld_out,vd)
    if basin_mask is not None:
        s.grid.mask = basin[:]
        x=s.grid.x_T.copy()
        xb=np.where(s.grid.mask==basin_mask)
        xb=xb[1]
        latb=np.where(s.grid.mask==basin_mask)[0][0]
        lonb=[np.min(xb),np.max(xb)]
        x[s.grid.mask!=basin_mask]=0
        x[s.grid.mask==basin_mask]=1
        x[:latb,lonb[0]:lonb[1]]=1
        s.grid.mask=x.copy()
        mask_str = 'grid.mask!=1'
        s.mask_where(fld_out,mask_str)
    s.grid.D[s.grid.D<0]=0.
    s.adjust_thickness(fld_out)
    s.volume_integral(fld_out,'X',normalize=normalize,use_weights=True)
    return None

def show_zonal_trend(T,S,OBS,field='thetao',title='Zonal Avg Potential Temperature Trend',vmin=None,vmax=None,cmap=plt.cm.bwr,nyears=None,ndf=None,ModelList=None,fname=None,pval_tol=0.05,lat_bnds=[-78,90.]):

    plt.clf()
    f, (ax1,ax2) = plt.subplots(2,sharex=True,figsize=(12,6))
    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
#    masked_zonal_avg(T,basin_mask)
#    masked_zonal_avg(S,basin_mask)

    if field=='thetao' or field=='sigma':
        V=T
        if field=='thetao':
            clevs=[5,10,15,20,25,30]
        elif field=='sigma':
            clevs=np.arange(25,34)
    elif field=='so':
        V=S
        clevs=np.arange(34,36.5,.25)



    D=V.grid.D.copy()
    D=np.ma.masked_where(D<30.,D)
    Dpth_mean=-np.ma.mean(D,axis=1)
    x=V.grid.latq;xc=V.grid.lath;y=-V.var_dict['delta']['zbax_data'];yc=-V.var_dict['delta']['zax_data']

    #### output units are degC or PSU per 50 years
    zout = sq(vars(V)['delta'])/nyears*50
    X,Y=np.meshgrid(xc,yc)
    DM,dum=np.meshgrid(Dpth_mean,yc)
    zout=np.ma.masked_where(Y<DM,zout)
    cf=ax1.pcolormesh(x,y,zout,vmin=vmin,vmax=vmax,cmap=cmap)
    cf=ax2.pcolormesh(x,y,zout,vmin=vmin,vmax=vmax,cmap=cmap)
    plt.colorbar(cf,ax=ax2,orientation='horizontal',fraction=0.1,pad=0.2)
    ctxt=ax1.contour(X,Y,zout,np.linspace(vmin,vmax,10),colors='w',linewidths=0.75)
    ax1.clabel(ctxt,inline=False,fmt='%1.2f')
    ctxt=ax2.contour(X,Y,zout,np.linspace(vmin,vmax,10),colors='w',linewidths=0.75)
    ax2.clabel(ctxt,inline=False,fmt='%1.2f')

    pval=sq(V.pval.copy())
    pval=np.ma.masked_where(pval<pval_tol,pval)
    if np.any(pval):
        ax1.pcolormesh(x,y,pval,alpha=0.1,cmap=plt.cm.gray)
        ax2.pcolormesh(x,y,pval,alpha=0.1,cmap=plt.cm.gray)

#    sigma2=wright_eos(vars(T)['reference_masked_xav'],vars(S)['reference_masked_xav'],0.)-1.e3
#    print 'max/min T_ref_xav= ',vars(T)['reference_masked_xav'].max(),vars(T)['reference_masked_xav'].min()
#    print 'max/min S_ref_xav= ',vars(S)['reference_masked_xav'].max(),vars(S)['reference_masked_xav'].min()


    tref=vars(OBS)[field+'_masked_xav']
    ctxt=ax1.contour(X,Y,sq(tref),clevs,colors='k')
    ax1.clabel(ctxt,inline=False,fmt='%2.1f')
    ctxt=ax2.contour(X,Y,sq(tref),clevs,colors='k')
    ax2.clabel(ctxt,inline=False,fmt='%2.1f')
    ax1.set_title(title)
    ax1.grid()
    ax2.grid()

#    if basin_mask==1:
#        ax1.set_xlim(V.grid.latq[0],-30.)
#        ax2.set_xlim(V.grid.latq[0],-30.)
#    elif basin_mask==2 or basin_mask == 5:
#        ax1.set_xlim(V.grid.latq[0],90.)
#        ax2.set_xlim(V.grid.latq[0],90.)
#    else:
#        ax1.set_xlim(V.grid.latq[0],90.)
#        ax2.set_xlim(V.grid.latq[0],90.)

    ax1.set_xlim(lat_bnds[0],lat_bnds[1])
    ax2.set_xlim(lat_bnds[0],lat_bnds[1])
    ax1.set_ylim(-500,0)
    ax2.set_ylim(-2000,-500)

    if fname is not None:
        plt.savefig(fname)
        plt.clf()


def zonal_avg(T,field=None,normalize=True,basin=None,basin_mask=None):
    for t in T:
        masked_zonal_avg(t,field,basin,basin_mask,normalize)

    return None

def show_trend(T,field='thetao',title='Depth Avg Potential Temperature Trend (W m-2)',vmin=None,vmax=None,cmap=plt.cm.bwr,fname=None,nyears=None,ndf=None,ModelList=None,pval_tol=0.01):
    if field=='thetao':
        rho_cp = 3925. * 1035.
        scale=rho_cp
        units='W m-2'
    elif field == 'so':
        scale=1.e-3*8.64e4*365.
        units='g kg-1 m-2 yr-1'
        title='Depth Avg Salinity Trend (g kg-1 m-2 yr-1)'

    fig=plt.figure(1,figsize=(12,6))
    ax1=plt.axes(projection=ccrs.Mollweide())
    x=T.grid.x_T_bounds;y=T.grid.y_T_bounds
    xc=T.grid.x_T;yc=T.grid.y_T
    zout = vars(T)['delta'] *scale/(nyears*8.64e4*365.)
#    print 'result=',zout[0,:,148,348]
#    plt.pcolormesh(sq(zout),vmin=vmin,vmax=vmax)
#    plt.show()
#    quit()
    cf=ax1.pcolormesh(x,y,sq(zout),vmin=vmin,vmax=vmax,cmap=cmap,transform=ccrs.PlateCarree())
    ax1.coastlines()
    ax1.set_global()
    ax1.gridlines()
    pval=sq(T.pval.copy())
    pval=np.ma.masked_where(pval<pval_tol,pval)
    ax1.pcolormesh(x,y,pval,transform=ccrs.PlateCarree(),alpha=0.1,cmap=plt.cm.gray)
    plt.colorbar(cf,ax=ax1,fraction=0.01,pad=0.04)
    if ndf is not None:
        ndf_=np.asarray(ndf)
        ndf__=np.sum(ndf_,axis=0)
        ctxt='Ensemble Size= '+str(ndf__)
        ax1.text(0.0,0.1,ctxt,transform=ax1.transAxes,fontsize=8)
    T.var_dict['delta']['Z']=None
    T.delta=np.ma.masked_where(T.grid.D[np.newaxis,np.newaxis,:]<10,T.delta)
    T.delta_ctrl=np.ma.masked_where(T.grid.D[np.newaxis,np.newaxis,:]<10,T.delta_ctrl)
    T.volume_integral('delta','XY',normalize=True)
    ctxt=sq(vars(T)['delta_xyav'])*scale/(nyears*8.64e4*365.)
    ctxt=str(ctxt)
    ctxt='Global Avg: '+ctxt[:ctxt.find('.')+4]
    ax1.text(0.0,0.05,ctxt,transform=ax1.transAxes,fontsize=8)
    if ModelList is not None:
        ax1.text(0.0,-.05,ModelList,transform=ax1.transAxes,fontsize=8)

    ax1.set_title(title)
    if fname is not None:
        plt.savefig(fname)
        plt.clf()


def sfc_trend(T,field='thetao',title='Surface Potential Temperature Change',vmin=None,vmax=None,cmap=plt.cm.bwr,fname=None):

    fig=plt.figure(1,figsize=(12,6))
    ax1=plt.axes(projection=ccrs.Mollweide())
    x=T.grid.x_T_bounds;y=T.grid.y_T_bounds
    xc=T.grid.x_T;yc=T.grid.y_T
    zout = vars(T)['delta'][0,0,:]
    cf=ax1.pcolormesh(x,y,sq(zout),vmin=vmin,vmax=vmax,cmap=cmap,transform=ccrs.PlateCarree())
    ax1.coastlines()
    ax1.set_global()
    ax1.gridlines()
    plt.colorbar(cf,ax=ax1,fraction=0.01,pad=0.04)
    ax1.set_title(title)

    if fname is not None:
        plt.savefig(fname)
        plt.clf()

def find_depth_range(model,path,fx,field='thetao',ztop=0.,zbot=-700.):

    pth=get_listing(path+field+'_*.nc')[0]
    S=state(pth,grid=fx,fields=[field],verbose=False,time_indices=np.arange(0,1))
    z_bounds=-S.var_dict[field]['zbax_data']
    itop=np.where(z_bounds<=ztop)[0][0]
    ibot=np.where(z_bounds<=zbot)[0][0]
    z_range = np.arange(itop,ibot+1)
    return z_range,z_bounds[z_range]


#######################

# Load CMIP5 database


db=dataset.connect('sqlite:///cmip5.db')
tb=db['CMIP5 experiments']
R=tb.distinct('model')
ModelList=[]

if args.model is None:
    for r in R:
        ModelList.append(r['model'])
else:
    for r in R:
        if r['model']==args.model:
            ModelList.append(r['model'].encode('ascii'))


tb=db['CMIP5 regridded x/y/z']
grid_woa,WOA=load_woa()
depth,basin=load_depth_basin()
## include Arctic with the Atlantic
basin[basin==4]=2
grid_woa.D=depth.copy()
grid_woa.D[grid_woa.D<10]=0
grid_woa.mask=basin.copy()
WOA.grid.D=depth
depths=WOA.var_dict['thetao']['zax_data']
# PresentDay results for the reference period (~2000-2005) and the analysis
# time (~2013-2017)
# Future refers to the analysis of the last 20 years of the 21st century referenced
# to the last 20 years of the historical period 1985-2005
#CR == Control experiment values for Reference time-period
#PR == Predicted values based on scenario emissions (ensemble mean) for Reference time-period
#CF == Control experiment values for Forecast  time-period
#PF == Predicted values based on scenario emissions (ensemble mean) for Forecast time-period

if args.type == 'heat_maps':
    Result=[];dTime=[]
    for time_frame in ['PresentDay','Future']:
        for v in ['thetao']:
            NDF=[];TREND=[];TREND_CTRL=[];PVAL=[]
            for model in ModelList:
                print model
                ctrl_ref=tb.find(variable=v,model=model,name=time_frame+'_ref_ctrl')
                fcst_ref=tb.find(variable=v,model=model,name=time_frame+'_ref')
                fcst_ctrl=tb.find(variable=v,model=model,name=time_frame+'_ctrl')
                fcst=tb.find(variable=v,model=model,name=time_frame)
                ztop,zbot=(np.where(depths>args.ztop)[0][0],np.where(depths>args.zbot)[0][0])
                flist_ctrl_ref=load_file_list(ctrl_ref)
                flist_ref=load_file_list(fcst_ref)
                flist_ctrl=load_file_list(fcst_ctrl)
                flist=load_file_list(fcst)
                CR=load_tracer(flist_ctrl_ref,grid=grid_woa,field=v,z_indices=np.arange(ztop,zbot))
                PR=load_tracer(flist_ref,grid=grid_woa,field=v,z_indices=np.arange(ztop,zbot))
                CF=load_tracer(flist_ctrl,grid=grid_woa,field=v,z_indices=np.arange(ztop,zbot))
                PF=load_tracer(flist,grid=grid_woa,field=v,z_indices=np.arange(ztop,zbot))
                depth_avg(CR,field=v,name=v+'_dz',normalize=False)
                depth_avg(PR,field=v,name=v+'_dz',normalize=False)
                depth_avg(CF,field=v,name=v+'_dz',normalize=False)
                depth_avg(PF,field=v,name=v+'_dz',normalize=False)
                for c in [CR,PR,CF,PF]:
                    if len(c)==0:
                        print 'THERE IS A PROBLEM WITH MODEL : ',model,' FOR ',time_frame,' ',v,' : data appears to be missing'
                        raise()
                ndf=len(CR)+len(PR)+len(CF)+len(PF)-3
                NDF.append(ndf)
                va=v+'_dz'
                trend,trend_ctrl,pval=ensemble_trend(grid_woa,CR,PR,CF,PF,va)
                TREND.append(trend)
                TREND_CTRL.append(trend_ctrl)
                PVAL.append(pval)

            dTime.append(CF[0].var_dict[v]['dates'][0].year-CR[0].var_dict[v]['dates'][0].year)
            S=state(grid=grid_woa,verbose=False)
            vd=PF[0].var_dict[v].copy()
            TREND=np.asarray(TREND)
            trend=np.mean(TREND,axis=0)
            TREND_CTRL=np.asarray(TREND_CTRL)
            trend_ctrl=np.mean(TREND_CTRL,axis=0)
            PVAL=np.asarray(PVAL)
            NDF=np.asarray(NDF)
#            print 'trend=',trend[0,:,148,348]
#            print 'trend_ctrl=',trend_ctrl[0,:,148,348]
#            quit()
            S.add_field_from_array(trend,'delta',var_dict=vd)
            S.add_field_from_array(trend_ctrl,'delta_ctrl',var_dict=vd)
#            S.add_field_from_array(tref,'reference',var_dict=vd)
            t2,pval=stats.ttest_ind(TREND,TREND_CTRL,axis=0)
            pval[np.isnan(pval)]=0.0
            vd['units']='none'
            S.add_field_from_array(pval,'pval',var_dict=vd)
            entry=dict(variable=v,state=S,ndf=NDF)
            Result.append(entry)
    WOA.adjust_thickness('thetao')
    WOA.adjust_thickness('so')
    thetao=Result[0]
    z_suffix=str(np.int(args.ztop))+'to'+str(np.int(args.zbot))+'m'
    tit='Present Day Rate of Warming '+z_suffix+' (W m-2)'
    print 'dTime= ',dTime
    show_trend(thetao['state'],field='thetao',title=tit,vmin=args.vmin,vmax=args.vmax,cmap=plt.cm.bwr,nyears=dTime[0],fname='heating_map_'+z_suffix+'_present.png',ndf=thetao['ndf'],ModelList=ModelList,pval_tol=0.05)
    thetao=Result[1]
    tit='Future Rate of Warming '+z_suffix+'m (W m-2)'
    show_trend(thetao['state'],field='thetao',title=tit,vmin=args.vmin,vmax=args.vmax,cmap=plt.cm.bwr,nyears=dTime[1],fname='heating_map_'+z_suffix+'_future.png',ndf=thetao['ndf'],ModelList=ModelList,pval_tol=0.05)


if args.type == 'salt_maps':
    Result=[];dTime=[]
    for time_frame in ['PresentDay','Future']:
        for v in ['so']:
            NDF=[];TREND=[];TREND_CTRL=[];PVAL=[]
            for model in ModelList:
                print model
                ctrl_ref=tb.find(variable=v,model=model,name=time_frame+'_ref_ctrl')
                fcst_ref=tb.find(variable=v,model=model,name=time_frame+'_ref')
                fcst_ctrl=tb.find(variable=v,model=model,name=time_frame+'_ctrl')
                fcst=tb.find(variable=v,model=model,name=time_frame)
                ztop,zbot=(np.where(depths>args.ztop)[0][0],np.where(depths>args.zbot)[0][0])
                flist_ctrl_ref=load_file_list(ctrl_ref)
                flist_ref=load_file_list(fcst_ref)
                flist_ctrl=load_file_list(fcst_ctrl)
                flist=load_file_list(fcst)
                CR=load_tracer(flist_ctrl_ref,grid=grid_woa,field=v,z_indices=np.arange(ztop,zbot))
                PR=load_tracer(flist_ref,grid=grid_woa,field=v,z_indices=np.arange(ztop,zbot))
                CF=load_tracer(flist_ctrl,grid=grid_woa,field=v,z_indices=np.arange(ztop,zbot))
                PF=load_tracer(flist,grid=grid_woa,field=v,z_indices=np.arange(ztop,zbot))
                depth_avg(CR,field=v,name=v+'_dz',normalize=False)
                depth_avg(PR,field=v,name=v+'_dz',normalize=False)
                depth_avg(CF,field=v,name=v+'_dz',normalize=False)
                depth_avg(PF,field=v,name=v+'_dz',normalize=False)
                for c in [CR,PR,CF,PF]:
                    if len(c)==0:
                        print 'THERE IS A PROBLEM WITH MODEL : ',model,' FOR ',time_frame,' ',v,' : data appears to be missing'
                        raise()
                ndf=len(CR)+len(PR)+len(CF)+len(PF)-3
                NDF.append(ndf)
                va=v+'_dz'
                trend,trend_ctrl,pval=ensemble_trend(grid_woa,CR,PR,CF,PF,va)
                TREND.append(trend)
                TREND_CTRL.append(trend_ctrl)
                PVAL.append(pval)

            dTime.append(CF[0].var_dict[v]['dates'][0].year-CR[0].var_dict[v]['dates'][0].year)
            S=state(grid=grid_woa,verbose=False)
            vd=PF[0].var_dict[v].copy()
            TREND=np.asarray(TREND)
            trend=np.mean(TREND,axis=0)
            TREND_CTRL=np.asarray(TREND_CTRL)
            trend_ctrl=np.mean(TREND_CTRL,axis=0)
            PVAL=np.asarray(PVAL)
            NDF=np.asarray(NDF)
#            print 'trend=',trend[0,:,148,348]
#            print 'trend_ctrl=',trend_ctrl[0,:,148,348]
#            quit()
            S.add_field_from_array(trend,'delta',var_dict=vd)
            S.add_field_from_array(trend_ctrl,'delta_ctrl',var_dict=vd)
#            S.add_field_from_array(tref,'reference',var_dict=vd)
            t2,pval=stats.ttest_ind(TREND,TREND_CTRL,axis=0)
            pval[np.isnan(pval)]=0.0
            vd['units']='none'
            S.add_field_from_array(pval,'pval',var_dict=vd)
            entry=dict(variable=v,state=S,ndf=NDF)
            Result.append(entry)
    WOA.adjust_thickness('thetao')
    WOA.adjust_thickness('so')
    so=Result[0]
    z_suffix=str(np.int(args.ztop))+'to'+str(np.int(args.zbot))+'m'
    tit='Present Day Rate of Salinity Change '+z_suffix+' (g kg-1 m-2 yr-1)'
    print 'dTime= ',dTime
    show_trend(so['state'],field='so',title=tit,vmin=args.vmin,vmax=args.vmax,cmap=plt.cm.bwr,nyears=dTime[0],fname='salt_map_'+z_suffix+'_present.png',ndf=so['ndf'],ModelList=ModelList,pval_tol=0.05)
    so=Result[1]
    tit='Future Rate of Salinity Change '+z_suffix+' (g kg m-2 yr-1)'
    show_trend(so['state'],field='so',title=tit,vmin=args.vmin,vmax=args.vmax,cmap=plt.cm.bwr,nyears=dTime[1],fname='salt_map_'+z_suffix+'_future.png',ndf=so['ndf'],ModelList=ModelList,pval_tol=0.05)

if args.type == 'zonal_sections':
    for region,reg_id in zip(['Global','Atlantic','Pacific','Indian'],[None,2,3,5]):
        Result=[]
        for time_frame in ['PresentDay','Future']:
            for v in ['thetao','so']:
                NDF=[];TREND=[];TREND_CTRL=[];PVAL=[];DTIME=[]
                for model in ModelList:
                    ctrl_ref=tb.find(variable=v,model=model,name=time_frame+'_ref_ctrl')
                    fcst_ref=tb.find(variable=v,model=model,name=time_frame+'_ref')
                    fcst_ctrl=tb.find(variable=v,model=model,name=time_frame+'_ctrl')
                    fcst=tb.find(variable=v,model=model,name=time_frame)
                    flist_ctrl_ref=load_file_list(ctrl_ref)
                    flist_ref=load_file_list(fcst_ref)
                    flist_ctrl=load_file_list(fcst_ctrl)
                    flist=load_file_list(fcst)
                    CR=load_tracer(flist_ctrl_ref,grid=grid_woa,field=v)
                    PR=load_tracer(flist_ref,grid=grid_woa,field=v)
                    CF=load_tracer(flist_ctrl,grid=grid_woa,field=v)
                    PF=load_tracer(flist,grid=grid_woa,field=v)
                    zonal_avg(CR,field=v,normalize=True,basin=basin,basin_mask=reg_id)
                    zonal_avg(PR,field=v,normalize=True,basin=basin,basin_mask=reg_id)
                    zonal_avg(CF,field=v,normalize=True,basin=basin,basin_mask=reg_id)
                    zonal_avg(PF,field=v,normalize=True,basin=basin,basin_mask=reg_id)
                    for c in [CR,PR,CF,PF]:
                        if len(c)==0:
                            print 'THERE IS A PROBLEM WITH MODEL : ',model,' FOR ',time_frame,' ',v,' : data appears to be missing'
                            raise()
                    ndf=len(CR)+len(PR)+len(CF)+len(PF)-3
                    print v,len(CR),len(PR),len(CF),len(PF)
                    NDF.append(ndf)
                    va=v+'_masked_xav'
                    trend,trend_ctrl,pval=ensemble_trend(grid_woa,CR,PR,CF,PF,va)
                    TREND.append(trend)
                    TREND_CTRL.append(trend_ctrl)
                    PVAL.append(pval)
                    DTIME.append(CF[0].var_dict[v]['dates'][0].year-CR[0].var_dict[v]['dates'][0].year)
                S=state(grid=grid_woa,verbose=False)
                vd=PF[0].var_dict[v].copy()
                TREND=np.asarray(TREND)
                trend=np.mean(TREND,axis=0)
                TREND_CTRL=np.asarray(TREND_CTRL)
                trend_ctrl=np.mean(TREND_CTRL,axis=0)
                PVAL=np.asarray(PVAL)
                NDF=np.asarray(NDF)
                S.add_field_from_array(trend,'delta',var_dict=vd)
                S.add_field_from_array(trend_ctrl,'delta_ctrl',var_dict=vd)
                t2,pval=stats.ttest_ind(TREND,TREND_CTRL,axis=0)
                pval[np.isnan(pval)]=0.0
                vd['units']='none'
                S.add_field_from_array(pval,'pval',var_dict=vd)
                entry=dict(variable=v,state=S,ndf=NDF,nyears=DTIME[0])
                Result.append(entry)
        WOA.adjust_thickness('thetao')
        WOA.adjust_thickness('so')
        zonal_avg([WOA],field='thetao',normalize=True,basin=basin,basin_mask=reg_id)
        zonal_avg([WOA],field='so',normalize=True,basin=basin,basin_mask=reg_id)
        thetao=Result[0]
        so=Result[1]
        tit=region+' Present Day Change in Zonal Avg Temperature (degC/50years)'
        show_zonal_trend(thetao['state'],so['state'],WOA,field='thetao',title=tit,vmin=-5,vmax=5,cmap=plt.cm.bwr,nyears=thetao['nyears'],fname=region+'_zonal_thetao_present.png',ndf=thetao['ndf'],ModelList=ModelList,pval_tol=0.05)
        tit=region+' Present Day Change in Zonal Avg Salinity (PSU/50years)'
        show_zonal_trend(thetao['state'],so['state'],WOA,field='so',title=tit,vmin=-.5,vmax=.5,cmap=plt.cm.bwr,nyears=thetao['nyears'],fname=region+'_zonal_so_present.png',ndf=thetao['ndf'],ModelList=ModelList,pval_tol=0.05)
#        tit=region+' Present Day Change in Zonal Avg Density Anomaly (kg/m3/50years)'
#        show_zonal_trend(thetao['state'],so['state'],WOA,field='sigma1',title=tit,vmin=-.5,vmax=.5,cmap=plt.cm.bwr,nyears=thetao['nyears'],fname=region+'_zonal_sigma_present.png',ndf=thetao['ndf'],ModelList=ModelList,pval_tol=0.05)
        thetao=Result[2]
        so=Result[3]
        tit=region+' Future Change in Zonal Avg Temperature (degC/50years)'
        show_zonal_trend(thetao['state'],so['state'],WOA,field='thetao',title=tit,vmin=-5,vmax=5,cmap=plt.cm.bwr,nyears=thetao['nyears'],fname=region+'_zonal_thetao_future.png',ndf=thetao['ndf'],ModelList=ModelList,pval_tol=0.05)
        tit=region+' Future Change in Zonal Avg Salinity (PSU/50years)'
        show_zonal_trend(thetao['state'],so['state'],WOA,field='so',title=tit,vmin=-.5,vmax=.5,cmap=plt.cm.bwr,nyears=thetao['nyears'],fname=region+'_zonal_so_future.png',ndf=thetao['ndf'],ModelList=ModelList,pval_tol=0.05)


if args.type == 'zonal_density_sections':
    for region,reg_id in zip(['Global','Atlantic','Pacific','Indian'],[None,2,3,5]):
        Result=[]
        for time_frame in ['PresentDay','Future']:
            for v in ['sigma']:
                NDF=[];TREND=[];TREND_CTRL=[];PVAL=[];DTIME=[]
                for model in ModelList:
                    ctrl_ref=tb.find(variable=v,model=model,name=time_frame+'_ref_ctrl')
                    fcst_ref=tb.find(variable=v,model=model,name=time_frame+'_ref')
                    fcst_ctrl=tb.find(variable=v,model=model,name=time_frame+'_ctrl')
                    fcst=tb.find(variable=v,model=model,name=time_frame)
                    flist_ctrl_ref=load_file_list(ctrl_ref)
                    flist_ref=load_file_list(fcst_ref)
                    flist_ctrl=load_file_list(fcst_ctrl)
                    flist=load_file_list(fcst)
                    CR=load_tracer(flist_ctrl_ref,grid=grid_woa,field=v)
                    PR=load_tracer(flist_ref,grid=grid_woa,field=v)
                    CF=load_tracer(flist_ctrl,grid=grid_woa,field=v)
                    PF=load_tracer(flist,grid=grid_woa,field=v)
                    zonal_avg(CR,field=v,normalize=True,basin=basin,basin_mask=reg_id)
                    zonal_avg(PR,field=v,normalize=True,basin=basin,basin_mask=reg_id)
                    zonal_avg(CF,field=v,normalize=True,basin=basin,basin_mask=reg_id)
                    zonal_avg(PF,field=v,normalize=True,basin=basin,basin_mask=reg_id)
                    for c in [CR,PR,CF,PF]:
                        if len(c)==0:
                            print 'THERE IS A PROBLEM WITH MODEL : ',model,' FOR ',time_frame,' ',v,' : data appears to be missing'
                            raise()
                    ndf=len(CR)+len(PR)+len(CF)+len(PF)-3
                    print v,len(CR),len(PR),len(CF),len(PF)
                    NDF.append(ndf)
                    va=v+'_masked_xav'
                    trend,trend_ctrl,pval=ensemble_trend(grid_woa,CR,PR,CF,PF,va)
                    TREND.append(trend)
                    TREND_CTRL.append(trend_ctrl)
                    PVAL.append(pval)
                    DTIME.append(CF[0].var_dict[v]['dates'][0].year-CR[0].var_dict[v]['dates'][0].year)
                S=state(grid=grid_woa,verbose=False)
                vd=PF[0].var_dict[v].copy()
                TREND=np.asarray(TREND)
                trend=np.mean(TREND,axis=0)
                TREND_CTRL=np.asarray(TREND_CTRL)
                trend_ctrl=np.mean(TREND_CTRL,axis=0)
                PVAL=np.asarray(PVAL)
                NDF=np.asarray(NDF)
                S.add_field_from_array(trend,'delta',var_dict=vd)
                S.add_field_from_array(trend_ctrl,'delta_ctrl',var_dict=vd)
                t2,pval=stats.ttest_ind(TREND,TREND_CTRL,axis=0)
                pval[np.isnan(pval)]=0.0
                vd['units']='none'
                S.add_field_from_array(pval,'pval',var_dict=vd)
                entry=dict(variable=v,state=S,ndf=NDF,nyears=DTIME[0])
                Result.append(entry)
        WOA.adjust_thickness('sigma')
        zonal_avg([WOA],field='sigma',normalize=True,basin=basin,basin_mask=reg_id)
        sigma=Result[0]
        tit=region+' Present Day Change in Zonal Avg Density Anomaly (kg/m3/50years)'
        show_zonal_trend(sigma['state'],sigma['state'],WOA,field='sigma',title=tit,vmin=-1,vmax=1,cmap=plt.cm.bwr,nyears=sigma['nyears'],fname=region+'_zonal_sigma_present.png',ndf=sigma['ndf'],ModelList=ModelList,pval_tol=0.05)
#        tit=region+' Present Day Change in Zonal Avg Density Anomaly (kg/m3/50years)'
#        show_zonal_trend(thetao['state'],so['state'],WOA,field='sigma1',title=tit,vmin=-.5,vmax=.5,cmap=plt.cm.bwr,nyears=thetao['nyears'],fname=region+'_zonal_sigma_present.png',ndf=thetao['ndf'],ModelList=ModelList,pval_tol=0.05)
        sigma=Result[1]
        tit=region+' Future Change in Zonal Avg Density Anomaly (kg/m3/50years)'
        show_zonal_trend(sigma['state'],sigma['state'],WOA,field='sigma',title=tit,vmin=-1,vmax=1,cmap=plt.cm.bwr,nyears=sigma['nyears'],fname=region+'_zonal_sigma_future.png',ndf=sigma['ndf'],ModelList=ModelList,pval_tol=0.05)

#        tit=region+' Future Change in Zonal Avg Density Anomaly (kg/m3/50years)'
#        show_zonal_trend(thetao['state'],so['state'],WOA,field='sigma1',title=tit,vmin=-.5,vmax=.5,cmap=plt.cm.bwr,nyears=thetao['nyears'],fname=region+'_zonal_sigma_future.png',ndf=thetao['ndf'],ModelList=ModelList,pval_tol=0.05)


#    if args.type == 'salt_maps':
#        thetao=Result[0]
#        so=Result[1]
#        sfc_trend(so['state'],field='so',title='Present Day SSS change (psu)',vmin=-1,vmax=1,cmap=plt.cm.bwr,fname='sss_present.png')
#        thetao=Result[2]
#        so=Result[3]
#        sfc_trend(so['state'],field='so',title='Future SSS change (psu)',vmin=-2,vmax=2,cmap=plt.cm.bwr,fname='sss_future.png')
