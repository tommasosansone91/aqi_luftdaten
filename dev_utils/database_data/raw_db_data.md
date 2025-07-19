

AreaParametersSet

milano
45.464145 
9.190407
6

roma
41.8901712
12.4922954
9


milano timehorizon=1day timedelta=1h



------------




  PGPASSWORD=aqigdmain pg_dump -U aqigd_main -d aqi_graphs_dashboard -t pm_lookup_AreaParametersSet \
  --data-only \
  --inserts \
  --column-inserts \
  | awk '/Milano/'