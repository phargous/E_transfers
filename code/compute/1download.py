import copernicusmarine
import numpy as np
import xarray as xr
import os
import sys
sys.path.append('../')
import time
from datetime import datetime, timedelta

from unittest.mock import patch

# # Mediterranean Sea Physics Reanalysis MED MFC
# copernicusmarine.subset(
#       dataset_id="cmems_mod_med_phy-cur_my_4.2km_P1D-m",
#       variables=["uo", "vo"],
#     #   minimum_longitude=-9.0625,
#     #   maximum_longitude=10.0625,
#     #   minimum_latitude=32,
#     #   maximum_latitude=45,
#       start_datetime='1993-01-01T00:00:00',
#       end_datetime='2026-04-30T23:59:59',
#       minimum_depth=1.0182366371154785,
#       maximum_depth=1.0182366371154785,
#       output_filename = '006_004_medmfc_uovo.nc',
#       output_directory = '../../data/',
#       force_download=True,
#     )


# # Global Ocean Ensemble Physics Reanalysis Ensemble
# copernicusmarine.subset(
#       dataset_id="cmems_mod_glo_phy-mnstd_my_0.25deg_P1D-m",
#       variables=["mlotst_mean", "mlotst_std", "uo_mean", "uo_std", "vo_mean", "vo_std", "zos_mean", "zos_std", "thetao_mean", "thetao_std", "so_mean", "so_std"],    #   minimum_longitude=-9.0625,
#       minimum_longitude=-10,
#       maximum_longitude=37,
#       minimum_latitude=30,
#       maximum_latitude=47,
#       start_datetime='1993-01-01T00:00:00',
#       end_datetime='2024-12-31T23:59:59',
#       minimum_depth=0.5057600140571594,
#       maximum_depth=0.5057600140571594,
#       output_filename = '001_031_ensemble_uovo_sal_temp_mld_zos.nc',
#       output_directory = '../../data/',
#       force_download=True,
#     )


# # Global Ocean Physics Reanalysis GLORYS12V1
# copernicusmarine.subset(
#       dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
#       variables=["bottomT", "mlotst", "so", "thetao", "uo", "vo", "zos"],
#       minimum_longitude=-10,
#       maximum_longitude=37,
#       minimum_latitude=30,
#       maximum_latitude=47,
#       start_datetime='1993-01-01T00:00:00',
#       end_datetime='2026-04-28T23:59:59',
#       minimum_depth=0.49402499198913574,
#       maximum_depth=0.49402499198913574,
#       output_filename = '001_030_glorys_uovo_sal_temp_boT_mld_zos.nc',
#       output_directory = '../../data/',
#       force_download=True,
#     )


# Mediterranean Sea Physics Reanalysis MED MFC sal et temp
# copernicusmarine.subset(
#       dataset_id="cmems_mod_med_phy-sal_my_4.2km_P1D-m",
#       variables=["so"],
#     #   minimum_longitude=-9.0625,
#     #   maximum_longitude=10.0625,
#     #   minimum_latitude=32,
#     #   maximum_latitude=45,
#       start_datetime='1993-01-01T00:00:00',
#       end_datetime='2026-04-30T23:59:59',
#       minimum_depth=1.0182366371154785,
#       maximum_depth=1.0182366371154785,
#       output_filename = '006_004_medmfc_so.nc',
#       output_directory = '../../data/',
#       force_download=True,
#     )
# copernicusmarine.subset(
#       dataset_id="cmems_mod_med_phy-temp_my_4.2km_P1D-m",
#       variables=["thetao"],
#     #   minimum_longitude=-9.0625,
#     #   maximum_longitude=10.0625,
#     #   minimum_latitude=32,
#     #   maximum_latitude=45,
#       start_datetime='1993-01-01T00:00:00',
#       end_datetime='2026-04-30T23:59:59',
#       minimum_depth=1.0182366371154785,
#       maximum_depth=1.0182366371154785,
#       output_filename = '006_004_medmfc_thetao.nc',
#       output_directory = '../../data/',
#       force_download=True,
#     )