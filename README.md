# ServerHeatMap
Visualize where people access your server using requests from Apache access log

## Getting Started

```batch
git clone https://github.com/SarangMohaniraj/ServerHeatMap.git
```

### Installation

```batch
pip install -r requirements.text
```

Make sure you install `python-geoip-geolite2` and `maxminddb-geolite2`. These allow you to get the longitude and latitude from the IP address.

### Usage

Put a copy of your own `access.log` or use the example taken from github.

Run `python main.py`. There are two types of heat maps you can choose from.

```python
plot(type="python") # opens in python
plot(type="folium") # opens a python server to display on a webpage
```
