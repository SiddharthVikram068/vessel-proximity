# vessel-proximity

## Introduction
This github repository is an approach to identify instances where a vessel comes into proximity of the other. This event is called "vessel proximity".

Each ship is identified by a unique 9 digit number called the Maritime Mobile Service Identity (MMSI). The longitudes and latitudes of different ships are given at different timestamps. The input data is in the file sample_data.csv

## Approach

The most simple approach can be a brute force one, where we just take one time stamp and find distance between all ships with each other for that timestamp. This approach is a very unoptimised one.
With improvements with calculations in batches with vectorization in pandas, we are already saving a lot of time in calculations. We can also use scipy cKD Trees for efficient pair calculations whose distances are less than the threshold distance 

## Optimizations 
if we make the KDTree for all the pairs together, we will get a lot of unnecessary pairs consisting of same mmsi numbers and ships at different time stamps. So we make a different KDTree for every unique timestamp. This helps us reject a lot of unnecessary pairs we would need to iterate over if we create pairs for the whole data. 

The optimization is applied in the file vesselprox_opt.py and the improvement comes out to be ten times, decreasing the time from 5 seconds to 0.5 seconds 

