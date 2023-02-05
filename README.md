# TfL Status API

Currently has a limited scope of functionality, can be used for current Underground status, weekend Underground closures, and London's Santander Bike Hire Scheme to check if bikes are available at any given station. All data is taken live from the [TfL XML Unified API](https://tfl.gov.uk/info-for/open-data-users/unified-api) and converted into a JSON format that is easy to work with (hopefully). You can see it in use on the [website](https://tfl.cxllm.co.uk/)

## Underground Status Checker

[`https://tfl.cxllm.co.uk/underground`](https://tfl.cxllm.co.uk/underground)

Returns an object with two keys:

```json
{
    "current_status": {...},
    "weekend_closures": {...}
}
```

### Current Status

Inside `current_status`, you can find the current operating status of all London tube lines, and this is updated in real time every time you request the route. It contains many objects, with the keys being the line names, i.e. `bakerloo, hammersmithandcity, jubilee, ...`. The objects contain this format of data:

```json
"linename": {
    "affected_stations": [], // the branch of the line affected by the incident (if there are 3 stations, this represents this branch: station 0 to station 1 via station 2)
    "details": null, // details of the a closure if there is one
    "line": "Line Name", // the line name
    "status": "Good Service" // the current status of the line, if all is operating well this will say "Good Service", and the details and affected_stations won't have values.
},
```

For example, this was an incident on the Metropolitan line on 23/05/2022:

```json
    "metropolitan": {
      "affected_stations": [
        [
          "Harrow-on-the-Hill",
          "Uxbridge"
        ]
      ],
      "details": "Minor delays between Harrow - on - the Hill and Uxbridge due to a customer incident. Good service on the rest of the line.",
      "line": "Metropolitan",
      "status": "Minor Delays"
    },
```

### Weekend Closures

The `weekend_closures` key shows the closures planned for the weekend on the Underground. It contains many objects, with the keys being the line names, i.e. `bakerloo, hammersmithandcity, jubilee, ...`. The objects contain this format of data:

```json
"linename": {
    "details": null, // details of a closure if there is one
    "is_closed": false, // if the line will be closed at the weekend
    "name": "Line Name", // the name of the line
    "status": "Good Service"  // the expected weekend status at this stage
},
```

For example, these were the planned closures for the Victoria Line for 28/05/2022 - 29/05/2022 found on 23/05/2022

```json
"victoria": {
    "details": "RMT STRIKE ACTION: There is planned strike action every Friday and Saturday night between 2030 and 0429 the following morning until Sunday 19 June. Central and Victoria lines could be affected. A good service is expected on the Victoria line (including Night Tube). A regular service is expected on the Central line (at least two trains per hour through central London).  Please check your travel if you are using these lines before 0600 on Saturday or Sundays. All other Tube lines will run their normal daytime services during these strikes, with the last Tubes in central London leaving around 01:00 and starting again at 05:30.",
    "is_closed": true,
    "name": "Victoria",
    "status": "Special Service"
},
```

## Santander Bike Hire

[`https://tfl.cxllm.co.uk/bikes`](https://tfl.cxllm.co.uk/bikes)

With this you can find up-to-date information on the Santander Bike Hire scheme, finding out the co-ordinates of all the stations, and how many bikes are available there, and how many docks there are in total.

The URL returns an array with all of stations in London, and each one has this data format (this shows data for a Clerkenwell station but the data format would be the same for each one):

```json
{
    "bikes_available": 1, // Number of bikes available at this station
    "coordinates": {
      "latitude": 51.52916347, // Co-ordinates of the station
      "longitude": -0.109970527
    },
    "id": 1,
    "name": "River Street, Clerkenwell", // Where it is located
    "number_of_docks": 19, // Number of docking stations for bikes
    "terminal_name": "001023" // TfL terminal name for the station
},

```
