import re
import json
import ipinfo


accessToken = '9f17e3535e20f4'
handler 	= ipinfo.getHandler(accessToken)

ip_address 	= '216.239.36.21'
details 	= handler.getDetails(ip_address)

IP 			= details.ip
org 		= details.org
city 		= details.city
country 	= details.country
region 		= details.region
location 	= details.loc

print ('Your IP detail\n')
print ('IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0} \nCoordinates : {5}'.format(org,region,country,city,IP,location))