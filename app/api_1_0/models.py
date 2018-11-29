"""Contains the models for the data."""
import datetime

import re


class IncidentValidators(object):
    """Validates an Incident object data."""

    def __init__(self):
        self.errors = []

    def validate_creator(self, creator):
        """Verify and set created_by."""
        if not is_empty(creator):
            created_by = ''
            try:
                created_by = int(creator)
            except:
                created_by = None
            if created_by is not None:
                return True
            else:
                self.errors.append("Created by should be an Integer")
                return False
        else:
            self.errors.append("Incident owner should not be blank")
            return False

    def validate_title(self, title):
        """Validate Title."""
        if not is_empty(title):
            if re.match("^[a-zA-Z0-9 _]*$", title):
                return True
            else:
                self.errors.append(("Title cannot contain special characters"))
        else:
            self.errors.append("Title cannot be empty")
            return False

    def validate_incident_type(self, incident_type):
        """Validate the incident type."""
        if not is_empty(incident_type):
            incident_types = ["red-flag", "intervention"]
            if incident_type in incident_types:
                return True
            else:
                self.errors.append(
                    "Incident type should either be a 'red-flag' or 'intervention'")
                return False
        else:
            self.errors.append("Incident type should not be empty")
            return False

    def validate_location(self, location):
        """Validate location."""
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
                    return True
                else:
                    self.errors.append(
                            "Coordinates should be floating point values")
                    return False
            else:
                self.errors.append("Two coordinates required")
                return False
        else:
            self.errors.append("Location should not be empty")
            return False

    def validate_comment(self, comment):
        """Validate comment."""
        if not is_empty(comment):
            return True
        else:
            self.errors.append("Comments cannot be empty")
            return False


def is_empty(value):
    """Check if string is empty or whitespace."""
    if value.isspace() or value == "":
        return True


class IncidentModel(IncidentValidators):
    """This class models an Incident."""

    def __init__(self, created_by, incident_type, location, title, comment):
        """Initialize an Incident object.

        args:
            created_by(str): incident owner
            type(str): either of intervention or red-flag
            location(str): longituted, latitude coordinates
            status(str): draft, under investigation, resolved or rejected
            comment(str): A description of the incident
        """
        super().__init__()
        self.id = ''
        self.created_by = created_by
        self.created_on = datetime.datetime.now()
        self.incident_type = incident_type
        self.location = location
        self.status = ''
        self.title = title
        self.unique_identifier = ''
        self.comment = comment
        self.images = []
        self.videos = []

    def save(self, db):
        """Save incident to db.

        args:
            db(list): The list into which to save the incident.
        """
        if self.validate_creator(self.created_by) and \
           self.validate_incident_type(self.incident_type) and \
           self.validate_location(self.location) and \
           self.validate_comment(self.comment) and \
           self.validate_title(self.title):
            self.id = len(db) + 1
            db.append({self.id: self.describe_incident()})
            return {'status': True, 'message': {"Id": self.id,
                    "message": "Successfuly created incident"}}
        else:
            return {'status': False, 'message': {'errors': self.errors}}

    @classmethod
    def find_incident(cls, incident_id, incident_list):
        """Retrieve an incident."""
        for incident in incident_list:
            for key, value in incident.items():
                if str(key) == str(incident_id):
                    return value

    @classmethod
    def update_incident(cls, incident_id, incident_list, data):
        """Update an incident."""
        incident = cls.find_incident(incident_id, incident_list)
        if isinstance(incident, dict):
            for value in incident_list:
                for key, value in value.items():
                    if str(key) == str(incident_id):
                        value.update(data)
                        return {'status': True, 'message': value}
        return {'status': False, 'message': 'That resource cannot be found'}

    @classmethod
    def delete_incident(cls, incident_id, incident_list):
        """Delete an incident."""
        for incident in incident_list:
            for key, value in incident.items():
                if str(key) == str(incident_id):
                    incident_list.remove(incident)
                    return True

    def describe_incident(self):
        """Return the object description.

        returns:
            dict: Incident properties

        """
        return {
            'Id': self.id,
            'Created By': int(self.created_by),
            'Date Created': str(self.created_on),
            'Type': self.incident_type,
            'Location': self.location,
            'Status': self.status,
            'Comment': self.comment,
            'Images': self.images,
            'Videos': self.videos,
            'Title': self.title,
            'Unique Identifier': self.unique_identifier
        }
