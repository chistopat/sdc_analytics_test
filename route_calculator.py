import itertools
import json
import operator
import typing

import models


def fetch_geo_data(text: typing.List[str]) -> typing.List[models.GeoMessage]:
    messages: typing.List[models.GeoMessage] = []
    for row in text:
        data = json.loads(row)
        if 'geo' in row:
            messages.append(models.GeoMessage(data))

    return sorted(messages, key=operator.attrgetter('utc_dttm'))


def fetch_control_data(
        text: typing.List[str],
) -> typing.List[models.ControlMessage]:
    messages: typing.List[models.ControlMessage] = []
    for row in text:
        data = json.loads(row)
        if 'control_switch_on' in row:
            messages.append(models.ControlMessage(data))

    return sorted(messages, key=operator.attrgetter('utc_dttm'))


def find_selfdrived_time(
        messages: typing.List[models.ControlMessage],
) -> typing.List[models.SelfdrivedInterval]:
    intervals: typing.List[models.SelfdrivedInterval] = []
    periods = itertools.groupby(messages,
                                operator.attrgetter('control_switch_on'))
    for is_selfdrived, timeseries in periods:
        if is_selfdrived:
            intervals.append(models.SelfdrivedInterval(list(timeseries)))
    return intervals


def filter_stops(
        messages: typing.List[models.GeoMessage],
) -> typing.List[models.GeoMessage]:
    groups = itertools.groupby(messages, key=operator.attrgetter('geo'))
    return [min(group[1], key=operator.attrgetter('utc_dttm'))
            for group in groups]


def split_by_seconds(
        messages: typing.List[models.GeoMessage],
) -> typing.List[models.GeoMessage]:
    groups = itertools.groupby(messages, key=operator.attrgetter('utc_dttm'))
    return [max(group[1], key=operator.attrgetter('geo'))
            for group in groups]


def compare_coordinates(
        messages: typing.List[models.GeoMessage],
) -> typing.List[models.Segment]:
    segments: typing.List[models.Segment] = []
    messages.sort(key=operator.attrgetter('utc_dttm'))
    for i, msg in enumerate(messages):
        if i+1 != len(messages):
            segments.append(models.Segment((messages[i], messages[i+1])))
    return segments


def check_time(
        interval: models.SelfdrivedInterval,
        segment: models.Segment,
) -> bool:
    if interval.begin_time <= segment.arrival_time <= interval.end_time:
        return True
    return False


def who_was_drive(
        intervals: typing.List[models.SelfdrivedInterval],
        segments: typing.List[models.Segment],
):
    for seg in segments:
        checks: typing.List[bool] = []
        for i in intervals:
            checks.append(check_time(i, seg))
        seg.is_selfdrived = any(checks)
    return segments


def get_routes_info(segments: typing.List[models.Segment]):
    results: typing.List[models.RouteInfo] = []
    groups = itertools.groupby(segments,
                               key=operator.attrgetter('is_selfdrived'))

    for is_selfdrived, group in groups:
        route_segments = tuple(group)
        distance_list = map(operator.attrgetter('distance'), route_segments)
        first_segment = min(route_segments,
                            key=operator.attrgetter('arrival_time'))
        last_segment = max(route_segments,
                           key=operator.attrgetter('destination_time'))
        arrival_point = str(first_segment.arrival_point)
        arrival_time = first_segment.arrival_time.isoformat()
        destination_point = str(last_segment.destination_point)
        destination_time = last_segment.destination_time.isoformat()

        results.append(models.RouteInfo(is_selfdrived=is_selfdrived,
                                        distance=sum(list(distance_list)),
                                        units='Meters',
                                        trip_time=len(route_segments),
                                        segments=route_segments,
                                        arrival_point=arrival_point,
                                        arrival_time=arrival_time,
                                        destination_time=destination_time,
                                        destination_point=destination_point,
                                        ))
    return results


def route_calculator(data: typing.Any) -> typing.List[models.RouteInfo]:
    geo_messages = fetch_geo_data(data)
    control_messages = fetch_control_data(data)
    uniq_geo = filter_stops(geo_messages)
    splited_geo = split_by_seconds(uniq_geo)
    selfdrived_intervals = find_selfdrived_time(control_messages)
    all_segments = compare_coordinates(splited_geo)
    all_segments = who_was_drive(selfdrived_intervals, all_segments)
    routes = get_routes_info(all_segments)
    return routes


def do_stuff():
    with open('data', 'r') as file_obj:
        raw_data = file_obj.readlines()

        for r in route_calculator(raw_data):
            print(r.serialize())


if __name__ == '__main__':
    do_stuff()
