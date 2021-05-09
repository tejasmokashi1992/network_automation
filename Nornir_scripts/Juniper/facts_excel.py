#!/usr/bin/python3
# Forked from Forked from Daniel Teycheney/writememe

# This is the way of initializing nornir.
from nornir import InitNornir
# Import netmiko plugin to send commands to device using SSH.
from nornir_netmiko.tasks import netmiko_send_command
# This module helps print nornir output in a decorative & readable manner.
from nornir_utils.plugins.functions import print_result
# This module uses F object to do advanced filtering of hosts.
from nornir.core.filter import F
# Import Json module to work on json data.
import json
# Import datetime module.
import datetime as dt
# Import module to work on excel sheet.
import openpyxl

def get_facts(task):
    # send show version command to get data in json format.
    task.run(task=netmiko_send_command, command_string="show version | display json | no-more")
    # send show virtual chassis command to get data in json format.
    task.run(task=netmiko_send_command, command_string="show virtual-chassis | display json | no-more")
    # Create a manual/static dictonary & put all required facts as key value pairs.
    facts_dict = {"site":"NJR3",
            "rack":task.host.data['rack_num'],
            "ip":task.host.hostname,
            "device_type":task.host.data['role'],
            "vendor":"Juniper"}
    # return the facts dictonary so that it is captured in output of the function.
    return facts_dict

def main_collector(wb):
    """
    The following block of code creates the various spreadsheet tabs, assign headers to those
    spreadsheets and inserts those headers at the top of that spreadsheet.
    """
    #--------------------------------------------------------------------------
    # Create facts worksheet
    facts_ws = wb.create_sheet("Facts")
    # Statically assign headers
    facts_headers = [
        "Site",
        "Rack",
        "Hostname",
        "IP",
        "Type",
        "Make",
        "Model",
        "Serial Number",
        "OS Version",
    ]
    # Write headers on the top line of the file
    facts_ws.append(facts_headers)
    #--------------------------------------------------------------------------

    # Initialize Nornir and define the inventory variables.
    """
    The following block of code assigns a filter based on
    platform to a variable. This variable is used later on
    to apply logic in for loops
    """
    nr = InitNornir(config_file="config.yaml")
    junos_devices = nr.filter(platform="junos")

    junos_get_facts = junos_devices.run(name="Processing device facts", task=get_facts)
    #--------------------------------------------------------------------------

    # For loop to process individual results inside junos_get_facts.
    for host, task_results in junos_get_facts.items():
        # junos_get_facts has 3 results. 1) facts_dict, 2) show version output, 3) show virtual chassis output.
        # This is facts_dict 
        get_basic_result = task_results[0].result
        # This is show version dict.
        get_version_result = json.loads(task_results[1].result)
        # This is show virtual chassis dict.
        get_ser_num_result = json.loads(task_results[2].result)

        # Extract required variable from the get_basic_result dict.
        site = get_basic_result['site']
        rack = get_basic_result['rack']
        ip = get_basic_result['ip']
        device_type = get_basic_result['device_type']
        vendor = get_basic_result['vendor']
        # Extract required variable from the get_version_result dict.
        hostname = get_version_result["multi-routing-engine-results"][0]["multi-routing-engine-item"][0]["software-information"][0]["host-name"][0]["data"]
        model = get_version_result["multi-routing-engine-results"][0]["multi-routing-engine-item"][0]["software-information"][0]["product-model"][0]["data"]
        os_version = get_version_result["multi-routing-engine-results"][0]["multi-routing-engine-item"][0]["software-information"][0]["junos-version"][0]["data"]

        # Find how many memers under virtual chassis.
        no_of_members = len(get_ser_num_result["virtual-chassis-information"][0]["member-list"][0]["member"])
        # Find fpc0 & fpc1 serial number & put them in single variable.
        if no_of_members == 2:
           ser_num_fpc0 = get_ser_num_result["virtual-chassis-information"][0]["member-list"][0]["member"][0]["fpc-slot"][0]["data"]+get_ser_num_result["virtual-chassis-information"][0]["member-list"][0]["member"][0]["member-serial-number"][0]["data"]
           ser_num_fpc1 = get_ser_num_result["virtual-chassis-information"][0]["member-list"][0]["member"][1]["fpc-slot"][0]["data"]+get_ser_num_result["virtual-chassis-information"][0]["member-list"][0]["member"][1]["member-serial-number"][0]["data"]
           ser_num = ser_num_fpc0 + "\n" + ser_num_fpc1
        else:
           ser_num = get_ser_num_result["virtual-chassis-information"][0]["member-list"][0]["member"][0]["fpc-slot"][0]["data"]+get_ser_num_result["virtual-chassis-information"][0]["member-list"][0]["member"][0]["member-serial-number"][0]["data"]
        # Put all the above variables in list called line. This line is to be added to excel.
        line = [
                site,
                rack,
                hostname,
                ip,
                device_type,
                vendor,
                model,
                ser_num,
                os_version,
        ]
        # Debug print
        # print(line)
        # Write values to file
        facts_ws.append(line)

def create_workbook():
    """
    This function creates an Excel workbook which is then passed to the main
    function 'main_collector' to retrieve and store results into an Excel
    workbook.
    """
    # Capture time
    cur_time = dt.datetime.now()
    # Cleanup time, so that the format is clean for the output file 2019-07-01-13-04-59
    fmt_time = cur_time.strftime("%Y-%m-%d-%H-%M-%S")
    # Setup workbook parameters
    wb = openpyxl.Workbook()
    # Execute program
    main_collector(wb)
    # Assign customer name to Excel file
    dc_name = "NJR3"
    # String together workbook name i.e. customer-2019-01-01-13-00-00.xlsx
    wb_name = "Collection-" + dc_name + "-" + fmt_time + ".xlsx"
    # Print workbook name
    print(
        "COLLECTION COMPLETE \n" + "Results located in Excel workbook: " + str(wb_name)
    )
    # Remove default created which is made using Openpyxl
    wb.remove(wb["Sheet"])
    # Save workbook
    wb.save(wb_name)

# Execute main function
create_workbook()
