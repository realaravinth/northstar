"""
Errors
"""
# North Star ---  A lookup service for forged fed ecosystem
# Copyright © 2022 Aravinth Manivannan <realaravinth@batsense.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from dataclasses import dataclass

from flask import jsonify


@dataclass
class Error(Exception):
    """Helper class for presenting errors in the format specified by the specification"""

    errcode: str
    error: str
    status: int


    def get_error(self):
        """Get error in serialziable form"""
        error = {}
        error["errcode"] = self.errcode
        error["error"] = self.error
        return error

    def get_error_resp(self):
        """Get error response"""
        resp = jsonify(self.get_error())
        resp.status = self.status
        return resp


F_D_NO_REGISTERED_INTERFACES = Error(
    errcode="F_D_NO_REGISTERED_INTERFACES",
    error="No interfaces are registered against the queried forge",
    status=400,
)

F_D_INTERNAL_SERVER_ERROR = Error(
    errcode="F_D_INTERNAL_SERVER_ERROR",
    error="Operation could not be performed due to internal errors.",
    status=500,
)


F_D_EMPTY_FORGE_LIST = Error(
    errcode="F_D_EMPTY_FORGE_LIST",
    error="The forge list submitted is empty",
    status=400,
)

F_D_INVALID_PAYLOAD = Error(
    errcode="F_D_INVALID_PAYLOAD",
    error="Please submit valid payload",
    status=400,
)


F_D_NOT_URL = Error(
    errcode="F_D_NOT_URL",
    error="Please submit valid URL",
    status=400,
)
