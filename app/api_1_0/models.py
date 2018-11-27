"""Contains the models for the data."""
import datetime


class IncidentModel(object):
    """This class models an Incident."""

    def __init__(self, created_by, incident_type, location, comment, errors=[]):
        """Initialize an Incident object.

        args:
            created_by(str): incident owner
            type(str): either of intervention or red-flag
            location(str): longituted, latitude coordinates
            status(str): draft, under investigation, resolved or rejected
            comment(str): A description of the incident
        """
        self.errors = errors
        self.id = ''
        self.created_by = created_by
        self.created_on = datetime.datetime.now()
        self.incident_type = incident_type
        self.location = location
        self.status = ''
        self.comment = comment
        self.images = []
        self.videos = []

    def save(self, db):
        """Save incident to db.

        args:
            db(list): The list into which to save the incident.
        """
        if self.created_by and self.incident_type and self.location and self.comment:
            self.id = len(db) + 1
            db.append({self.id: self.describe_incident()})
            return {'status': True, 'message': {"Id": self.id,
                    "message": "Successfuly created incident"}}
        else:
            return {'status': False, 'message': {'errors': self.errors}}

    @property
    def created_by(self):
        """Get incident created_by."""
        return self._created_by

    @created_by.setter
    def created_by(self, creator):
        """Verify and set created_by."""
        if not is_empty(creator):
            created_by = ''
            try:
                created_by = int(creator)
            except:
                created_by = None
            if created_by is not None:
                self._created_by = creator
            else:
                self._created_by = None
                self.errors.append("Created by should be an Integer")
        else:
            self._created_by = None
            self.errors.append("Incident owner should not be blank")


    @property
    def incident_type(self):
        """Get incident_type."""
        return self._incident_type

    @incident_type.setter
    def incident_type(self, incident_type):
        if not is_empty(incident_type):
            incident_types = ["red-flag", "intervention"]
            if incident_type in incident_types:
                self._incident_type = incident_type
            else:
                self._incident_type = None
                self.errors.append(
                    "Incident type should either be a 'red-flag' or 'intervention'")
        else:
            self._incident_type = None
            self.errors.append("Incident type should not be empty")

    @property
    def location(self):
        """Get location."""
        return self._location

    @location.setter
    def location(self, location):
        if not is_empty(location):
            coordinates = [x.strip() for x in location.split(',')]
            if len(coordinates) == 2:
                longitude = ''
                lat = ''
                try:
                    longitude = float(coordinates[0])
                    lat = float(coordinates[1])
                except:
                    longitude = None
                    lat = None
                if longitude is not None and lat is not None:
                    self._location = location
                else:
                    self.errors.append(
                            "Coordinates should be floating point values")
                    self._location = None
            else:
                self._location = None
                self.errors.append("Two coordinates required")
        else:
            self._location = None
            self.errors.append("Location should not be empty")

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        if not is_empty(comment):
            self._comment = comment
        else:
            self.errors.append("Comments cannot be empty")
            self._comment = None

    def describe_incident(self):
        """Return the object description.

        returns:
            dict: Incident properties

        """
        return {
            'Id': self.id,
            'Owner': self.created_by,
            'Date Created': str(self.created_on),
            'Incident Type': self.incident_type,
            'Location': self.location,
            'Status': self.status,
            'Comment': self.comment,
            'Images': self.images,
            'Videos': self.videos
        }


def is_empty(value):
    """Check if string is empty or whitespace."""
    if value.isspace() or value == "":
        return True
