# craigslist-recommendation-system #

Craigslist is a popular website that provides local classified advertisements for housing, community services, jobs, etc. The site serves more than 20 billion page views per month, putting it in 72nd place overall among websites worldwide. However, especially for housing, the huge volume of options to choose from, with a not so intuitive website like Craigslist, can be overwhelming for a user who wants to quickly arrive at a decision. We decided to fix this problem, by designing a recommender system, that gives recommendations to the user, based on the user's requirements.


Follow instructions from Running.txt


The work flow can be represented in the below Data Flow Diagram:

![alt text](Images/DFDBD.png)

The Home page consists of filters to let the user enter a city and the number of bedroom(s). The heart icon allows the user to select a listingas favorite. After favoriting some listings, the user can move to the Favorites Tab at the top and view recommendations based on the favorited options.The analytics tab displays some insights about the overall Rental scene in Canada.

Technologies used:

Crawler was developed using the Python Scrapy library. The web front end was built using the Flask web framework. The charts were developed using Highcharts JS. For the back end, Pyspark libraries were used for computations. Cassandra was the Database. 


