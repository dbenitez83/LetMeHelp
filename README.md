# Visualizing Geographic Statistical Data with Google Maps

This repository contains the code that I used to build a custom Google Maps based map to visualize geographic statistical data. As an example, I plotted the relative median income and population density of postal code areas in Finland. You can find more details about how the map was created on [my blog](https://nholmber.github.io/2018/08/gmaps-statistics/).

To reproduce the map and open it up in a browser, you can follow these steps

1. Register an account on the [Google Cloud Platform](https://cloud.google.com/maps-platform) to obtain an API key in order to use the Google Maps JS API. Registration is free, although a credit card is required. Free quota is available for the Google Maps API.
2. Add your API key to the [key.py](key.py) file.
3. Run the [map.py](map.py) script: `python map.py`.