# pamsched

A minimal, self-contained Python package for representing and parsing **recording schedules for Passive Acoustic Monitoring (PAM)** devices.

The package focuses **only** on the *data structure* for recording schedules, not on waveform I/O, analysis, or recorder-specific configuration files.

## Features

- **Device-agnostic** data model for PAM recording schedules.
- **JSON-based DSL** support (AudioMoth-style).
- **Python dataclasses** representing the DSL.
- **Parser** to load/dump schedules from/to JSON.

## JSON Schema

A [JSON Schema](http://json-schema.org/) for the recording schedule data model is available in [schema.json](schema.json). You can use this schema to validate your schedule files or to generate client code in other languages.

## Installation

```bash
pip install git+https://github.com/0kam/pamsched
```

## Usage

```python
from pamsched import loads, dumps, RecordingSchedule

# Load from JSON string
json_str = '{"version": "0.1.0", "pattern_type": "continuous", "continuous": {}}'
schedule = loads(json_str)
print(schedule)

# Dump to dict
data = dumps(schedule)
print(data)
```
