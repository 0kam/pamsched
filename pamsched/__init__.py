"""
pamsched: A minimal package for PAM recording schedules.
"""
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

from .parser import loads, dumps

__all__ = [
    "RecordingSchedule",
    "PatternType",
    "ContinuousPattern",
    "ScheduledPattern",
    "TriggeredPattern",
    "Window",
    "Cycle",
    "Trigger",
    "TriggerType",
    "SensorTrigger",
    "AudioTrigger",
    "EventTrigger",
    "loads",
    "dumps",
]
