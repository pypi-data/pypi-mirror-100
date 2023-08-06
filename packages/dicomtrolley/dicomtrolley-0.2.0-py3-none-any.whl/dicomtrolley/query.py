"""Models queries to a MINT server"""
import datetime
from typing import ClassVar, List, Optional, Set

from pydantic.class_validators import validator
from pydantic.main import BaseModel

from dicomtrolley.include_fields import (
    InstanceLevel,
    SeriesLevel,
    SeriesLevelPromotable,
    StudyLevel,
)


class QueryLevels:
    STUDY = "STUDY"
    SERIES = "SERIES"
    INSTANCE = "INSTANCE"

    ALL = {STUDY, SERIES, INSTANCE}


class QueryParameter(BaseModel):
    """Something you can search on in the MINT find DICOM studies function"""

    pass


class Query(BaseModel):
    """Things you can search for with the MINT find DICOM studies function

    Notes
    -----
    * All string arguments support (*) as a wildcard
    * non-pep8 parameter naming format follows MINT url parameters naming
    """

    # String parameters (wildcards allowed)
    studyInstanceUID: str = ""
    accessionNumber: str = ""
    patientName: str = ""
    patientID: str = ""
    modalitiesInStudy: str = ""
    institutionName: str = ""
    patientSex: str = ""
    studyDescription: str = ""
    institutionalDepartmentName: str = ""

    # date search parameters
    patientBirthDate: Optional[datetime.date]
    minStudyDate: Optional[datetime.datetime]
    maxStudyDate: Optional[datetime.datetime]

    # meta parameters: how to return results
    queryLevel: str = QueryLevels.STUDY  # to which depth to return results
    includeFields: List[str] = []  # which dicom fields to return
    limit: int = 0  # how many results to return. 0 = all

    class Config:
        extra = "forbid"  # raise ValueError when passing an unknown keyword to init

    def __str__(self):
        return str(self.as_parameters())

    @validator("maxStudyDate", always=True)
    def min_max_study_date_xor(cls, value, values):  # noqa: B902, N805
        """Min and max should both be given or both be empty"""
        if values.get("minStudyDate", None) and not value:
            raise ValueError(
                f"minStudyDate parameter was passed "
                f"({values['minStudyDate']}), "
                f"but maxStudyDate was not. Both need to be given"
            )
        elif value and not values.get("minStudyDate", None):
            raise ValueError(
                f"maxStudyDate parameter was passed ({value}), "
                f"but minStudyDate was not. Both need to be given"
            )
        return value

    @validator("includeFields")
    def include_fields_check(cls, include_fields, values):  # noqa: B902, N805
        """Include fields should be valid and match query level"""
        query_level = values["queryLevel"]
        valid_fields = get_valid_fields(query_level=query_level)
        for field in include_fields:
            if field not in valid_fields:
                raise ValueError(
                    f'"{field}" is not a valid include field for query '
                    f"level {query_level}. Valid fields: {valid_fields}"
                )
        return include_fields

    def as_parameters(self):
        """All non-empty query parameters. For use as url parameters"""
        parameters = {x: y for x, y in self.dict().items() if y}

        if "minStudyDate" in parameters:
            parameters["minStudyDate"] = self.date_to_iso(
                parameters["minStudyDate"]
            )
        if "maxStudyDate" in parameters:
            parameters["maxStudyDate"] = self.date_to_iso(
                parameters["maxStudyDate"]
            )
        if "patientBirthDate" in parameters:
            parameters["patientBirthDate"] = parameters[
                "patientBirthDate"
            ].strftime("%Y%m%d")

        return parameters

    @staticmethod
    def date_to_iso(date):
        """MINT expects min- and maxStudyDate to be ISO8601 "basic date time" format
        yyyymmddThhmmssZ
        This format allows for setting the time zone offset from UTC, where 'Z'
        means zero
        Example:
        minStudyDateTime=20141231T210349Z
        &maxStudyDateTime=20141201T230349Z
        To change the time zone offset, append the datetime string with a time zone
        offset value of +hhm m or -hhmm. For example: +0700, -0130 , and so on. Note
        that the offset is not equivalent to time zone, and can change throughout the
        year based on time zone rules.

        Returns
        -------
        str:
            date in iso format requested by MINT server
        """
        return (
            date.replace(microsecond=0)
            .isoformat()
            .replace("-", "")
            .replace(":", "")
            + "Z"
        )


class StudyInstanceUID(QueryParameter):
    StudyInstanceUID: str


class AccessionNumber(QueryParameter):
    AccessionNumber: str


class PatientName(QueryParameter):
    """Matches against a format of "lastName^firstName". For example,
    "Armstrong^Lil".

    Wildcard support: Use one or more wildcard characters (*) to complete the string.
    For example: "A*^L*", "Armstrong*", "arm*", "A*^*l".
    """

    key: ClassVar[str] = "PatientName"


class PatientID(QueryParameter):
    key: ClassVar[str] = "PatientID"


class ModalitiesInStudy(QueryParameter):
    key: ClassVar[str] = "ModalitiesInStudy"


class InstitutionName(QueryParameter):
    key: ClassVar[str] = "InstitutionName"


class PatientSex(QueryParameter):
    key: ClassVar[str] = "PatientSex"


class StudyDescription(QueryParameter):
    key: ClassVar[str] = "StudyDescription"


class InstitutionalDepartmentName(QueryParameter):
    key: ClassVar[str] = "InstitutionalDepartmentName"


def get_valid_fields(query_level) -> Set[str]:
    """All fields that can be returned at the given level"""
    if query_level == QueryLevels.INSTANCE:
        return InstanceLevel.fields
    elif query_level == QueryLevels.SERIES:
        return SeriesLevel.fields | SeriesLevelPromotable.fields
    elif query_level == QueryLevels.STUDY:
        return StudyLevel.fields
    else:
        raise ValueError(
            f'Unknown query level "{query_level}". Valid values '
            f"are {QueryLevels.ALL}"
        )
