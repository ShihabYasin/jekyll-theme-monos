---
layout: post
title: Ride-Sharing-Algorithm-Analysis
date: 2022-01-06 16:20:23 +0900
category: Algorithm
tag: Algorithm
---

## Uber, Lyft Ride Sharing Algorithm Implementation Analysis:

### Some definition(s):

1. **Batched Matching**: Some r-distance (threshold) geo-fenced rider(s) (that might come dynamically) at some point of time(t) will create a Batch of Riders (B). All riders each having an r radius geo-fenced circle form a bigger region R, all drivers in R are candidate drivers to be dispatched for all riders of B, within t & t+P (definition of P is below) time duration.
2. **Intelligent Matching**: If dynamically a driver popup whose distance is closer than an already dispatched driver to a rider then this ride will shift to the new driver, if ETA of old driver to reach rider is higher than a threshold time duration(T) that is statistically/empirically chosen over cost gain. Driver who is currently riding a trip and drops off near to a new rider is also a candidate driver.

### **Algorithm Description**:

* Form different sets of B periodically (P,  P<<T) considering “Intelligent Matching” over different regions of interest (e.g. New York) such that overlapping regions are minimal.
* Using ETA info of vehicles (using geohash or based on precalculated/predefined weights), as weights, from a rider calculate weighted A* path distance. For each rider assign lowest distance driver, if more than 2 drivers available assign lower priced driver, to resolve further conflict do coin toss. After assigning a driver to a rider that driver will be unavailable for other riders(while counting weighted A* path distance).

* While pathfinding using A* consider at most 2r geo-distance to search for drivers/vehicles.


### **Pre-Calculate & Parallel Compute:**

* Introduce pre-calculated pick-up hotspot points to riders (on app) to start riding from, against all available drivers within a certain geo-fenced region pR, to reduce pick-up time and to dispatch appropriate drivers to the rider based on minimal costing.
* Calculate supply and demand forecasting using data science based on app usage history of riders and active vehicle/driver movement data (direction, speed, position, time, costing etc.) on a particular hour of a day/week/year.
* Deploy forecasting data when available to pre-calculate pick-up hotspots.
