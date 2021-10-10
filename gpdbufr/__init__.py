import pdbufr
import os
import typing as T
from pyproj import Geod
from shapely.geometry import Point
import geopandas as gpd


def distance(center, position):
    g = Geod(ellps="WGS84")
    az12, az21, dist = g.inv(position.x, position.y, center.x, center.y)
    return dist


def read_geo_bufr(
    path: T.Union[str, bytes, "os.PathLike[T.Any]"],
    columns: T.Iterable[str],
    filters: T.Mapping[str, T.Any] = {},
    required_columns: T.Union[bool, T.Iterable[str]] = True,
) -> gpd.GeoDataFrame:
    """
    Read selected observations from a BUFR file into GeoDataFrame.

    :param path: The path to the BUFR file
    :param columns: A list of BUFR keys to return in the DataFrame for every observation
    :param filters: A dictionary of BUFR key / filter definition to filter the observations to return
    :param required_columns: The list BUFR keys that are required for all observations.
        ``True`` means all ``columns`` are required
    """

    for key in ["geometry", "CRS"]:
        if key not in columns:
            if isinstance(columns, list):
                columns.append(key)
            elif isinstance(columns, tuple):
                columns += (key,)
            elif isinstance(columns, set):
                columns |= {key}
            else:
                raise ValueError("columns must be an instance of list or tuple or set")

    dataFrame = pdbufr.read_bufr(path, columns, filters, required_columns)

    if dataFrame.empty:
        return dataFrame

    dataFrame["geometry"] = dataFrame["geometry"].apply(Point)
    CRS = dataFrame.CRS[0]
    if not CRS:
        raise TypeError(
            "pdbufr does currently not support the type of coordinate system reference in BUFR data"
        )
    return gpd.GeoDataFrame(dataFrame, geometry=dataFrame.geometry, crs=CRS)
