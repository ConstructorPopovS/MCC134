
from __future__ import print_function
from time import sleep
from sys import stdout
from daqhats import mcc134, HatIDs, HatError, TcTypes
from daqhats_utils import select_hat_device, tc_type_to_string
# __import__('daqhats_utils')


# Constants
CURSOR_BACK_2 = '\x1b[2D'
ERASE_TO_END_OF_LINE = '\x1b[0K'


def main():
    tc_type = TcTypes.TYPE_K   # change this to the desired thermocouple type
    delay_between_reads = 1  # Seconds
    channels = (0, 1, 2, 3)

    # Creating a file with fileName#
    dataFile = open('file_From_Python.txt', 'w')

    try:
        # Get an instance of the selected hat device object.
        address = select_hat_device(HatIDs.MCC_134)
        hat = mcc134(address)

        for channel in channels:
            hat.tc_type_write(channel, tc_type)

        # Display the header row for the data table.
        print('\n  Sample', end='')
        dataFile.write('Sample')
        for channel in channels:
            print('     Channel', channel, end='')
            dataFile.write('     Channel')
            dataFile.write(str(channel))
        print('')
        dataFile.write('\n')

        samples_per_channel = 0
        while (samples_per_channel <= 10):
            # Display the updated samples per channel count
            print('\r{:8d}'.format(samples_per_channel), end='')
            dataFile.write(str(samples_per_channel))
            samples_per_channel += 1

            # Read a single value from each selected channel.
            for channel in channels:
                value = hat.t_in_read(channel)
                if value == mcc134.OPEN_TC_VALUE:
                    print('     Open     ', end='')
                elif value == mcc134.OVERRANGE_TC_VALUE:
                    print('     OverRange', end='')
                elif value == mcc134.COMMON_MODE_TC_VALUE:
                    print('   Common Mode', end='')
                else:
                    print('{:12.2f} C'.format(value), end='')

            # stdout.flush()
            # Wait the specified interval between reads.
            sleep(delay_between_reads)
        dataFile.close()
        

    except (HatError, ValueError) as error:
        print('\n', error)


if __name__ == '__main__':
    # This will only be run when the module is called directly.
    main()
