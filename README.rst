gpdbufr
=======

.. image:: https://img.shields.io/pypi/v/pdbufr.svg
   :target: https://pypi.python.org/pypi/gpdbufr/

GeoPandas reader for the BUFR format using ecCodes and pdbufr.

Features with development status **Beta**:

- extracts observations from a BUFR file as a Pandas DataFrame,
- reads BUFR 3 and 4 files with uncompressed and compressed subsets,
- supports all modern versions of Python 3.9, 3.8, 3.7, 3.6 and PyPy3,
- works on Linux, MacOS and Windows, the ecCodes C-library is the only binary dependency,
- sports a rich filtering engine,
- alternative use of Pandas DataFrame or GeoPandas GeoDataFrame 
- WMO station positions (latitude, longitude, heightOfStationGroundAboveMeanSeaLevel) are used to build geometry for GeoPandas GeoSeries 
- Coordinate Reference System is included as computed key CRS and defaults to WGS84 if missing as BufrKey 
- computed keys (data_datetime, typical_datetime, WMO_station_id, geometry, CRS) can now also be used to filter the records

Limitations:

- no conda-forge package (yet).

Installation
============

GeoPandas
---------

The easiest way to install *gpdbufr* dependencies is via Conda::

    $ conda install -c conda-forge python-eccodes pandas geopandas pdbufr

and *gpdbufr* itself as a Python package from PyPI with::

    $ pip install gpdbufr


System dependencies
-------------------

The Python module depends on the ECMWF *ecCodes* library
that must be installed on the system and accessible as a shared library.
Some Linux distributions ship a binary version that may be installed with the standard package manager.
On Ubuntu 18.04 use the command::

    $ sudo apt-get install libeccodes0

On a MacOS with HomeBrew use::

    $ brew install eccodes

As an alternative you may install the official source distribution
by following the instructions at
https://software.ecmwf.int/wiki/display/ECC/ecCodes+installation

You may run a simple selfcheck command to ensure that your system is set up correctly::

    $ python -m pdbufr selfcheck
    Found: ecCodes v2.19.0.
    Your system is ready.


Usage
=====

First, you need a well-formed BUFR file, if you don't have one at hand you can download our
`sample file <http://download.ecmwf.int/test-data/metview/gallery/temp.bufr>`_::

    $ wget http://download.ecmwf.int/test-data/metview/gallery/temp.bufr

You can explore the file with *ecCodes* command line tools ``bufr_ls`` and ``bufr_dump`` to
understand the structure and the keys/values you can use to select the observations you
are interested in.

Pandas Part
-----------

The ``gpdbufr.read_bufr`` function return a ``pandas.DataFrame`` with the requested columns.
It accepts query filters on the BUFR message header
that are very fast and query filters on the observation keys.
Additionally also on the following computed keys:

- data_datetime and typical_datetime (datetime.datetime)
- geometry (List [longitude,latitude,heightOfStationGroundAboveMeanSeaLevel])
- CRS (BufrKey Coordinate Reference System Values 0,1,2,3 and missing are supported (4 and 5 are not supported), defaults to WGS84 (EPSG:4632))

Filters match on an exact value or with one of the values in a list and all filters must match:

.. code-block:: python

    >>> import gpdbufr
    >>> df_all = gpdbufr.read_bufr('temp.bufr', columns=('stationNumber', 'latitude', 'longitude'))
    >>> df_all.head()
       stationNumber  latitude  longitude
    0            907     58.47     -78.08
    1            823     53.75     -73.67
    2              9    -90.00       0.00
    3            486     18.43     -69.88
    4            165     21.98    -159.33

    >>> df_one = pdbufr.read_bufr(
    ...     'temp.bufr',
    ...     columns=('stationNumber', 'latitude', 'longitude'),
    ...     filters={'stationNumber': 907},
    ... )
    >>> df_one.head()
       stationNumber  latitude  longitude
    0            907     58.47     -78.08

    >>> df_two = pdbufr.read_bufr(
    ...     'temp.bufr',
    ...     columns=('stationNumber', 'data_datetime', 'pressure', 'airTemperature'),
    ...     filters={'stationNumber': [823, 9]},
    ... )

    >>> df_two.head()
       stationNumber  pressure  airTemperature       data_datetime
    0            823  100000.0             NaN 2008-12-08 12:00:00
    1            823   97400.0           256.7 2008-12-08 12:00:00
    2            823   93700.0           255.1 2008-12-08 12:00:00
    3            823   92500.0           255.3 2008-12-08 12:00:00
    4            823   90600.0           256.7 2008-12-08 12:00:00

    >>> df_two.tail()
         stationNumber  pressure  airTemperature       data_datetime
    190              9    2990.0             NaN 2008-12-08 12:00:00
    191              9    2790.0           206.3 2008-12-08 12:00:00
    192              9    2170.0             NaN 2008-12-08 12:00:00
    193              9    2000.0           203.1 2008-12-08 12:00:00
    194              9    1390.0           197.9 2008-12-08 12:00:00

GeoPandas Part
--------------

The ``gpdbufr.read_geo_bufr`` function return a ``geopandas.GeoDataFrame`` with the requested columns.
It accepts query filters on the BUFR message header 
that are very fast and query filters on the observation keys.
Additionally also on the following computed keys:

- data_datetime and typical_datetime (datetime.datetime)
- geometry (shapely.geometry.Point.X <-> longitude, .Y <-> latitude, .Z <-> heightOfStationGroundAboveMeanSeaLevel)
- CRS (BufrKey Coordinate Reference System Values 0,1,2,3 and missing are supported (4 and 5 are not supported), defaults to WGS84 (EPSG:4632))

Filters match on an exact value or with one of the values in a list and all filters must match:

.. code-block:: python

    >>> import gpdbufr
    >>> from pyproj import Geod
    >>> from shapely.geometry import Point
    
    >>> def distance(center,position):
    ...     g = Geod(ellps="WGS84") 
    ...     az12,az21,dist = g.inv(position.x,position.y,center.x,center.y)
    ...     return dist
    
    >>> df_all = gpdbufr.read_geo_bufr(
    ...     'temp.bufr', 
    ...     columns=('stationNumber', 'latitude', 'longitude'),
    ...)
    
    >>> df_all.head()
       stationNumber  latitude  ...                         geometry        CRS
    0            907     58.47  ...   POINT Z (-78.080 58.470 0.000)  EPSG:4326
    1            823     53.75  ...   POINT Z (-73.670 53.750 0.000)  EPSG:4326
    2              9    -90.00  ...    POINT Z (0.000 -90.000 0.000)  EPSG:4326
    3            486     18.43  ...   POINT Z (-69.880 18.430 0.000)  EPSG:4326
    4            165     21.98  ...  POINT Z (-159.330 21.980 0.000)  EPSG:4326

    >>> center = Point(-75.0,55.0)
    >>> radius = 1000*1000 # 1000 km

    >>> df_geo = gpdbufr.read_geo_bufr(
    ...     'temp.bufr', 
    ...     columns=('stationNumber', 'latitude', 'longitude'), 
    ...     filters={'geometry': lambda x: distance(center,Point(x)) < radius}, 
    ...)
    
    >>> df_geo.head()
       stationNumber  latitude  ...                              geometry        CRS
    0            907     58.47  ...  POINT Z (-78.08000 58.47000 0.00000)  EPSG:4326
    1            823     53.75  ...  POINT Z (-73.67000 53.75000 0.00000)  EPSG:4326
    2            816     53.30  ...  POINT Z (-60.37000 53.30000 0.00000)  EPSG:4326
    3            836     51.27  ...  POINT Z (-80.65000 51.27000 0.00000)  EPSG:4326
    4            906     58.12  ...  POINT Z (-68.42000 58.12000 0.00000)  EPSG:4326

    >>> df_one = gpdbufr.read_geo_bufr(
    ...     'temp.bufr',
    ...     columns=('stationNumber', 'latitude', 'longitude'),
    ...     filters={'stationNumber': 907},
    ... )
    
    >>> df_one.head()
       stationNumber  latitude  ...                              geometry        CRS
    0            907     58.47  ...  POINT Z (-78.08000 58.47000 0.00000)  EPSG:4326

    >>> df_two = gpdbufr.read_geo_bufr(
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


Contributing
============

The main repository is hosted on GitHub,
testing, bug reports and contributions are highly welcomed and appreciated:

https://github.com/nklever/gpdbufr

Please see the CONTRIBUTING.rst document for the best way to help.

GeoPandas contribution:

- `Nik Klever <https://github.com/nklever>`_ - `University of Applied Sciences Augsburg <https://hs-augsburg.de>`_


See also the list of `contributors <https://github.com/ecmwf/pdbufr/contributors>`_ who participated in this project.


License
=======

Copyright 2019- European Centre for Medium-Range Weather Forecasts (ECMWF).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.