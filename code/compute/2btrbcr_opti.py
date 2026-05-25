import os
import numpy as np
import xarray as xr
import gsw
import time

start_time = time.time()
# ======================
# DATASETS CONFIG
# ======================

#111111111
# datasets = [
#     {
#         "path": "../../data/001_030_glorys_uovo_sal_temp_boT_mld_zos.nc",
#         "u": "uo",
#         "v": "vo",
#         "T": "thetao",
#         "S": "so"
#     },
#     {
#         "path": "../../data/001_031_ensemble_uovo_sal_temp_mld_zos.nc",
#         "u": "uo_mean",
#         "v": "vo_mean",
#         "T": "thetao_mean",
#         "S": "so_mean"
#     }
# ]

#222222222
datasets = [
    {
        "path": "../../data/006_004_medmfc_uovo.nc",
        "S_path": "../../data/006_004_medmfc_so.nc",
        "T_path": "../../data/006_004_medmfc_thetao.nc",
        "u": "uo",
        "v": "vo",
        "T": "thetao",
        "S": "so"
    }
]

# ======================
# CORE FUNCTION
# ======================

def compute_btr_bcr(ds, u_name, v_name, T_name, S_name):

    # --- standardize coords ---
    ds = ds.rename({'longitude': 'lon', 'latitude': 'lat'})
    if "depth" in ds.dims:
        ds = ds.squeeze("depth", drop=True)

    u = ds[u_name]
    v = ds[v_name]
    T = ds[T_name]
    S = ds[S_name]

    # ======================
    # METRICS
    # ======================

    R = 6371000

    lat = ds.lat.values
    lon = ds.lon.values

    lat_rad = np.deg2rad(lat)
    lon_rad = np.deg2rad(lon)

    dlat = np.gradient(lat_rad)
    dlon = np.gradient(lon_rad)

    dx = R * np.cos(lat_rad)[:, None] * dlon
    dy = R * dlat[:, None]
    dy = np.repeat(dy, len(lon), axis=1)

    dx = xr.DataArray(dx, coords={"lat": ds.lat, "lon": ds.lon}, dims=("lat", "lon"))
    dy = xr.DataArray(dy, coords={"lat": ds.lat, "lon": ds.lon}, dims=("lat", "lon"))

    # ======================
    # BTR
    # ======================

    umean = u.mean("time")
    vmean = v.mean("time")

    uprime = u - umean
    vprime = v - vmean

    dudx = umean.differentiate("lon") / dx
    dudy = umean.differentiate("lat") / dy
    dvdx = vmean.differentiate("lon") / dx
    dvdy = vmean.differentiate("lat") / dy

    btr = -(
        (uprime**2) * dudx +
        (uprime * vprime) * (dvdx + dudy) +
        (vprime**2) * dvdy
    )

    btrm = btr.mean("time")

    # ======================
    # BCR (DASK-compatible TEOS)
    # ======================

    lon2d, lat2d = np.meshgrid(ds.lon.values, ds.lat.values)

    SA = xr.apply_ufunc(
        gsw.SA_from_SP,
        S,
        0,
        lon2d,
        lat2d,
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float],
    )

    CT = xr.apply_ufunc(
        gsw.CT_from_pt,
        SA,
        T,
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float],
    )

    rho = xr.apply_ufunc(
        gsw.rho,
        SA,
        CT,
        0,
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float],
    )

    rho0 = 1025
    g = 9.81

    b = -g * (rho - rho0) / rho0

    bmean = b.mean("time")
    bprime = b - bmean

    dbdx = bmean.differentiate("lon") / dx
    dbdy = bmean.differentiate("lat") / dy

    bcr = -(uprime * bprime * dbdx + vprime * bprime * dbdy)
    bcrm = bcr.mean("time")

    # ======================
    # OUTPUT
    # ======================

    out = xr.Dataset({
        "btr": btr,
        "btrm": btrm,
        "bcr": bcr,
        "bcrm": bcrm,
    })

    # metadata
    out["btr"].attrs["long_name"] = "Barotropic conversion rate (m^2 s^-3)"
    out["bcr"].attrs["long_name"] = "Baroclinic conversion rate (m^2 s^-3)"
    out["btrm"].attrs["long_name"] = "Mean barotropic conversion rate (m^2 s^-3)"
    out["bcrm"].attrs["long_name"] = "Mean baroclinic conversion rate (m^2 s^-3)"

    return out


# ======================
# LOOP (OPTIMIZED)
# ======================

for ds_info in datasets:

    print(f"\nProcessing {ds_info['path']}")
    #111111111
    # ds = xr.open_dataset(
    #     ds_info["path"],
    #     chunks={"time": 50}   # clé pour gros fichiers
    # )

    #222222222
    ds_u = xr.open_dataset(ds_info["path"], chunks={"time": 50})
    ds_T = xr.open_dataset(ds_info["T_path"], chunks={"time": 50})
    ds_S = xr.open_dataset(ds_info["S_path"], chunks={"time": 50})
    ds = xr.merge([ds_u, ds_T, ds_S])


    result = compute_btr_bcr(
        ds,
        ds_info["u"],
        ds_info["v"],
        ds_info["T"],
        ds_info["S"],
    )

    # compression pour gros fichiers
    encoding = {var: {"zlib": True, "complevel": 4} for var in result.data_vars}

    out_path = ds_info["path"].replace(".nc", "_btr_bcr.nc")

    print("Saving...")
    result.to_netcdf(out_path, encoding=encoding)

    print(f"Saved to {out_path}")

    del result


end_time = time.time()
execution_time = end_time - start_time
print(f"Time: {execution_time} seconds")