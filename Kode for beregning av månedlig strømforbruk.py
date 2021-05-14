# -*- coding: utf-8 -*-
"""
Created on Fri May 14 15:29:02 2021

@author: torst
"""

Hele={
  "inputs": {
    "location": {
      "latitude": 63.428,
      "longitude": 10.385,
      "elevation": 20
    },
    "meteo_data": {
      "radiation_db": "PVGIS-ERA5",
      "meteo_db": "ERA-Interim",
      "year_min": 2005,
      "year_max": 2016,
      "use_horizon": True,
      "horizon_db": "DEM-calculated"
    },
    "mounting_system": {
      "vertical_axis": {
        "slope": {
          "value": 20,
          "optimal": False
        },
        "azimuth": {
          "value": "-",
          "optimal": "-"
        }
      }
    },
    "pv_module": {
      "technology": "c-Si",
      "peak_power": 22.7,
      "system_loss": 14
    },
    "economic_data": {
      "system_cost": None,
      "interest": None,
      "lifetime": None
    }
  },
  "outputs": {
    "monthly": {
      "vertical_axis": [
        {
          "month": "Januar",
          "E_d": 6.4,
          "E_m": 198.25,
          "H(i)_d": 0.38,
          "H(i)_m": 11.69,
          "SD_m": 72.99
        },
        {
          "month": "Februar",
          "E_d": 26.18,
          "E_m": 732.99,
          "H(i)_d": 1.38,
          "H(i)_m": 38.78,
          "SD_m": 136.95
        },
        {
          "month": "Mars",
          "E_d": 60.31,
          "E_m": 1869.76,
          "H(i)_d": 3.13,
          "H(i)_m": 96.95,
          "SD_m": 406.2
        },
        {
          "month": "April",
          "E_d": 94.87,
          "E_m": 2846.08,
          "H(i)_d": 4.98,
          "H(i)_m": 149.55,
          "SD_m": 353.52
        },
        {
          "month": "Mai",
          "E_d": 118.75,
          "E_m": 3681.36,
          "H(i)_d": 6.36,
          "H(i)_m": 197.27,
          "SD_m": 211.42
        },
        {
          "month": "Juni",
          "E_d": 114.78,
          "E_m": 3443.48,
          "H(i)_d": 6.28,
          "H(i)_m": 188.28,
          "SD_m": 454.57
        },
        {
          "month": "Juli",
          "E_d": 107.62,
          "E_m": 3336.33,
          "H(i)_d": 5.98,
          "H(i)_m": 185.32,
          "SD_m": 587.14
        },
        {
          "month": "August",
          "E_d": 86.8,
          "E_m": 2690.85,
          "H(i)_d": 4.8,
          "H(i)_m": 148.82,
          "SD_m": 360.2
        },
        {
          "month": "September",
          "E_d": 57.01,
          "E_m": 1710.35,
          "H(i)_d": 3.12,
          "H(i)_m": 93.64,
          "SD_m": 250.48
        },
        {
          "month": "Oktober",
          "E_d": 32.13,
          "E_m": 996,
          "H(i)_d": 1.75,
          "H(i)_m": 54.29,
          "SD_m": 220.94
        },
        {
          "month": "November",
          "E_d": 9.7,
          "E_m": 291.01,
          "H(i)_d": 0.56,
          "H(i)_m": 16.9,
          "SD_m": 68.04
        },
        {
          "month": "Desember",
          "E_d": 2.02,
          "E_m": 62.71,
          "H(i)_d": 0.14,
          "H(i)_m": 4.39,
          "SD_m": 21.39
        }
      ]
    },
    "totals": {
      "vertical_axis": {
        "E_d": 59.89,
        "E_m": 1821.6,
        "E_y": 21859.16,
        "H(i)_d": 3.25,
        "H(i)_m": 98.82,
        "H(i)_y": 1185.87,
        "SD_m": 101.06,
        "SD_y": 1212.74,
        "l_aoi": -2.56,
        "l_spec": "?(0)",
        "l_tg": -3.1,
        "l_total": -18.8
      }
    }
  },
  "meta": {
    "inputs": {
      "location": {
        "description": "Selected location",
        "variables": {
          "latitude": {
            "description": "Latitude",
            "units": "decimal degree"
          },
          "longitude": {
            "description": "Longitude",
            "units": "decimal degree"
          },
          "elevation": {
            "description": "Elevation",
            "units": "m"
          }
        }
      },
      "meteo_data": {
        "description": "Sources of meteorological data",
        "variables": {
          "radiation_db": {
            "description": "Solar radiation database"
          },
          "meteo_db": {
            "description": "Database used for meteorological variables other than solar radiation"
          },
          "year_min": {
            "description": "First year of the calculations"
          },
          "year_max": {
            "description": "Last year of the calculations"
          },
          "use_horizon": {
            "description": "Include horizon shadows"
          },
          "horizon_db": {
            "description": "Source of horizon data"
          }
        }
      },
      "mounting_system": {
        "description": "Mounting system",
        "choices": "fixed, vertical_axis, inclined_axis, two_axis",
        "fields": {
          "slope": {
            "description": "Inclination angle from the horizontal plane",
            "units": "degree"
          },
          "azimuth": {
            "description": "Orientation (azimuth) angle of the (fixed) PV system (0 = S, 90 = W, -90 = E)",
            "units": "degree"
          }
        }
      },
      "pv_module": {
        "description": "PV module parameters",
        "variables": {
          "technology": {
            "description": "PV technology"
          },
          "peak_power": {
            "description": "Nominal (peak) power of the PV module",
            "units": "kW"
          },
          "system_loss": {
            "description": "Sum of system losses",
            "units": "%"
          }
        }
      },
      "economic_data": {
        "description": "Economic inputs",
        "variables": {
          "system_cost": {
            "description": "Total cost of the PV system",
            "units": "user-defined currency"
          },
          "interest": {
            "description": "Annual interest",
            "units": "%/y"
          },
          "lifetime": {
            "description": "Expected lifetime of the PV system",
            "units": "y"
          }
        }
      }
    },
    "outputs": {
      "monthly": {
        "type": "time series",
        "timestamp": "monthly averages",
        "variables": {
          "E_d": {
            "description": "Average daily energy production from the given system",
            "units": "kWh/d"
          },
          "E_m": {
            "description": "Average monthly energy production from the given system",
            "units": "kWh/mo"
          },
          "H(i)_d": {
            "description": "Average daily sum of global irradiation per square meter received by the modules of the given system",
            "units": "kWh/m2/d"
          },
          "H(i)_m": {
            "description": "Average monthly sum of global irradiation per square meter received by the modules of the given system",
            "units": "kWh/m2/mo"
          },
          "SD_m": {
            "description": "Standard deviation of the monthly energy production due to year-to-year variation",
            "units": "kWh"
          }
        }
      },
      "totals": {
        "type": "time series totals",
        "variables": {
          "E_d": {
            "description": "Average daily energy production from the given system",
            "units": "kWh/d"
          },
          "E_m": {
            "description": "Average monthly energy production from the given system",
            "units": "kWh/mo"
          },
          "E_y": {
            "description": "Average annual energy production from the given system",
            "units": "kWh/y"
          },
          "H(i)_d": {
            "description": "Average daily sum of global irradiation per square meter received by the modules of the given system",
            "units": "kWh/m2/d"
          },
          "H(i)_m": {
            "description": "Average monthly sum of global irradiation per square meter received by the modules of the given system",
            "units": "kWh/m2/mo"
          },
          "H(i)_y": {
            "description": "Average annual sum of global irradiation per square meter received by the modules of the given system",
            "units": "kWh/m2/y"
          },
          "SD_m": {
            "description": "Standard deviation of the monthly energy production due to year-to-year variation",
            "units": "kWh"
          },
          "SD_y": {
            "description": "Standard deviation of the annual energy production due to year-to-year variation",
            "units": "kWh"
          },
          "l_aoi": {
            "description": "Angle of incidence loss",
            "units": "%"
          },
          "l_spec": {
            "description": "Spectral loss",
            "units": "%"
          },
          "l_tg": {
            "description": "Temperature and irradiance loss",
            "units": "%"
          },
          "l_total": {
            "description": "Total loss",
            "units": "%"
          }
        }
      }
    }
  }
}
 
Inputs=Hele["inputs"]
 
Outputs=Hele["outputs"]
 
Monthly= Outputs["monthly"]
 
V_axis= Monthly["vertical_axis"]
 
Januar=V_axis[0]
 
Februr=V_axis[1]
 
Mars=V_axis[2]
 
April=V_axis[3]
 
Mai=V_axis[4]
 
Juni=V_axis[5]
 
Juli=V_axis[6]
 
August=V_axis[7]
 
September=V_axis[8]
 
Oktober=V_axis[9]
 
November=V_axis[10]
 
Desember=V_axis[11]
 
 
 
print(Februr["E_m"])
liste_per_mnd = []
for i in range(12):
    month = V_axis[i]
    liste_per_mnd.append(month["E_m"])
 
print(liste_per_mnd)
årlig = sum(liste_per_mnd)
print(årlig,"kWh Årlig produksjon")
 
 
 
import matplotlib.pyplot as plt #Importerer for å kunne plotte
 
 
 
# x-kordinater
left = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
 
#Høyde 
 
 
height = [198.25, 732.99, 1869.76, 2846.08, 3681.36, 3443.48, 3336.33, 2690.85, 1710.35, 996, 291.01, 62.71]
# labels for bars
tick_label = ["Jan","Feb","Mars","Apr","Mai","Juni","Juli","Aug","Sep","Okt","Nov","Des"]
 
# Hvordan "barene" skla se ut
plt.bar(left, height, tick_label = tick_label,
        width = 0.8, color = ['red', 'green'])
 
# navn på x-aksen
plt.xlabel('Måneder')
# y-aksen
plt.ylabel('Solpanel energi produksjon [Wt]')
# overskrift
plt.title("Energi produsert pr måned")
 
#plt.grid() 
# for å vise plottet
plt.show()