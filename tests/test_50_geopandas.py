import gpdbufr
import sys
import os
from pyproj import Geod
from shapely.geometry import Point

SAMPLE_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "sample-data")
TEST_DATA_GEOPANDAS = os.path.join(
    SAMPLE_DATA_FOLDER,
    "Z__C_EDZW_20210516120400_bda01,synop_bufr_GER_999999_999999__MW_466.bin",
)
VERBOSE = True


def distance(center, position):
    g = Geod(ellps="WGS84")
    az12, az21, dist = g.inv(position.x, position.y, center.x, center.y)
    return dist


def readBufrFile(file, columns, filters={}, geopandas=False):
    try:
        if geopandas:
            df_all = gpdbufr.read_geo_bufr(file, columns, filters)
        else:
            df_all = gpdbufr.read_bufr(file, columns, filters)
        return df_all
    except:
        t, v, tb = sys.exc_info()
        sys.stderr.write(f"File={file}: {t} - {v} \n")
        raise


def testPdBufr2GeoPandas(file):
    center = Point([11.010754, 47.800864])  # Hohenpeißenberg
    radius = 100 * 1000  # 100 km
    columnsList = [
        [
            "WMO_station_id",
            "stationOrSiteName",
            "geometry",
            "CRS",
            "typicalDate",
            "typicalTime",
            "timeSignificance",
            "timePeriod",
            "windDirection",
            "windSpeed",
        ],
        [
            "WMO_station_id",
            "stationOrSiteName",
            "latitude",
            "longitude",
            "geometry",
            "CRS",
            "typicalDate",
            "typicalTime",
            "timeSignificance",
            "timePeriod",
            "windDirection",
            "windSpeed",
        ],
        [
            "WMO_station_id",
            "stationOrSiteName",
            "geometry",
            "CRS",
            "typicalDate",
            "typicalTime",
            "timePeriod",
            "windDirection",
            "windSpeed",
        ],
        [
            "WMO_station_id",
            "stationOrSiteName",
            "latitude",
            "longitude",
            "geometry",
            "CRS",
            "typicalDate",
            "typicalTime",
            "timePeriod",
            "windDirection",
            "windSpeed",
        ],
        [
            "WMO_station_id",
            "stationOrSiteName",
            "typicalDate",
            "typicalTime",
            "timePeriod",
            "windDirection",
            "windSpeed",
        ],
    ]
    filtersList = [
        dict(),
        dict(windDirection=float, windSpeed=float),
        dict(
            windDirection=float,
            windSpeed=float,
            geometry=lambda x: distance(center, Point(x)) < radius,
        ),
    ]
    results = []
    for cIndx, columns in enumerate(columnsList):
        for fIndx, filters in enumerate(filtersList):
            for gIndx, geopandas in {"GeoPandas": True, "Pandas": False}.items():
                if VERBOSE:
                    print(f"columns[{cIndx}]={columns}")
                    print(f"filters[{fIndx}]={filters}")
                    print(f"{gIndx} Result")
                rs = readBufrFile(file, columns, filters, geopandas=geopandas)
                if VERBOSE:
                    print(rs)
                results.append(
                    dict(cIndx=cIndx, fIndx=fIndx, gIndx=gIndx, rs=rs, len=len(rs))
                )
                if geopandas and "geometry" in filters:
                    for station in rs.to_records():
                        assert distance(center, station["geometry"]) < radius
                    if VERBOSE:
                        print(f"Distance check (radius = {radius/1000} km) ok")

    if VERBOSE:
        print("Length Checks and DataFrame Checks")

    for indx, test in enumerate(results):
        if test["cIndx"] in [0, 1] and test["fIndx"] == 0:
            results[indx]["awaitedLength"] = 178
        elif test["cIndx"] in [0, 1] and test["fIndx"] == 1:
            results[indx]["awaitedLength"] = 175
        elif test["cIndx"] in [0, 1] and test["fIndx"] == 2:
            results[indx]["awaitedLength"] = 10
        elif test["cIndx"] in [2, 3, 4] and test["fIndx"] == 0:
            results[indx]["awaitedLength"] = 204
        elif test["cIndx"] in [2, 3, 4] and test["fIndx"] == 1:
            results[indx]["awaitedLength"] = 201
        elif test["cIndx"] in [2, 3, 4] and test["fIndx"] == 2:
            results[indx]["awaitedLength"] = 13

        try:
            assert test["len"] == test["awaitedLength"]
        except:
            print(f"assertion in {indx}: {test}")
            raise
        if VERBOSE:
            print(
                f"{test['cIndx']} {test['fIndx']} {test['gIndx']}: Length Check ok ({test['len']})"
            )

        if test["gIndx"] == "Pandas":
            if not (test["cIndx"] == 4):
                assert any(
                    test["rs"].sort_index().sort_index(axis=1)
                    == results[indx - 1]["rs"].sort_index().sort_index(axis=1)
                )
                if VERBOSE:
                    print(
                        f"{test['cIndx']} {test['fIndx']}: Pandas DataFrame vs {results[indx-1]['gIndx']} GeoDataFrame Comparison ok"
                    )
            else:
                if VERBOSE:
                    print(
                        f"{test['cIndx']} {test['fIndx']}: DataFrame Pandas vs {results[indx-1]['gIndx']} GeoDataFrame could not be equal because geometry and CRS is automatically included only into GeoPandas"
                    )

    print("all Checks ok")


if __name__ == "__main__":
    testPdBufr2GeoPandas(TEST_DATA_GEOPANDAS)