# Python version: Python3
# Sys Env : Windows
# #########################################
# by Neil
# #########################################
import subprocess
import re
from datetime import datetime
import time
import math
import pandas as pd
import matplotlib.pyplot as plt
import csv
import requests
# from pynput import keyboard
import keyboard
import sys
import io
TARGET_SSID = "uniwide"

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

"""
Description:
Get and return current connected wifi infomation
"""
def get_public_ip():
    response = requests.get('http://ipinfo.io/ip')
    public_ip = response.text.strip()
    return public_ip

def get_network_delay(ip):
    command = 'ping -n ' + str(1) + " " + ip
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    text = result.stdout
    times = re.findall(r'time=(\d+)ms', text)
    times = [int(t) for t in times]
    if len(times) >=1:
        return times[0]
    else:
        return -1

def task_1_get_ping_info(pack_amount,ip):
    command = 'ping -n ' +str(pack_amount) + " " + ip
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    text = result.stdout
    print(text)
    times = re.findall(r'time=(\d+)ms', text)
    times = [int(t) for t in times]

    df = pd.DataFrame(times, columns=['Time (ms)'])
    df.to_csv('task_1.csv', index=False)
    print(df)
    return df
def task_1_plot_csv(csv_file):
    df = pd.read_csv(csv_file)
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Time (ms)'], marker='o')
    plt.xlabel('Packet Index')
    plt.ylabel('Time (ms)')
    plt.title('Ping Response Times')
    plt.grid(True)
    plt.xticks(df.index[::5])
    plt.tight_layout()
    plt.savefig("ping_plot.png")
    plt.show()
"""
Return the SSID of current connected wifi
"""
def get_current_wifi_SSID():
    command = 'netsh wlan show interfaces'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    text = result.stdout
    # print(text)
    # text.replace(" \n","")
    pattern = r'(?s)([a-zA-Z\s\(\)0-9]+)\s*:\s*([a-zA-Z0-9%_:.\s-]+?)(?=\n\s*[a-zA-Z\s\(\)0-9]|$)'
    # pattern = r'([a-zA-Z\s\(\)0-9]+)\s*:\s*([a-zA-Z0-9%_:.\s-]+)'
    matches = re.findall(pattern, text)
    formated_match = {}
    for field, value in matches:
        # print(f"{field.strip()} : {value.strip()}")
        formated_match[field.strip()] = value.strip()
    # deal with condition without connection
    if "SSID" in formated_match.keys():
        return formated_match["SSID"]
    else:
        return ""
def get_current_wifi_BSSID():
    command = 'netsh wlan show interfaces'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    text = result.stdout
    # print(text)
    # text.replace(" \n","")
    pattern = r'(?s)([a-zA-Z\s\(\)0-9]+)\s*:\s*([a-zA-Z0-9%_:.\s-]+?)(?=\n\s*[a-zA-Z\s\(\)0-9]|$)'
    # pattern = r'([a-zA-Z\s\(\)0-9]+)\s*:\s*([a-zA-Z0-9%_:.\s-]+)'
    matches = re.findall(pattern, text)
    formated_match = {}
    for field, value in matches:
        # print(f"{field.strip()} : {value.strip()}")
        formated_match[field.strip()] = value.strip()
    # deal with condition without connection
    if "BSSID" in formated_match.keys():
        return formated_match["BSSID"]
    else:
        return ""
def show_time_info():
    now = datetime.now()
    # format time
    formatted_time = now.strftime("Current time: %A, %d %B %Y %H:%M:%S")
    # timestamp
    timestamp = int(time.time())
    print(formatted_time)
    print(f"Timestamp: {timestamp}")

def show_current_wifi():
    if get_current_wifi_SSID() != "":
        print(f"WiFi status: Connected ({get_current_wifi_SSID()})")
    else:
        print(f"WiFi status: Unconnected")

def show_all_AP_infos(df):
    col_widths = [max(len(str(item)) for item in df[col].tolist() + [col]) for col in df.columns]
    header = df.columns.tolist()
    header_line = '|'.join([header[i].ljust(col_widths[i]) for i in range(len(header))])
    print(header_line)
    print("+".join('-' * (width) for width in col_widths))

    for _, row in df.iterrows():
        print('|'.join([str(row[col]).ljust(col_widths[i]) for i, col in enumerate(df.columns)]))
        print("+".join('-' * (width) for width in col_widths))
"""
Description:
Run the shell code and return stdout text
"""
def get_wifi_info():
    command = 'netsh wlan show networks mode=Bssid'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    text = result.stdout
    # text.replace(" \n","")
    return text
"""
Description:
Parse the text to a dict which is easier to get field and value
return a dict
"""
def get_SSID_list(text):
    pattern = r"(SSID \d+ : [^\n]+(?:\n(?!SSID \d+ :).*)+)"
    matches = re.findall(pattern, text)

    # for i in matches:
    #     print(i)
    #     print("-" * 10)
    return matches

def get_BSSID_list(SSID_text):
    pattern = r"(BSSID \d+[\s\S]+?)(?=BSSID \d+|$)"
    matches = re.findall(pattern, SSID_text)
    return matches

def parse_wifi_info(info):
    pattern = r'(?s)([a-zA-Z\s\(\)0-9]+)\s*:\s*([a-zA-Z0-9%_:.\s-]+?)(?=\n\s*[a-zA-Z\s\(\)0-9]|$)'
    # pattern = r'([a-zA-Z\s\(\)0-9]+)\s*:\s*([a-zA-Z0-9%_:.\s-]+)'
    matches = re.findall(pattern, info)
    formated_match = {}
    for field, value in matches:
        # print(f"{field.strip()} : {value.strip()}")
        formated_match[field.strip()] = value.strip()

    return formated_match
## return a list sorted by SSID
def channel_to_frequency(channel):
    if int(channel) <= 11:
        return "2.4 GHz"
    else:
        return "5 GHz"
def get_channel_width(radio_type):
    if radio_type == "802.11n":
        return 40.0
    else:
        return 80.0

def percentage_to_signal_strength(percentage):
    percentage = int(percentage.replace("%",""))
    return percentage/2 -100

"""
input : a str of all info of wifi info
output: a list which contains parsed firld and value of each BSSID as dict
"""
def get_formated_wifi_info(text):
    SSID_list = get_SSID_list(text)
    data_list = []
    timestamp = int(time.time())
    for SSID_text in SSID_list:

        SSID = re.search(r"SSID \d+ : (\w+)", SSID_text).group(1)
        BSSID_list = get_BSSID_list(SSID_text)
        for i in BSSID_list:
            k = re.sub(r"BSSID \d+", "BSSID", i)
            parsed_BSSID_info = parse_wifi_info(k)
            bss_info = {}
            bss_info["time"] = timestamp
            bss_info["os"] = "Windows 10"
            bss_info["network interface"] = "Intel(R) Wireless-AC 9560 160MHz"
            bss_info["gps latitude"] = float(-1)
            bss_info["gps longitude"] = float(-1)
            bss_info["gps accuracy (meters)"] = float(-1)
            bss_info["ssid"] = SSID
            bss_info["bssid"] = parsed_BSSID_info["BSSID"]
            bss_info["wi-fi standard"] = parsed_BSSID_info["Radio type"]
            # bss_info["Signal"] = parsed_BSSID_info["Signal"]
            bss_info["rssi (in dbm)"] = float(percentage_to_signal_strength(parsed_BSSID_info["Signal"]))
            bss_info["network channel"] = int(parsed_BSSID_info["Channel"])
            bss_info["frequency"] = channel_to_frequency(bss_info["network channel"])
            bss_info["channel width (in mhz)"] = float(get_channel_width(parsed_BSSID_info["Radio type"]))
            bss_info["noise level (in dbm)"] = None
            current_BSSID = get_current_wifi_BSSID()
            if bss_info["ssid"] == TARGET_SSID and get_current_wifi_SSID() != "" and current_BSSID == bss_info["bssid"]:
                try:
                    bss_info["public ip address"] = get_public_ip()
                    bss_info["network delay (in ms)"] = float(get_network_delay("unsw.edu.au"))
                except Exception as e:
                    # 这里处理异常
                    print(f"error：{e}")
                    bss_info["public ip address"] = None
                    bss_info["network delay (in ms)"] = None
            else:
                bss_info["public ip address"] = None
                bss_info["network delay (in ms)"] = None
            # for o,p in bss_info.items():
            #     print(o,p)
            data_list.append(bss_info)

    return data_list
class Collect:
    def __init__(self):
        self.df = pd.read_csv("new csv template.csv")
        #
        self.df = self.df.iloc[0:0]
        # self.stop_flag = False

    def collect_data_run(self):
        # self.stop_flag = False
        while True:
            try:
                if keyboard.is_pressed('f6'):
                    print("F6 pressed. Exiting the loop...")
                    self.save_file()
                    break
                text_wifi_info = get_wifi_info()
                data_list = get_formated_wifi_info(text_wifi_info)
                df_temp = pd.DataFrame(data_list)
                # df = df.append(df_temp, ignore_index=True)
                self.df = pd.concat([self.df, df_temp], ignore_index=True)
                show_all_AP_infos(df_temp)
                # time.sleep(0.1)
            except Exception as e:
                continue
    def collect_stop(self):
        self.stop_flag = True
    def save_file(self):
        print()
        self.df.to_csv("data_2.csv")
        print(f"Table output to csv file: data_2.csv")

    # def on_key_release(self,key):
    #     if key == keyboard.Key.f4:
    #         self.collect_data_run()
    #     if key == keyboard.Key.f5:
    #         self.collect_stop()
    # def run(self):
    #     with keyboard.Listener(on_release=self.on_key_release) as listener:
    #         listener.join()

if __name__ == "__main__":
    global_STOP_FLAG = False
    show_time_info()
    show_current_wifi()
    # text_wifi_info = get_wifi_info()
    # df = pd.read_csv("new csv template.csv")
    # df = df.iloc[0:0]
    # def on_key_release(key):
    #     if key == keyboard.Key.f4:
    #         collect_data_run(df)
    #     if key == keyboard.Key.f5:
    #         collect_stop()
    # df = pd.DataFrame(data_list)
    # unique_ssid_count = df['BSSID'].nunique()
    # print(f"There are {unique_ssid_count} APs visible:\n")
    # with keyboard.Listener(on_release=on_key_release) as listener:
    #     listener.join()
    test = Collect()
    test.collect_data_run()
    # print()
    # df.to_csv("data.csv")
    # print(f"Table output to csv file: data.csv")
