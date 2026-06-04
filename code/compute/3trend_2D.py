import os
import sys
sys.path.append('../')
import numpy as np
import xarray as xr
import pymk as pymk
import time


#################################### NON OPTIMISED VERSION ####################################
# start_time1 = time.time()

# def pmk_test(ts):
#     if np.isnan(ts).all():
#         return np.nan, np.nan, np.nan, np.nan
#     results = pymk.yue_wang_modification_test(ts)
#     slope, p_value, n_ns, intercept = results.slope, results.p, results.n_ns, results.intercept
#     return slope, p_value, n_ns, intercept


# sat = xr.open_dataset('../../results/btr_med_sat.nc')
# glorys = xr.open_dataset('../../results/001_030_glorys_btr_bcr.nc')
# ensemble = xr.open_dataset('../../results/001_031_ensemble_btr_bcr.nc')
# ww = xr.open_dataset('../../results/wind_work_era5.nc')

# a = [np.zeros((len(sat.lat), len(sat.lon))) for _ in range(20)]
# slope_sat, slope_wwt, slope_iww, slope_wwc, slope_curl, pvalue_sat, pvalue_wwt, pvalue_iww, pvalue_wwc, pvalue_curl, nns_sat, nns_wwt, nns_iww, nns_wwc, nns_curl, intercept_sat, intercept_wwt, intercept_iww, intercept_wwc, intercept_curl = a


# for i in range(len(sat.lat)):
#     for j in range(len(sat.lon)):
#         slope_sat[i,j], pvalue_sat[i,j], nns_sat[i,j], intercept_sat[i,j] = pmk_test(sat.btr[:,i,j])
#         slope_wwt[i,j], pvalue_wwt[i,j], nns_wwt[i,j], intercept_wwt[i,j] = pmk_test(ww.wwt[:,i,j])
#         slope_iww[i,j], pvalue_iww[i,j], nns_iww[i,j], intercept_iww[i,j] = pmk_test(ww.iww[:,i,j])
#         slope_wwc[i,j], pvalue_wwc[i,j], nns_wwc[i,j], intercept_wwc[i,j] = pmk_test(ww.wwc[:,i,j])
#         slope_curl[i,j], pvalue_curl[i,j], nns_curl[i,j], intercept_curl[i,j] = pmk_test(ww.curl[:,i,j])

# ds_out = xr.Dataset(
#     {
#         "slope_sat": (("lat", "lon"), slope_sat),
#         "pvalue_sat": (("lat", "lon"), pvalue_sat),
#         "intercept_sat": (("lat", "lon"), intercept_sat),
#         "nns_sat": (("lat", "lon"), nns_sat),
#         "slope_wwt": (("lat", "lon"), slope_wwt),
#         "pvalue_wwt": (("lat", "lon"), pvalue_wwt),
#         "intercept_wwt": (("lat", "lon"), intercept_wwt),
#         "nns_wwt": (("lat", "lon"), nns_wwt),
#         "slope_iww": (("lat", "lon"), slope_iww),
#         "pvalue_iww": (("lat", "lon"), pvalue_iww),
#         "intercept_iww": (("lat", "lon"), intercept_iww),
#         "nns_iww": (("lat", "lon"), nns_iww),
#         "slope_wwc": (("lat", "lon"), slope_wwc),
#         "pvalue_wwc": (("lat", "lon"), pvalue_wwc),
#         "intercept_wwc": (("lat", "lon"), intercept_wwc),
#         "nns_wwc": (("lat", "lon"), nns_wwc),
#         "slope_curl": (("lat", "lon"), slope_curl),
#         "pvalue_curl": (("lat", "lon"), pvalue_curl),
#         "intercept_curl": (("lat", "lon"), intercept_curl),
#         "nns_curl": (("lat", "lon"), nns_curl)
#     },
#     coords={
#         'lat': sat.lat,
#         'lon': sat.lon
#     }
# )
# ds_out.to_netcdf('../../results/trends_sat_btr_ww.nc')


# a = [np.zeros((len(glorys.lat), len(glorys.lon))) for _ in range(8)]
# slope_btr, slope_bcr, pvalue_btr, pvalue_bcr, nns_btr, nns_bcr, intercept_btr, intercept_bcr = a

# for i in range(len(glorys.lat)):
#     for j in range(len(glorys.lon)):
#         slope_btr[i,j], pvalue_btr[i,j], nns_btr[i,j], intercept_btr[i,j] = pmk_test(glorys.btr[:,i,j])
#         slope_bcr[i,j], pvalue_bcr[i,j], nns_bcr[i,j], intercept_bcr[i,j] = pmk_test(glorys.bcr[:,i,j])


# ds_out = xr.Dataset(
#     {
#         "slope_btr": (("lat", "lon"), slope_btr),
#         "pvalue_btr": (("lat", "lon"), pvalue_btr),
#         "intercept_btr": (("lat", "lon"), intercept_btr),
#         "nns_btr": (("lat", "lon"), nns_btr),
#         "slope_bcr": (("lat", "lon"), slope_bcr),
#         "pvalue_bcr": (("lat", "lon"), pvalue_bcr),
#         "intercept_bcr": (("lat", "lon"), intercept_bcr),
#         "nns_bcr": (("lat", "lon"), nns_bcr)
#     },
#     coords={
#         'lat': glorys.lat,
#         'lon': glorys.lon
#     }
# )
# ds_out.to_netcdf('../../results/trends_glorys_btr_bcr.nc')


# a = [np.zeros((len(ensemble.lat), len(ensemble.lon))) for _ in range(8)]
# slope_btr, slope_bcr, pvalue_btr, pvalue_bcr, nns_btr, nns_bcr, intercept_btr, intercept_bcr = a

# for i in range(len(ensemble.lat)):
#     for j in range(len(ensemble.lon)):
#         slope_btr[i,j], pvalue_btr[i,j], nns_btr[i,j], intercept_btr[i,j] = pmk_test(ensemble.btr[:,i,j])
#         slope_bcr[i,j], pvalue_bcr[i,j], nns_bcr[i,j], intercept_bcr[i,j] = pmk_test(ensemble.bcr[:,i,j])


# ds_out = xr.Dataset(
#     {
#         "slope_btr": (("lat", "lon"), slope_btr),
#         "pvalue_btr": (("lat", "lon"), pvalue_btr),
#         "intercept_btr": (("lat", "lon"), intercept_btr),
#         "nns_btr": (("lat", "lon"), nns_btr),
#         "slope_bcr": (("lat", "lon"), slope_bcr),
#         "pvalue_bcr": (("lat", "lon"), pvalue_bcr),
#         "intercept_bcr": (("lat", "lon"), intercept_bcr),
#         "nns_bcr": (("lat", "lon"), nns_bcr)
#     },
#     coords={
#         'lat': ensemble.lat,
#         'lon': ensemble.lon
#     }
# )
# ds_out.to_netcdf('../../results/trends_ensemble_btr_bcr.nc')


# end_time1 = time.time()
# execution_time1 = end_time1 - start_time1
# print(f"Time: {execution_time1} seconds")





#################################### OPTIMISED VERSION ####################################
start_time1 = time.time()

def pmk_test(ts):
    if np.all(np.isnan(ts)):
        return np.nan, np.nan, np.nan, np.nan

    res = pymk.yue_wang_modification_test(ts)
    return res.slope, res.p, res.n_ns, res.intercept

def compute_trend(da):

    slope, pval, nns, intercept = xr.apply_ufunc(
        pmk_test,
        da,
        input_core_dims=[["time"]],
        output_core_dims=[[], [], [], []],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float, float, float, float],
    )

    return slope, pval, nns, intercept


##### sat btr wwt iww wwc curl
sat = xr.open_dataset('../../results/btr_med_sat.nc')
ww  = xr.open_dataset('../../results/wind_work_era5.nc')

slope_sat, p_sat, nns_sat, int_sat = compute_trend(sat.btr)
slope_wwt, p_wwt, nns_wwt, int_wwt = compute_trend(ww.wwt)
slope_iww, p_iww, nns_iww, int_iww = compute_trend(ww.iww)
slope_wwc, p_wwc, nns_wwc, int_wwc = compute_trend(ww.wwc)
slope_curl, p_curl, nns_curl, int_curl = compute_trend(ww.curl)

ds_out = xr.Dataset({
    "slope_sat": slope_sat, "pvalue_sat": p_sat, "intercept_sat": int_sat, "nns_sat": nns_sat,
    "slope_wwt": slope_wwt, "pvalue_wwt": p_wwt, "intercept_wwt": int_wwt, "nns_wwt": nns_wwt,
    "slope_iww": slope_iww, "pvalue_iww": p_iww, "intercept_iww": int_iww, "nns_iww": nns_iww,
    "slope_wwc": slope_wwc, "pvalue_wwc": p_wwc, "intercept_wwc": int_wwc, "nns_wwc": nns_wwc,
    "slope_curl": slope_curl, "pvalue_curl": p_curl, "intercept_curl": int_curl, "nns_curl": nns_curl
})

ds_out.to_netcdf('../../results/trends_sat_btr_ww.nc')
del sat, ww, ds_out
print("Trends computed for sat btr wwt iww wwc curl")

#####glorys btr bcr
glorys = xr.open_dataset('../../results/001_030_glorys_btr_bcr.nc')

slope_btr, p_btr, nns_btr, int_btr = compute_trend(glorys.btr)
slope_bcr, p_bcr, nns_bcr, int_bcr = compute_trend(glorys.bcr)

ds_out = xr.Dataset({
    "slope_btr": slope_btr, "pvalue_btr": p_btr, "intercept_btr": int_btr, "nns_btr": nns_btr,
    "slope_bcr": slope_bcr, "pvalue_bcr": p_bcr, "intercept_bcr": int_bcr, "nns_bcr": nns_bcr
})

ds_out.to_netcdf('../../results/trends_glorys_btr_bcr.nc')
del glorys, ds_out
print("Trends computed for glorys btr bcr")

##### ensemble btr bcr
ensemble = xr.open_dataset('../../results/001_031_ensemble_btr_bcr.nc')

slope_btr, p_btr, nns_btr, int_btr = compute_trend(ensemble.btr)
slope_bcr, p_bcr, nns_bcr, int_bcr = compute_trend(ensemble.bcr)

ds_out = xr.Dataset({
    "slope_btr": slope_btr, "pvalue_btr": p_btr, "intercept_btr": int_btr, "nns_btr": nns_btr,
    "slope_bcr": slope_bcr, "pvalue_bcr": p_bcr, "intercept_bcr": int_bcr, "nns_bcr": nns_bcr
})

ds_out.to_netcdf('../../results/trends_ensemble_btr_bcr.nc')
print("Trends computed for ensemble btr bcr")


end_time1 = time.time()
execution_time1 = end_time1 - start_time1
print(f"Time: {execution_time1} seconds")