"""
Data models for PAM recording schedules.

This module defines the dataclasses that represent the recording schedule DSL.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Literal


class PatternType(str, Enum):
    """
    Enumeration of supported recording pattern types.

    Attributes
    ----------
    CONTINUOUS : str
        "continuous" pattern.
    SCHEDULED : str
        "scheduled" pattern.
    TRIGGERED : str
        "triggered" pattern.
    """
    CONTINUOUS = "continuous"
    SCHEDULED = "scheduled"
    TRIGGERED = "triggered"


@dataclass
class ContinuousPattern:
    """
    Represents a continuous recording pattern.

    Parameters
    ----------
    start_at : str, optional
        ISO 8601 datetime string indicating when to start recording.
        If None, starts immediately.
    end_at : str, optional
        ISO 8601 datetime string indicating when to stop recording.
        If None, records indefinitely until stopped.
    """
    start_at: Optional[str] = None
    end_at: Optional[str] = None


@dataclass
class Cycle:
    """
    Represents a duty cycle for recording.

    Parameters
    ----------
    record_seconds : int
        Number of seconds to record.
    sleep_seconds : int
        Number of seconds to sleep between recordings.
    """
    record_seconds: int
    sleep_seconds: int


WindowType = Literal["fixed", "solar"]


@dataclass
class Window:
    """
    Represents a time window for scheduled recording.

    Parameters
    ----------
    window_type : WindowType
        Type of the window, either "fixed" or "solar".
    start : str
        Start time of the window.
        Format: "HH:MM" for fixed windows, or e.g. "sunrise-10m" for solar.
    end : str
        End time of the window.
        Format: "HH:MM" for fixed windows, or e.g. "sunset+10m" for solar.
    days_of_week : list of str, optional
        List of days of the week to apply this window (e.g., ["Mon", "Tue"]).
        If None, applies to all days.
    months : list of int, optional
        List of months (1-12) to apply this window.
        If None, applies to all months.
    """
    window_type: WindowType
    start: str
    end: str
    days_of_week: Optional[List[str]] = None
    months: Optional[List[int]] = None


@dataclass
class ScheduledPattern:
    """
    Represents a scheduled recording pattern.

    Parameters
    ----------
    windows : list of Window
        List of time windows during which the schedule is active.
    cycle : Cycle
        Duty cycle configuration to apply within the active windows.
    timezone : str, optional
        IANA timezone string (e.g., "Asia/Tokyo").
        If None, implies UTC or device local time depending on context.
    """
    windows: List[Window]
    cycle: Cycle
    timezone: Optional[str] = None


class TriggerType(str, Enum):
    """
    Enumeration of supported trigger types.

    Attributes
    ----------
    SENSOR : str
        Trigger based on sensor readings.
    AUDIO : str
        Trigger based on audio classification/detection.
    EVENT : str
        Trigger based on abstract named events.
    """
    SENSOR = "sensor"
    AUDIO = "audio"
    EVENT = "event"


@dataclass
class SensorTrigger:
    """
    Configuration for a sensor-based trigger.

    Parameters
    ----------
    kind : str
        Type of sensor (e.g., "temperature_c", "light_lux", "battery_v").
    op : str
        Comparison operator (">", ">=", "<", "<=").
    threshold : float
        Threshold value for the trigger.
    """
    kind: str
    op: str
    threshold: float


@dataclass
class AudioTrigger:
    """
    Configuration for an audio-based trigger.

    Parameters
    ----------
    class_label : str
        Label of the audio class to detect (e.g., "bird").
    min_confidence : float
        Minimum confidence score required to trigger (0.0 to 1.0).
    """
    class_label: str
    min_confidence: float


@dataclass
class EventTrigger:
    """
    Configuration for an event-based trigger.

    Parameters
    ----------
    name : str
        Name of the event (e.g., "rain_stopped").
    offset_seconds : int, default=0
        Time offset in seconds relative to the event.
    """
    name: str
    offset_seconds: int = 0


@dataclass
class Trigger:
    """
    Represents a single trigger configuration.

    Parameters
    ----------
    trigger_type : TriggerType
        The type of trigger.
    sensor : SensorTrigger, optional
        Configuration for sensor trigger. Required if trigger_type is SENSOR.
    audio : AudioTrigger, optional
        Configuration for audio trigger. Required if trigger_type is AUDIO.
    event : EventTrigger, optional
        Configuration for event trigger. Required if trigger_type is EVENT.
    """
    trigger_type: TriggerType
    sensor: Optional[SensorTrigger] = None
    audio: Optional[AudioTrigger] = None
    event: Optional[EventTrigger] = None


@dataclass
class TriggeredPattern:
    """
    Represents a triggered recording pattern.

    Parameters
    ----------
    triggers : list of Trigger
        List of triggers that can activate recording.
    max_duration : int, optional
        Maximum duration in seconds for a single triggered recording.
    """
    triggers: List[Trigger]
    max_duration: Optional[int] = None


@dataclass
class RecordingSchedule:
    """
    Root object representing a complete recording schedule.

    Parameters
    ----------
    version : str
        Version of the DSL used (e.g., "0.1.0").
    pattern_type : PatternType
        The active pattern type ("continuous", "scheduled", or "triggered").
    continuous : ContinuousPattern, optional
        Configuration for continuous pattern. Required if pattern_type is CONTINUOUS.
    scheduled : ScheduledPattern, optional
        Configuration for scheduled pattern. Required if pattern_type is SCHEDULED.
    triggered : TriggeredPattern, optional
        Configuration for triggered pattern. Required if pattern_type is TRIGGERED.
    """
    version: str
    pattern_type: PatternType
    continuous: Optional[ContinuousPattern] = None
    scheduled: Optional[ScheduledPattern] = None
    triggered: Optional[TriggeredPattern] = None
