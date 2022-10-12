# =================================================================
#
# Terms and Conditions of Use
#
# Unless otherwise noted, computer program source code of this
# distribution # is covered under Crown Copyright, Government of
# Canada, and is distributed under the MIT License.
#
# The Canada wordmark and related graphics associated with this
# distribution are protected under trademark law and copyright law.
# No permission is granted to use them outside the parameters of
# the Government of Canada's corporate identity program. For
# more information, see
# http://www.tbs-sct.gc.ca/fip-pcim/index-eng.asp
#
# Copyright title to all 3rd party software distributed with this
# software is held by the respective copyright holders as noted in
# those files. Users are asked to read the 3rd Party Licenses
# referenced with those assets.
#
# Copyright (c) 2021 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import json
import os
from datetime import datetime

from pygeometa.core import get_charstring
from pygeometa.helpers import json_serial
from pygeometa.schemas.base import BaseOutputSchema

THISDIR = os.path.dirname(os.path.realpath(__file__))


class OGCAPIDRecordOutputSchema(BaseOutputSchema):
    """OGC API - Records - Part 1: Core record schema"""

    def __init__(self):
        """
        Initialize object

        :returns: pygeometa.schemas.base.BaseOutputSchema
        """

        super().__init__('oarec-record', 'json', THISDIR)

    def write(self, mcf: dict, stringify: str = True) -> str:
        """
        Write outputschema to JSON string buffer

        :param mcf: dict of MCF content model
        :param stringify: whether to return a string representation (default)
                          else native (dict, etree)


        :returns: MCF as a STAC item representation
        """

        minx, miny, maxx, maxy = (mcf['identification']['extents']
                                  ['spatial'][0]['bbox'])

        title = get_charstring('title', mcf['identification'],
                               mcf['metadata']['language'],
                               mcf['metadata']['language_alternate'])

        dateval = datetime.utcnow().strftime("%Y-%m-%d")


        record = {
            'id': mcf['cat_id'],
            'type': 'Feature',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[
                    [minx, miny],
                    [minx, maxy],
                    [maxx, maxy],
                    [maxx, miny],
                    [minx, miny]
                ]]
            },
            'properties': {
                'record-created': dateval,
                'record-updated': dateval,
                'type': 'feature',
                'title': mcf['cat_description'],
                'description': mcf['cat_description'],
                'extents': {
                    'spatial': {
                        'bbox': [minx, miny, maxx, maxy],
                        'crs': 'http://www.opengis.net/def/crs/OGC/1.3/CRS84'  # noqa
                    },
                    'temporal': {
                        'interval': [mcf['cat_begin'], mcf['cat_end']],
                        'trs': 'http://www.opengis.net/def/uom/ISO-8601/0/Gregorian'  # noqa
                    }
                },
            },
            'links': []
        }

        link = {
            'rel': 'root',
            'type': 'application/json',
            'title': 'This document is an OGC Record',
            'href': mcf['cat_file']
        }
        record['links'].append(link)

        return json.dumps(record, default=json_serial, indent=4)
