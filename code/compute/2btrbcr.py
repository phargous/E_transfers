import os
import numpy as np
import xarray as xr
import gsw


datasets = [
    {
        "path": "../../data/001_030_glorys_uovo_sal_temp_boT_mld_zos.nc",
        "u": "uo",
        "v": "vo",
        "T": "thetao",
        "S": "so"
    },
    {
        "path": "../../data/001_031_ensemble_uovo_sal_temp_mld_zos.nc",
        "u": "uo_mean",
        "v": "vo_mean",
        "T": "thetao_mean",
        "S": "so_mean"
    }
]


def compute_btr_bcr(ds, u_name, v_name, T_name, S_name):

    # --- rename standard ---
    ds = ds.rename({'longitude': 'lon', 'latitude': 'lat'})
    if "depth" in ds.dims:
        ds = ds.squeeze("depth", drop=True)

    # --- variables ---
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

    dx = xr.DataArray(dx, coords={"lat": ds.lat, "lon": ds.lon}, dims=("lat","lon"))
    dy = xr.DataArray(dy, coords={"lat": ds.lat, "lon": ds.lon}, dims=("lat","lon"))

    # ======================
    # BTR
    # ======================

    umean = u.mean("time")
    vmean = v.mean("time")

    uprime = u - umean
    vprime = v - vmean

    uu = uprime**2
    vv = vprime**2
    uv = uprime * vprime

    dudx = umean.differentiate("lon") / dx
    dudy = umean.differentiate("lat") / dy
    dvdx = vmean.differentiate("lon") / dx
    dvdy = vmean.differentiate("lat") / dy

    btr = -(uu*dudx + uv*(dvdx+dudy) + vv*dvdy)
    btrm = btr.mean("time")

    # ======================
    # BCR
    # ======================

    lon2d, lat2d = np.meshgrid(ds.lon.values, ds.lat.values)

    SA = gsw.SA_from_SP(S, 0, lon2d, lat2d)
    CT = gsw.CT_from_pt(SA, T)
    rho = gsw.rho(SA, CT, 0)

    rho0 = 1025
    g = 9.81

    b = -g * (rho - rho0) / rho0
    bprime = b - b.mean("time")

    ub = uprime * bprime
    vb = vprime * bprime

    dbdx = b.mean("time").differentiate("lon") / dx
    dbdy = b.mean("time").differentiate("lat") / dy

    bcr = -(ub * dbdx + vb * dbdy)
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

    out["btr"].attrs["long_name"] = "Barotropic conversion rate m² s⁻³"
    out["bcr"].attrs["long_name"] = "Baroclinic conversion rate (surface buoyancy flux proxy) m² s⁻³"
    out["btrm"].attrs["long_name"] = "Mean barotropic conversion rate m² s⁻³"
    out["bcrm"].attrs["long_name"] = "Mean baroclinic conversion rate (surface buoyancy flux proxy) m² s⁻³"

    return out



for ds_info in datasets:

    print(f"Processing {ds_info['path']}")

    ds = xr.open_dataset(ds_info["path"])

    result = compute_btr_bcr(
        ds,
        ds_info["u"],
        ds_info["v"],
        ds_info["T"],
        ds_info["S"]
    )

    # save result
    out_path = ds_info["path"].replace(".nc", "_btr_bcr.nc")
    result.to_netcdf(out_path)
    print(f"Saved result to {out_path}")
    del result