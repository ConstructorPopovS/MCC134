
from __future__ import print_function
from time import sleep
from sys import stdout
from daqhats import mcc134, HatIDs, HatError, TcTypes
from daqhats_utils import select_hat_device, tc_type_to_string
import csv #for saving data in fil in csv format
import time #for creating timer during experiment

# Constants
CURSOR_BACK_2 = '\x1b[2D'
ERASE_TO_END_OF_LINE = '\x1b[0K'


def main():
    tc_type = TcTypes.TYPE_K   # change this to the desired thermocouple type
    delay_between_reads = 0.1  # Seconds
    channels = (0, 1, 2, 3)
    

    # open the file in the write mode
    dataFile = open('file_From_Python.txt', 'w')

    # create the csv writer
    writer = csv.writer(dataFile)


    try:
        # Get an instance of the selected hat device object.
        address = select_hat_device(HatIDs.MCC_134)
        hat = mcc134(address)

        for channel in channels:
            hat.tc_type_write(channel, tc_type)
        
        # Display the header row for the data table.
        dataHeader = "   Sample,   "
        dataHeader += " Time,      "
        # print('\n  Sample', end='')
        for channel in channels:
            # print('     Channel', channel, end='')
            dataHeader += " Channel" + str(channel) + ","
            
        print(dataHeader)
        dataFile.write(dataHeader + '\n')

        samples_per_channel = 0
        startTime = float(0.0)
        
        while (samples_per_channel <= 100):
            dataRow = []
            dataRow.append(samples_per_channel)
            # Display the updated samples per channel count
            print('\r{:6d}'.format(samples_per_channel), end='')

            if samples_per_channel == 0:
                startTime = time.perf_counter()
            
            sampleTime = time.perf_counter()
            sampleTimeFromStart = sampleTime - startTime
            dataRow.append(sampleTimeFromStart)
            print('{:12.2f} s'.format(sampleTimeFromStart), end='')


            # Read a single value from each selected channel.
            for channel in channels:
                value = hat.t_in_read(channel)

                # dataRow.append(value)
                if value == mcc134.OPEN_TC_VALUE:
                    print('   Open    ', end='')
                    dataRow.append('Open')
                elif value == mcc134.OVERRANGE_TC_VALUE:
                    print(' OverRange ', end='')
                    dataRow.append('OverRange')
                elif value == mcc134.COMMON_MODE_TC_VALUE:
                    print('Common Mode', end='')
                    dataRow.append('CommonMode')
                else:
                    print('{:12.2f} C'.format(value), end='')
                    strValue = str(value)
                    dataRow.append(strValue)

            writer.writerow(dataRow)
            samples_per_channel += 1
            # stdout.flush()
            # Wait the specified interval between reads.
            sleep(delay_between_reads)
        print('\n')
        dataFile.close()
        

    except (HatError, ValueError) as error:
        print('\n', error)


if __name__ == '__main__':
    # This will only be run when the module is called directly.
    main()
