"""
Parser module for reading and writing recording schedules.

This module provides functions to serialize and deserialize `RecordingSchedule`
objects to and from JSON-compatible dictionaries or strings.
"""
from __future__ import annotations

import json
from typing import Any, Dict, Union

from .models import (
    RecordingSchedule,
    PatternType,
    ContinuousPattern,
    ScheduledPattern,
    TriggeredPattern,
    Window,
    Cycle,
    Trigger,
    TriggerType,
    SensorTrigger,
    AudioTrigger,
    EventTrigger,
)

JsonType = Union[Dict[str, Any], str]


def loads(obj: JsonType) -> RecordingSchedule:
    """
    Parse a JSON string or Python dict into a RecordingSchedule instance.

    Parameters
    ----------
    obj : str or dict
        The input JSON string or dictionary representing the schedule.

    Returns
    -------
    RecordingSchedule
        The parsed recording schedule object.

    Raises
    ------
    ValueError
        If the input structure does not match the expected schema or
        contains invalid values.
    """
    if isinstance(obj, str):
        data: Dict[str, Any] = json.loads(obj)
    else:
        data = obj

    version = data.get("version", "0.1.0")
    pattern_type = PatternType(data["pattern_type"])

    continuous = None
    scheduled = None
    triggered = None

    if pattern_type is PatternType.CONTINUOUS:
        c = data["continuous"]
        continuous = ContinuousPattern(
            start_at=c.get("start_at"),
            end_at=c.get("end_at"),
        )

    elif pattern_type is PatternType.SCHEDULED:
        s = data["scheduled"]
        cycle_dict = s["cycle"]
        cycle = Cycle(
            record_seconds=cycle_dict["record_seconds"],
            sleep_seconds=cycle_dict["sleep_seconds"],
        )
        windows = [
            Window(
                window_type=w["window_type"],
                start=w["start"],
                end=w["end"],
                days_of_week=w.get("days_of_week"),
                months=w.get("months"),
            )
            for w in s["windows"]
        ]
        scheduled = ScheduledPattern(
            windows=windows,
            cycle=cycle,
            timezone=s.get("timezone"),
        )

    elif pattern_type is PatternType.TRIGGERED:
        t = data["triggered"]
        trigger_list = []
        for raw_trig in t["triggers"]:
            ttype = TriggerType(raw_trig["trigger_type"])
            sensor = audio = event = None

            if ttype is TriggerType.SENSOR and "sensor" in raw_trig:
                sdict = raw_trig["sensor"]
                sensor = SensorTrigger(
                    kind=sdict["kind"],
                    op=sdict["op"],
                    threshold=sdict["threshold"],
                )
            elif ttype is TriggerType.AUDIO and "audio" in raw_trig:
                adict = raw_trig["audio"]
                audio = AudioTrigger(
                    class_label=adict["class"],
                    min_confidence=adict["min_confidence"],
                )
            elif ttype is TriggerType.EVENT and "event" in raw_trig:
                edict = raw_trig["event"]
                event = EventTrigger(
                    name=edict["name"],
                    offset_seconds=edict.get("offset_seconds", 0),
                )

            trigger_list.append(
                Trigger(
                    trigger_type=ttype,
                    sensor=sensor,
                    audio=audio,
                    event=event,
                )
            )

        triggered = TriggeredPattern(
            triggers=trigger_list,
            max_duration=t.get("max_duration"),
        )

    return RecordingSchedule(
        version=version,
        pattern_type=pattern_type,
        continuous=continuous,
        scheduled=scheduled,
        triggered=triggered,
    )


def dumps(schedule: RecordingSchedule) -> Dict[str, Any]:
    """
    Serialize a RecordingSchedule instance into a Python dict.

    The returned dictionary is JSON-serializable and follows the DSL structure.

    Parameters
    ----------
    schedule : RecordingSchedule
        The recording schedule object to serialize.

    Returns
    -------
    dict
        A dictionary representation of the schedule.
    """
    data: Dict[str, Any] = {
        "version": schedule.version,
        "pattern_type": schedule.pattern_type.value,
    }

    if schedule.pattern_type is PatternType.CONTINUOUS and schedule.continuous:
        data["continuous"] = {
            "start_at": schedule.continuous.start_at,
            "end_at": schedule.continuous.end_at,
        }

    elif schedule.pattern_type is PatternType.SCHEDULED and schedule.scheduled:
        s = schedule.scheduled
        data["scheduled"] = {
            "timezone": s.timezone,
            "cycle": {
                "record_seconds": s.cycle.record_seconds,
                "sleep_seconds": s.cycle.sleep_seconds,
            },
            "windows": [
                {
                    "window_type": w.window_type,
                    "start": w.start,
                    "end": w.end,
                    "days_of_week": w.days_of_week,
                    "months": w.months,
                }
                for w in s.windows
            ],
        }

    elif schedule.pattern_type is PatternType.TRIGGERED and schedule.triggered:
        t = schedule.triggered
        data["triggered"] = {
            "max_duration": t.max_duration,
            "triggers": [],
        }
        for trig in t.triggers:
            item: Dict[str, Any] = {
                "trigger_type": trig.trigger_type.value
            }
            if trig.sensor is not None:
                item["sensor"] = {
                    "kind": trig.sensor.kind,
                    "op": trig.sensor.op,
                    "threshold": trig.sensor.threshold,
                }
            if trig.audio is not None:
                item["audio"] = {
                    "class": trig.audio.class_label,
                    "min_confidence": trig.audio.min_confidence,
                }
            if trig.event is not None:
                item["event"] = {
                    "name": trig.event.name,
                    "offset_seconds": trig.event.offset_seconds,
                }
            data["triggered"]["triggers"].append(item)

    return data
