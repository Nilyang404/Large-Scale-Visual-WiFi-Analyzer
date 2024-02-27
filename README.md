# Visual-WiFi-Analyzer

### 1. Description

A Solution for collecting and analyzing WiFi signals in large public areas. Suitable for public areas such as shopping malls, schools, gymnasiums, etc.

![heatmap](https://github.com/Nilyang404/Visual-WiFi-Analyzer/assets/63556313/65564109-f325-4c9a-94cb-c505fa4304fd)

By data collecting processing, visualization and analysis, we are able to  identify areas with weak signals on the campus and design the solutions to solve the problem of weak signals.

For Example, by deploying additional APs outside the nearest building in areas with weak signal. Judging from the results of data simulation, the solution will effectively improve the WIFI signal on the campus

### 2. How to collect data
This the CLI command part is designed for Windows PowerShell, for Mac Os or Linux, you may need to modify the CLI command part.
The collection of frequency, SSID, BSSID and other wifi information has been described in detail in the previous lab reports. For the public network IP data, I chose to query the public IP query server, it will response the public ip.

```python
def get_public_ip():
    response = requests.get('http://ipinfo.io/ip')
    public_ip = response.text.strip()
    return public_ip
```

Due to energy-saving reasons, the laptop network adapter will no longer search for all nearby wifi information once connected to a wifi. I need to click the wifi button to display all nearby wifi and always keep the wifi search window in the foreground. In addition, I set the Laptop to not sleep or shut down when closed. Then I can put it in my backpack while the program remains active, and walk around planned areas on campus to collect data until the activity track covers all areas.

### 3. How to merge GPS data

Since GPS recording software is able to record a tracking point every second, including longitude and latitude, accuracy, and time accurate to the second, which is the smallest unit of timestamp. Therefore, even if the response time of the delay test and public network IP request cannot be determined, the same GPS tracking time can always be found when check a single wifi collection timestamp. The two data sets can be merged on this basis. Fill in the latitude, longitude and accuracy information.

### 4. Data analysis and visualization

Use visualize.py to generate charts, heat maps, and draw maps from the merged data set.
![image](https://github.com/Nilyang404/Visual-WiFi-Analyzer/assets/63556313/7256880d-eaae-40d3-9f69-eeb625d46c30)
![data points](https://github.com/Nilyang404/Visual-WiFi-Analyzer/assets/63556313/59280e6a-01a3-4318-92a4-0a97f66fb6c1)
![map](https://github.com/Nilyang404/Visual-WiFi-Analyzer/assets/63556313/db8f4963-6e83-4f22-9ecf-3ff7788f6e55)
![image](https://github.com/Nilyang404/Visual-WiFi-Analyzer/assets/63556313/aa90917e-42c9-469c-8c68-88734a71b858)


