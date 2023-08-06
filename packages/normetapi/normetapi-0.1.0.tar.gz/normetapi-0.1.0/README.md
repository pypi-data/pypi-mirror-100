# normetapi
A small Python library for interacting with the [MET Norway Weather API](https://api.met.no/).

## Installation

```bash
pip install normetapi
```

## Examples

### Getting a forecast for a specified location:

```python
from normetapi import location_forecast

# Get forecast for Trondheim:
forecast = location_forecast(63.4107, 10.4538)
print(forecast)
```

The forecast will be returned as a dictionary. See the description
of [locationforecast](https://api.met.no/weatherapi/locationforecast/2.0/documentation)
and the [data model](https://api.met.no/doc/locationforecast/datamodel)
in the [MET Norway Weather API description](https://api.met.no/).

### Getting the immediate forecast for a specified location:

```python
from normetapi import nowcast

# Get nowcast for Trondheim:
forecast = nowcast(63.4107, 10.4538, altitude=123)
print(forecast)
```

The forecast will be returned as a dictionary. See the description
of [nowcast](https://api.met.no/weatherapi/nowcast/2.0/documentation)
and the [data model](https://api.met.no/doc/locationforecast/datamodel)
in the [MET Norway Weather API description](https://api.met.no/).

### Getting weather icons:

```python
from normetapi import weathericon

# Get icons:
_, legend = weathericon(output_file='icons.tgz')
print(legend)
```

This will download weather icons as a gzipped tar archive
and return legends as a dictionary. See the
description of [weathericon](https://api.met.no/weatherapi/weathericon/2.0/documentation)
in the [MET Norway Weather API description](https://api.met.no/).

## Terms of service

Please read the [terms of service](https://api.met.no/doc/TermsOfService).
In particular, to quote the terms of service:

> All requests must (if possible) include an identifying User Agent-string (UA)
> in the request with the application/domain name, optionally version number.

Please modify the ``USER_AGENT`` variable in [api.py](normetapi/api.py) to fit your
intended use.
