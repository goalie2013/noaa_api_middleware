from enum import Enum
from pydantic import BaseModel

class Queries(BaseModel):
    startdate: str
    enddate: str
    offset: int = 0
    limit: int = 50
    datatypeid: str | None = None
    options: object | None = None
    


class ResModel(BaseModel):
    date: str
    value: int
    id: str | None = None
    name: str | None = None
    
  
  
class DatasetParameter(str, Enum):
    SUMMARY = "summary"
    WEATHER_RADAR_TWO = "radar2"
    WEATHER_RADAR_THREE = "radar3"
    CLIMATE_NORMALS = "climate"
    PRECIP = "ppt"
    

class SummaryParameter(str, Enum):
    DAILY_SUMM = "daily"
    MONTHLY_SUMM = "monthly"
    YEARLY_SUMM = "yearly"

#class RadarParameter(str, Enum):
#    WEATHER_RADAR_TWO = "2"
#    WEATHER_RADAR_THREE = "3"
    
class ClimateParameter(str, Enum):
    CLIMATE_NORMALS_HOUR = "hour"
    CLIMATE_NORMALS_DAY = "day"
    CLIMATE_NORMALS_MONTH = "month"
    CLIMATE_NORMALS_YEAR = "year"
   
class PptParameter(str, Enum):
     PRECIP_15_MIN = "15"
     PRECIP_HOUR = "hourly"
     


# Link Enums w/ API dataset IDs in a dictionary
datasets = {
    SummaryParameter.DAILY_SUMM: "GHCND",
    SummaryParameter.MONTHLY_SUMM: "GSOM",
    SummaryParameter.YEARLY_SUMM: "GSOY",
    DatasetParameter.WEATHER_RADAR_TWO: "NEXRAD2",
    DatasetParameter.WEATHER_RADAR_THREE: "NEXRAD3",
    ClimateParameter.CLIMATE_NORMALS_HOUR: "NORMAL_HLY",
    ClimateParameter.CLIMATE_NORMALS_DAY: "NORMAL_DLY",
    ClimateParameter.CLIMATE_NORMALS_MONTH: "NORMAL_MLY",
    ClimateParameter.CLIMATE_NORMALS_YEAR: "NORMAL_ANN",
    PptParameter.PRECIP_15_MIN: "PRECIP_15",
    PptParameter.PRECIP_HOUR: "PRECIP_HLY"
}

class EE(str, Enum):
    DAILY_SUMM = "ghcnd",
    MONTHLY_SUMM = "gsom",
    YEARLY_SUMM = "gsoy",
    WEATHER_RADAR_TWO = "nexrad2",
    WEATHER_RADAR_THREE = "nexrad3",
    CLIMATE_NORMALS_HOUR = "normal_hly",
    CLIMATE_NORMALS_DAY = "normal_dly",
    CLIMATE_NORMALS_MONTH = "normal_mly",
    CLIMATE_NORMALS_YEAR = "normal_ann",
    PRECIP_15_MIN = "precip_15",
    PRECIP_HOUR = "precip_hly"