import geoip2.database

reader = geoip2.database.Reader('C:\\Users\\dprefac\\Downloads\\GeoLite2-Country.mmdb')

print(reader.country("194.126.147.65"))
