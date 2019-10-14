import dataclasses
import datetime
import json
import operator
import typing

import haversine


class GeoMessage:
    def __init__(self, msg: dict):
        self.geo = (msg['geo']['lat'], msg['geo']['lon'])
        self.utc_dttm = datetime.datetime.utcfromtimestamp(msg['ts'] // 10**9)

    def __repr__(self):
        return '{}, {}'.format(self.geo, self.utc_dttm)


class ControlMessage:
    def __init__(self, msg: dict):
        self.control_switch_on = msg['control_switch_on']
        self.utc_dttm = datetime.datetime.utcfromtimestamp(msg['ts'] / 10**9)


class SelfdrivedInterval:
    def __init__(self, time_series: typing.List[ControlMessage]):
        key = operator.attrgetter('utc_dttm')
        self.begin_time = min(time_series, key=key).utc_dttm
        self.end_time = max(time_series, key=key).utc_dttm

    def __repr__(self):
        return '"{}, {}"'.format(self.begin_time, self.end_time)


@dataclasses.dataclass
class Segment:
    is_selfdrived: typing.Optional[bool]

    def __init__(self, data: typing.Tuple[GeoMessage, GeoMessage]):
        arrival = data[0]
        destination = data[1]
        self.arrival_point = arrival.geo
        self.arrival_time = arrival.utc_dttm
        self.destination_point = destination.geo
        self.destination_time = destination.utc_dttm
        self.trip_time = self.destination_time - self.arrival_time
        self.distance = haversine.haversine(self.destination_point,
                                            self.arrival_point,
                                            haversine.Unit.METERS)

    def serialize(self):
        return json.dumps(self.prepare())

    def prepare(self):
        return {
                'arrival_point': format('{}, {}'.format(*self.arrival_point)),
                'arrival_time': self.arrival_time.strftime(
                    '%Y-%m-%dT%H:%M:%S.%f+0000'),
                'destination_point': format('{}, {}'.format(
                    *self.destination_point)),
                'destination_time': self.destination_time.strftime(
                    '%Y-%m-%dT%H:%M:%S.%f+0000'),
                'trip_time': self.trip_time.microseconds,
                'distance': self.distance,
                'is_selfdrived': self.is_selfdrived,
            }


@dataclasses.dataclass
class RouteInfo:
    is_selfdrived: bool
    distance: float
    units: str
    trip_time: float
    segments: typing.Tuple[Segment, ...]
    arrival_point: str
    arrival_time: str
    destination_point: str
    destination_time: str

    def serialize(self):
        return json.dumps({
            'is_selfdrived': self.is_selfdrived,
            'distance': self.distance,
            'units': self.units,
            'trip_time': self.trip_time,
            'arrival_point': self.arrival_point,
            'arrival_time': self.arrival_time,
            'destination_point': self.destination_point,
            'destination_time': self.destination_time,
        })
