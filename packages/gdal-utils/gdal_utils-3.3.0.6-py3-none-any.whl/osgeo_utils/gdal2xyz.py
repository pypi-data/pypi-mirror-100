#!/usr/bin/env python3
###############################################################################
# $Id$
#
# Project:  GDAL
# Purpose:  Script to translate GDAL supported raster into XYZ ASCII
#           point stream.
# Author:   Frank Warmerdam, warmerdam@pobox.com
#
###############################################################################
# Copyright (c) 2002, Frank Warmerdam <warmerdam@pobox.com>
# Copyright (c) 2020, Idan Miara <idan@miara.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################

import sys
from numbers import Number
from pathlib import Path
from typing import Optional, Union, Sequence, Tuple
import numpy as np

from osgeo import gdal
from osgeo_utils.auxiliary.base import num, PathLike
from osgeo_utils.auxiliary.progress import get_progress_callback, ProgressCallbackOrDefault
from osgeo_utils.auxiliary.util import PathOrDS
from osgeo_utils.auxiliary.numpy_util import GDALTypeCodeAndNumericTypeCodeFromDataSet


def Usage():
    print('Usage: gdal2xyz.py [-help]'
          '                   [-skip factor] [-srcwin xoff yoff width height]'
          '                   [-b|band band]* [-allbands] [-csv]'
          '                   [-skipnodata]'
          '                   [-srcnodata value]* [-dstnodata value]*'
          '                   src_dataset [dst_dataset]')
    print('')
    return 1


def main(argv):
    srcwin = None
    skip = 1
    srcfile = None
    dstfile = None
    band_nums = []
    all_bands = False
    delim = ' '
    skip_nodata = False
    src_nodata = []
    dst_nodata = []

    argv = gdal.GeneralCmdLineProcessor(argv)
    if argv is None:
        return 0

    # Parse command line arguments.
    i = 1
    while i < len(argv):
        arg = str(argv[i]).lower()
        if arg.startswith('--'):
            arg = arg[1:]

        if arg == '-srcwin':
            srcwin = (int(argv[i + 1]), int(argv[i + 2]),
                      int(argv[i + 3]), int(argv[i + 4]))
            i = i + 4

        elif arg == '-skip':
            skip = int(argv[i + 1])
            i = i + 1

        elif arg in ['-b', '-band']:
            b = int(argv[i + 1])
            i = i + 1
            if b:
                band_nums.append(b)
            else:
                all_bands = True

        elif arg == '-allbands':
            all_bands = True

        elif arg == '-csv':
            delim = ','

        elif arg in ['-skipnodata', '-skip_nodata']:
            skip_nodata = True

        elif arg in ['-nodatavalue', '-srcnodata']:
            src_nodata.append(num(argv[i + 1]))
            i = i + 1

        elif arg == '-dstnodata':
            dst_nodata.append(num(argv[i + 1]))
            i = i + 1

        elif srcfile is None:
            srcfile = arg

        elif dstfile is None:
            dstfile = arg

        elif arg == '-help':
            return Usage()

        else:
            return Usage()

        i = i + 1

    if srcfile is None:
        return Usage()

    if all_bands:
        band_nums = None
    elif not band_nums:
        band_nums = 1
    return gdal2xyz(srcfile=srcfile, dstfile=dstfile, srcwin=srcwin, skip=skip,
                    band_nums=band_nums, delim=delim,
                    skip_nodata=skip_nodata, src_nodata=src_nodata, dst_nodata=dst_nodata)


def gdal2xyz(srcfile: PathOrDS, dstfile: PathLike = None,
             srcwin: Optional[Sequence[int]] = None,
             skip: Union[int, Sequence[int]] = 1,
             band_nums: Optional[Sequence[int]] = None, delim=' ',
             skip_nodata: bool = False,
             src_nodata: Optional[Union[Sequence, Number]] = None, dst_nodata: Optional[Union[Sequence, Number]] = None,
             return_np_arrays: bool = False, pre_allocate_np_arrays: bool = True,
             progress_callback: ProgressCallbackOrDefault = ...) -> Optional[Tuple]:
    """
    translates a raster file (or dataset) into xyz format

    skip - how many rows/cols to skip each iteration
    srcwin (xoff, yoff, xsize, ysize) - Selects a subwindow from the source image for copying based on pixel/line location.
    band_nums - selected input bands to process, None to process all.
    delim - the delimiter to use between values in a line
    skip_nodata - Exclude the output lines with nodata value (as determined by srcnodata)
    src_nodata - The nodata value of the dataset (for skipping or replacing)
        default (`None`) - Use the dataset NoDataValue;
        `Sequence`/`Number` - use the given nodata value (per band or per dataset).
    dst_nodata - Replace source nodata with a given nodata. Has an effect only if not setting `-skipnodata`
        default(`None`) - use srcnodata, no replacement;
        `Sequence`/`Number` - replace the `srcnodata` with the given nodata value (per band or per dataset).
    srcfile - The source dataset filename or dataset object
    dstfile - The output dataset filename; for dstfile=None - if return_np_arrays=False then output will be printed to stdout
    return_np_arrays - return numpy arrays of the result, otherwise returns None
    pre_allocate_np_arrays - pre-allocated result arrays.
        Should be faster unless skip_nodata and the input is very sparse thus most data points will be skipped.
    progress_callback - progress callback function. use None for quiet or Ellipsis for using the default callback
    """

    result = None

    progress_callback = get_progress_callback(progress_callback)

    # Open source file.
    srcds = gdal.Open(str(srcfile), gdal.GA_ReadOnly) if isinstance(srcfile, (Path, str)) else srcfile
    if srcds is None:
        raise Exception(f'Could not open {srcfile}.')

    if not band_nums:
        band_nums = list(range(1, srcds.RasterCount + 1))
    elif isinstance(band_nums, int):
        band_nums = [band_nums]
    bands = []
    for band_num in band_nums:
        band = srcds.GetRasterBand(band_num)
        if band is None:
            raise Exception(f'Could not get band {band_num} from file {srcfile}')
        bands.append(band)
    band_count = len(bands)

    gt = srcds.GetGeoTransform()

    # Collect information on all the source files.
    if srcwin is None:
        srcwin = (0, 0, srcds.RasterXSize, srcds.RasterYSize)

    dt, np_dt = GDALTypeCodeAndNumericTypeCodeFromDataSet(srcds)

    # Open the output file.
    if dstfile is not None:
        dst_fh = open(dstfile, 'wt')
    elif return_np_arrays:
        dst_fh = None
    else:
        dst_fh = sys.stdout

    if dst_fh:
        if dt == gdal.GDT_Int32 or dt == gdal.GDT_UInt32:
            band_format = (("%d" + delim) * len(bands)).rstrip(delim) + '\n'
        else:
            band_format = (("%g" + delim) * len(bands)).rstrip(delim) + '\n'

        # Setup an appropriate print format.
        if abs(gt[0]) < 180 and abs(gt[3]) < 180 \
            and abs(srcds.RasterXSize * gt[1]) < 180 \
            and abs(srcds.RasterYSize * gt[5]) < 180:
            frmt = '%.10g' + delim + '%.10g' + delim + '%s'
        else:
            frmt = '%.3f' + delim + '%.3f' + delim + '%s'

    if isinstance(src_nodata, Number):
        src_nodata = [src_nodata] * band_count
    elif src_nodata is None:
        src_nodata = list(band.GetNoDataValue() for band in bands)
    if None in src_nodata:
        src_nodata = None
    if src_nodata is not None:
        src_nodata = np.asarray(src_nodata, dtype=np_dt)

    if isinstance(dst_nodata, Number):
        dst_nodata = [dst_nodata] * band_count
    if (dst_nodata is None) or (None in dst_nodata) or (src_nodata is None):
        dst_nodata = None
    if dst_nodata is not None:
        dst_nodata = np.asarray(dst_nodata, dtype=np_dt)

    skip_nodata = skip_nodata and (src_nodata is not None)
    replace_nodata = (not skip_nodata) and (dst_nodata is not None)
    process_nodata = skip_nodata or replace_nodata

    if isinstance(skip, Sequence):
        x_skip, y_skip = skip
    else:
        x_skip = y_skip = skip

    x_off, y_off, x_size, y_size = srcwin
    bands_count = len(bands)

    nXBlocks = (x_size - x_off) // x_skip
    nYBlocks = (y_size - y_off) // y_skip
    progress_end = nXBlocks * nYBlocks
    progress_curr = 0
    progress_prev = -1
    progress_parts = 100

    if return_np_arrays:
        size = progress_end if pre_allocate_np_arrays else 0
        all_geo_x = np.empty(size)
        all_geo_y = np.empty(size)
        all_data = np.empty((size, band_count), dtype=np_dt)

    # Loop emitting data.
    idx = 0
    for y in range(y_off, y_off + y_size, y_skip):

        size = bands_count if pre_allocate_np_arrays else 0
        data = np.empty((size, x_size), dtype=np_dt)  # dims: (bands_count, x_size)
        for i_bnd, band in enumerate(bands):
            band_data = band.ReadAsArray(x_off, y, x_size, 1)  # read one band line
            if pre_allocate_np_arrays:
                data[i_bnd] = band_data[0]
            else:
                data = np.append(data, band_data, axis=0)

        for x_i in range(0, x_size, x_skip):

            progress_curr += 1
            if progress_callback:
                progress_frac = progress_curr / progress_end
                progress = int(progress_frac * progress_parts)
                if progress > progress_prev:
                    progress_prev = progress
                    progress_callback(progress_frac)

            x_i_data = data[:, x_i]   # single pixel, dims: (bands)
            if process_nodata and np.array_equal(src_nodata, x_i_data):
                if skip_nodata:
                    continue
                elif replace_nodata:
                    x_i_data = dst_nodata

            x = x_i + x_off

            geo_x = gt[0] + (x + 0.5) * gt[1] + (y + 0.5) * gt[2]
            geo_y = gt[3] + (x + 0.5) * gt[4] + (y + 0.5) * gt[5]

            if dst_fh:
                band_str = band_format % tuple(x_i_data)
                line = frmt % (float(geo_x), float(geo_y), band_str)
                dst_fh.write(line)
            if return_np_arrays:
                if pre_allocate_np_arrays:
                    all_geo_x[idx] = geo_x
                    all_geo_y[idx] = geo_y
                    all_data[idx] = x_i_data
                else:
                    all_geo_x = np.append(all_geo_x, geo_x)
                    all_geo_y = np.append(all_geo_y, geo_y)
                    all_data = np.append(all_data, [x_i_data], axis=0)
            idx += 1

    if return_np_arrays:
        nodata = None if skip_nodata else dst_nodata if replace_nodata else src_nodata
        if idx != progress_curr:
            all_geo_x = all_geo_x[:idx]
            all_geo_y = all_geo_y[:idx]
            all_data = all_data[:idx,:]
        result = all_geo_x, all_geo_y, all_data.transpose(), nodata

    return result


if __name__ == '__main__':
    sys.exit(main(sys.argv))
