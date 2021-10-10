gpdbufr
=======

pdbufr GeoPandas Usage 
----------------------

.. image:: https://img.shields.io/pypi/v/pdbufr.svg
   :target: https://pypi.python.org/pypi/pdbufr/

Example for the usage of GeoPandas for the BUFR format using ecCodes and pdbufr.

Installation
============

pdbufr should be installed as described in https://github.com/ecmwf/pdbufr

GeoPandas should be installed as described in https://github.com/geopandas/geopandas

gpdbufr could be installed as a package using folder ``gpdbufr`` and ``\_\_init\_\_.py``
or copying functions *read_geo_bufr* and *distance* directly from file ``gpdbufr/\_\_init\_\_.py``

Usage
=====

First, you need a well-formed BUFR file, if you don't have one at hand you can download our
`sample file <http://download.ecmwf.int/test-data/metview/gallery/temp.bufr>`_::

    $ wget http://download.ecmwf.int/test-data/metview/gallery/temp.bufr

You can explore the file with *ecCodes* command line tools ``bufr_ls`` and ``bufr_dump`` to
understand the structure and the keys/values you can use to select the observations you
are interested in.

The ``read_geo_bufr`` function is built upon pdbufr.read_bufr but returns a ``geopandas.GeoDataFrame`` with the requested columns.
It accepts the same arguments as pdbufr.read_bufr.

The ``distance`` function is built upon the pyproj.Geod class with ellips="WGS84".
This function needs two arguments as shapely.geometry.Point instances.

Filters match on an exact value or with one of the values in a list and all filters must match:

.. code-block:: python

    >>> from gpdbufr import read_geo_bufr, distance
    >>> from shapely.geometry import Point
    
    >>> df_all = read_geo_bufr(
    ...     'temp.bufr', 
    ...     columns=('stationNumber', 'latitude', 'longitude'),
    ... )
    
    >>> df_all.head()
       stationNumber  latitude  ...                         geometry        CRS
    0            907     58.47  ...   POINT Z (-78.080 58.470 0.000)  EPSG:4326
    1            823     53.75  ...   POINT Z (-73.670 53.750 0.000)  EPSG:4326
    2              9    -90.00  ...    POINT Z (0.000 -90.000 0.000)  EPSG:4326
    3            486     18.43  ...   POINT Z (-69.880 18.430 0.000)  EPSG:4326
    4            165     21.98  ...  POINT Z (-159.330 21.980 0.000)  EPSG:4326

    [5 rows x 5 columns]
    >>> center = Point(-75.0,55.0)
    >>> radius = 1000*1000 # 1000 km

    >>> df_geo = read_geo_bufr(
    ...     'temp.bufr', 
    ...     columns=('stationNumber', 'latitude', 'longitude'), 
    ...     filters={'geometry': lambda x: distance(center,Point(x)) < radius}, 
    ... )
    
    >>> df_geo.head()
       stationNumber  latitude  ...                              geometry        CRS
    0            907     58.47  ...  POINT Z (-78.08000 58.47000 0.00000)  EPSG:4326
    1            823     53.75  ...  POINT Z (-73.67000 53.75000 0.00000)  EPSG:4326
    2            816     53.30  ...  POINT Z (-60.37000 53.30000 0.00000)  EPSG:4326
    3            836     51.27  ...  POINT Z (-80.65000 51.27000 0.00000)  EPSG:4326
    4            906     58.12  ...  POINT Z (-68.42000 58.12000 0.00000)  EPSG:4326

    [5 rows x 5 columns]
    >>> df_one = read_geo_bufr(
    ...     'temp.bufr',
    ...     columns=('stationNumber', 'latitude', 'longitude'),
    ...     filters={'stationNumber': 907},
    ... )
    
    >>> df_one.head()
       stationNumber  latitude  ...                              geometry        CRS
    0            907     58.47  ...  POINT Z (-78.08000 58.47000 0.00000)  EPSG:4326

    >>> df_two = read_geo_bufr(
    ...     'temp.bufr',
    ...     columns=('stationNumber', 'data_datetime', 'pressure', 'airTemperature'),
    ...     filters={'stationNumber': [823, 9]},
    ... )

    >>> df_two.head()
       stationNumber  pressure  ...                              geometry        CRS
    0            823  100000.0  ...  POINT Z (-73.67000 53.75000 0.00000)  EPSG:4326
    1            823   97400.0  ...  POINT Z (-73.67000 53.75000 0.00000)  EPSG:4326
    2            823   93700.0  ...  POINT Z (-73.67000 53.75000 0.00000)  EPSG:4326
    3            823   92500.0  ...  POINT Z (-73.67000 53.75000 0.00000)  EPSG:4326
    4            823   90600.0  ...  POINT Z (-73.67000 53.75000 0.00000)  EPSG:4326

    >>> df_two.tail()
         stationNumber  pressure  ...                             geometry        CRS
    190              9    2990.0  ...  POINT Z (36.17000 51.77000 0.00000)  EPSG:4326
    191              9    2790.0  ...  POINT Z (36.17000 51.77000 0.00000)  EPSG:4326
    192              9    2170.0  ...  POINT Z (36.17000 51.77000 0.00000)  EPSG:4326
    193              9    2000.0  ...  POINT Z (36.17000 51.77000 0.00000)  EPSG:4326
    194              9    1390.0  ...  POINT Z (36.17000 51.77000 0.00000)  EPSG:4326


License
=======

Copyright 2021 - Nik Klever (University of Applied Sciences Augsburg).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
