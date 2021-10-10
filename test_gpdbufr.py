# (C) Copyright 2021 - Nik Klever (University of Applied Sciences Augsburg).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import typing as T

import pdbufr
import geopandas as gpd

from gpdbufr import read_geo_bufr, distance
from pyproj import Geod  # type: ignore
from shapely.geometry import Point  # type: ignore

TEST_DATA_GEOPANDAS = (
    "Z__C_EDZW_20210516120400_bda01,synop_bufr_GER_999999_999999__MW_466.bin"
)


def test_GeoPandas_without_latlon_with_timesignificance() -> None:
    center = Point([11.010754, 47.800864])  # Hohenpeißenberg
    radius = 100 * 1000  # 100 km
    columns = [
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
    ]
    filter_wind = dict(windDirection=float, windSpeed=float)
    filter_wind_geometry = dict(
        windDirection=float,
        windSpeed=float,
        geometry=lambda x: distance(center, Point(x)) < radius,
    )

    rsg = read_geo_bufr(TEST_DATA_GEOPANDAS, columns)
    assert len(rsg) == 178

    rs = pdbufr.read_bufr(TEST_DATA_GEOPANDAS, columns)
    assert len(rs) == 178

    assert any(
        rs.sort_index().sort_index(axis=1) == rsg.sort_index().sort_index(axis=1)
    )

    rsg = read_geo_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind)
    assert len(rsg) == 175

    rs = pdbufr.read_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind)
    assert len(rs) == 175

    assert any(
        rs.sort_index().sort_index(axis=1) == rsg.sort_index().sort_index(axis=1)
    )

    rsg = read_geo_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind_geometry)
    assert len(rsg) == 10
    for station in rsg.to_records():
        assert distance(center, station["geometry"]) < radius

    rs = pdbufr.read_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind_geometry)
    assert len(rs) == 10
    for station in rs.to_records():
        assert distance(center, Point(station["geometry"])) < radius

    assert any(
        rs.sort_index().sort_index(axis=1) == rsg.sort_index().sort_index(axis=1)
    )


def test_GeoPandas_with_latlon_with_timesignificance() -> None:
    center = Point([11.010754, 47.800864])  # Hohenpeißenberg
    radius = 100 * 1000  # 100 km
    columns = [
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
    ]
    filter_wind = dict(windDirection=float, windSpeed=float)
    filter_wind_geometry = dict(
        windDirection=float,
        windSpeed=float,
        geometry=lambda x: distance(center, Point(x)) < radius,
    )

    rsg = read_geo_bufr(TEST_DATA_GEOPANDAS, columns)
    assert len(rsg) == 178

    rs = pdbufr.read_bufr(TEST_DATA_GEOPANDAS, columns)
    assert len(rs) == 178

    assert any(
        rs.sort_index().sort_index(axis=1) == rsg.sort_index().sort_index(axis=1)
    )

    rsg = read_geo_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind)
    assert len(rsg) == 175

    rs = pdbufr.read_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind)
    assert len(rs) == 175

    assert any(
        rs.sort_index().sort_index(axis=1) == rsg.sort_index().sort_index(axis=1)
    )

    rsg = read_geo_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind_geometry)
    assert len(rsg) == 10
    for station in rsg.to_records():
        assert distance(center, station["geometry"]) < radius

    rs = pdbufr.read_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind_geometry)
    assert len(rs) == 10
    for station in rs.to_records():
        assert distance(center, Point(station["geometry"])) < radius

    assert any(
        rs.sort_index().sort_index(axis=1) == rsg.sort_index().sort_index(axis=1)
    )


def test_GeoPandas_without_latlon_without_timesignificance() -> None:
    center = Point([11.010754, 47.800864])  # Hohenpeißenberg
    radius = 100 * 1000  # 100 km
    columns = [
        "WMO_station_id",
        "stationOrSiteName",
        "geometry",
        "CRS",
        "typicalDate",
        "typicalTime",
        "timePeriod",
        "windDirection",
        "windSpeed",
    ]
    filter_wind = dict(windDirection=float, windSpeed=float)
    filter_wind_geometry = dict(
        windDirection=float,
        windSpeed=float,
        geometry=lambda x: distance(center, Point(x)) < radius,
    )

    rsg = read_geo_bufr(TEST_DATA_GEOPANDAS, columns)
    assert len(rsg) == 204

    rs = pdbufr.read_bufr(TEST_DATA_GEOPANDAS, columns)
    assert len(rs) == 204

    assert any(
        rs.sort_index().sort_index(axis=1) == rsg.sort_index().sort_index(axis=1)
    )

    rsg = read_geo_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind)
    assert len(rsg) == 201

    rs = pdbufr.read_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind)
    assert len(rs) == 201

    assert any(
        rs.sort_index().sort_index(axis=1) == rsg.sort_index().sort_index(axis=1)
    )

    rsg = read_geo_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind_geometry)
    assert len(rsg) == 13
    for station in rsg.to_records():
        assert distance(center, station["geometry"]) < radius

    rs = pdbufr.read_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind_geometry)
    assert len(rs) == 13
    for station in rs.to_records():
        assert distance(center, Point(station["geometry"])) < radius

    assert any(
        rs.sort_index().sort_index(axis=1) == rsg.sort_index().sort_index(axis=1)
    )


def test_GeoPandas_with_latlon_without_timesignificance() -> None:
    center = Point([11.010754, 47.800864])  # Hohenpeißenberg
    radius = 100 * 1000  # 100 km
    columns = [
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
    ]
    filter_wind = dict(windDirection=float, windSpeed=float)
    filter_wind_geometry = dict(
        windDirection=float,
        windSpeed=float,
        geometry=lambda x: distance(center, Point(x)) < radius,
    )

    rsg = read_geo_bufr(TEST_DATA_GEOPANDAS, columns)
    assert len(rsg) == 204

    rs = pdbufr.read_bufr(TEST_DATA_GEOPANDAS, columns)
    assert len(rs) == 204

    assert any(
        rs.sort_index().sort_index(axis=1) == rsg.sort_index().sort_index(axis=1)
    )

    rsg = read_geo_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind)
    assert len(rsg) == 201

    rs = pdbufr.read_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind)
    assert len(rs) == 201

    assert any(
        rs.sort_index().sort_index(axis=1) == rsg.sort_index().sort_index(axis=1)
    )

    rsg = read_geo_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind_geometry)
    assert len(rsg) == 13
    for station in rsg.to_records():
        assert distance(center, station["geometry"]) < radius

    rs = pdbufr.read_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind_geometry)
    assert len(rs) == 13
    for station in rs.to_records():
        assert distance(center, Point(station["geometry"])) < radius

    assert any(
        rs.sort_index().sort_index(axis=1) == rsg.sort_index().sort_index(axis=1)
    )


def test_GeoPandas_without_geometry_without_latlon_without_timesignificance() -> None:
    center = Point([11.010754, 47.800864])  # Hohenpeißenberg
    radius = 100 * 1000  # 100 km
    columns = [
        "WMO_station_id",
        "stationOrSiteName",
        "typicalDate",
        "typicalTime",
        "timePeriod",
        "windDirection",
        "windSpeed",
    ]
    filter_wind = dict(windDirection=float, windSpeed=float)
    filter_wind_geometry = dict(
        windDirection=float,
        windSpeed=float,
        geometry=lambda x: distance(center, Point(x)) < radius,
    )

    rsg = read_geo_bufr(TEST_DATA_GEOPANDAS, columns)
    assert len(rsg) == 204

    rs = pdbufr.read_bufr(TEST_DATA_GEOPANDAS, columns)
    assert len(rs) == 204

    rsg = read_geo_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind)
    assert len(rsg) == 201

    rs = pdbufr.read_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind)
    assert len(rs) == 201

    rsg = read_geo_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind_geometry)
    assert len(rsg) == 13
    for station in rsg.to_records():
        assert distance(center, station["geometry"]) < radius

    rs = pdbufr.read_bufr(TEST_DATA_GEOPANDAS, columns, filter_wind_geometry)
    assert len(rs) == 13
    for station in rs.to_records():
        assert distance(center, Point(station["geometry"])) < radius
