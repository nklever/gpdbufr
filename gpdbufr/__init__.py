# (C) Copyright 2019- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

from pdbufr.bufr_structure import stream_bufr

__all__ = ["stream_bufr"]

try:
    from pdbufr.bufr_read import read_bufr
    from .bufr_read import read_geo_bufr
    
    __all__ += ["read_bufr","read_geo_bufr"]
except ModuleNotFoundError:  # pragma: no cover
    pass

__version__ = "0.1.0"