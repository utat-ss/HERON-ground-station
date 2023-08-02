"""
automate.py

Establishes the command schedule for the satellite, and sends the appropriate commands through
the flowgraph pipeline.

Author(s): Adyn Miles
"""

from schedule import Scheduler
import argparse
from datetime import datetime
from propagate import Propagator
from tx_wrapper import TX_Command
from rx_wrapper import RX_Command
import smtplib
import constants as const

def parse_config():
    """
    Sets up configurability of start time for launch and TLE.

    Returns:
        parser.parse_args(): contains all configuration arguments.
    """

    parser = argparse.ArgumentParser()

    ### State Vector Values
    parser.add_argument("--epoch_time", type=float, default=22300.000000000, help="Epoch time defined as YYDDD.DDDDDDDDD")
    parser.add_argument("--inclination", type=float, default=51.6460, help="Inclination (deg)")
    parser.add_argument("--right_ascension", type=float, default=269.3699, help="Right ascension of the ascending node (deg)")
    parser.add_argument("--eccentricity", type=float, default=0.001910, help="Eccentricity of the orbit")
    parser.add_argument("--perigee", type=float, default=75.3707, help="Argument of perigee in degrees")
    parser.add_argument("--mean_anomaly", type=float, default=348.7711, help="Mean anomaly in degrees")
    parser.add_argument("--mean_motion", type=float, default=15.49065788, help="Mean motion (revolutions per day)")

    ### SatNOGS Interface Information
    parser.add_argument("--satellite_id", type=int, default=5622043, help='Input the SatNOGS satellite ID (integer value)')

    ### File Path Information
    parser.add_argument("--tx_log_path", type=str, default='logging/tx/', help="Input the path of the output path for TX logs. Note this path will be appended with the current date and time monthly.")
    parser.add_argument("--rx_log_path", type=str, default='logging/rx/', help="Input the path of the output path for RX logs. Note this path will be appended with the current date and time monthly.")
    parser.add_argument("--command_path", type=str, default='commands/cmdout.bin', help='path to command file that stores commands for TX flowgraph in binary.')

    return parser.parse_args()



def send_error_email(send, receive, message):
  server = smtplib.SMTP(const.HOST)
  msg = "Subject: Test email python\n\n{}".format(message)
  server.sendmail(send, receive, msg)
  server.quit()
  print("Error email now sent to ss-operations@utat.ca")


def main():
    schedule = Scheduler(['Contact', 'Erase', 'DataDisable', 'RTC', 'DisablePayload', 'DataCollection', 'MissionComplete'])
    cfg = parse_config()
    c_state = schedule.Contact
    # test call to obtain satellite info from SatNOGS API
    ack = False
    while True:
        if (c_state == schedule.Contact):
            print("Attempting contact");
            # First, need to check orbit propagator for estimated pass times (with tolerances based
            # on the predicted accuracy of the orbit propagator tool)
            current_time = schedule.curr_time()
            satellite_request = Propagator(str(cfg.satellite_id))
            valid_pass = satellite_request.get_pass_times()
            satellite_info = satellite_request.get_satellite_info()
            print(satellite_info)
            for pass_num, time in enumerate(valid_pass):
                valid_pass[pass_num] = schedule.epoch_time(time)
            if current_time in valid_pass or True:
                tx = TX_Command(cfg.command_path, cfg.tx_log_path)
                # Create an easy method of calling the correct op code for the outgoing command.
                try:
                    tx.command('0x00')
                except ValueError:
                    send_error_email(const.SENDER, const.RECEIVER, "The command with id {} is not valid. Please try again.".format('0x00'))
                rx = RX_Command(cfg.command_path, cfg.rx_log_path)
                ack = rx.receive()
                if ack == True:
                    c_state = schedule.Erase
                    ack = False
        elif (c_state == schedule.Erase):
            print("Erase the payload data.")
            satellite_request = Propagator(str(cfg.satellite_id))
            valid_pass = satellite_request.get_pass_times()
            for pass_num, time in enumerate(valid_pass):
                valid_pass[pass_num] = schedule.epoch_time(time)
            current_time = schedule.curr_time()
            if current_time in valid_pass or True:
                tx = TX_Command(cfg.command_path, cfg.tx_log_path)
                try:
                    tx.command('0x37', pwd=["0x55", "0x54", "0x55"])
                except ValueError:
                    send_error_email(const.SENDER, const.RECEIVER, "The command with id {} is not valid. Please try again.".format('0x37'))
                rx = RX_Command(cfg.command_path, cfg.rx_log_path)
                ack = rx.receive()
                if ack == True:
                    c_state = schedule.DataDisable
                    ack = False
        elif (c_state == schedule.DataDisable):
            print("Disable automatic data collection from the payload.")
            satellite_request = Propagator(str(cfg.satellite_id))
            valid_pass = satellite_request.get_pass_times()
            for pass_num, time in enumerate(valid_pass):
                valid_pass[pass_num] = schedule.epoch_time(time)
            current_time = schedule.curr_time()
            if current_time in valid_pass or True:
                tx = TX_Command(cfg.command_path, cfg.tx_log_path)
                try: 
                    tx.command('0x22', args=[False, 0x00])
                except ValueError:
                    send_error_email(const.SENDER, const.RECEIVER, "The command with id {} is not valid. Please try again.".format('0x22'))
                rx = RX_Command(cfg.command_path, cfg.rx_log_path)
                ack = rx.receive()
                if ack == True:
                    c_state = schedule.RTC
                    ack = False
        elif (c_state == schedule.RTC):
            print("Updating the RTC")
            satellite_request = Propagator(str(cfg.satellite_id))
            valid_pass = satellite_request.get_pass_times()
            for pass_num, time in enumerate(valid_pass):
                valid_pass[pass_num] = schedule.epoch_time(time)
            current_time = schedule.curr_time()
            if current_time in valid_pass or True:
                tx = TX_Command(cfg.command_path, cfg.tx_log_path)
                try: 
                    tx.command('0x02', args=[datetime.now().strftime("%d/%m/%Y"), datetime.now().strftime("%H:%M:%S")])
                except ValueError:
                    send_error_email(const.SENDER, const.RECEIVER, "The command with id {} is not valid. Please try again.".format('0x02'))
                rx = RX_Command(cfg.command_path, cfg.rx_log_path)
                ack = rx.receive()
                if ack == True:
                    c_state = schedule.DisablePayload
                    ack = False 
        elif (c_state == schedule.DisablePayload):
            print("Disabling Payload")
            satellite_request = Propagator(str(cfg.satellite_id))
            valid_pass = satellite_request.get_pass_times()
            for pass_num, time in enumerate(valid_pass):
                valid_pass[pass_num] = schedule.epoch_time(time)
            current_time = schedule.curr_time()
            if current_time in valid_pass or True:
                tx = TX_Command(cfg.command_path, cfg.tx_log_path)
                try:
                    tx.command('0x41', args=[False, "0x00000605"])
                except ValueError:
                    send_error_email(const.SENDER, const.RECEIVER, "The command with id {} is not valid. Please try again.".format('0x20'))
                rx = RX_Command(cfg.command_path, cfg.rx_log_path)
                ack = rx.receive()
                if ack:
                    therms_invalid = True
                    ack = False
                tx = TX_Command(cfg.command_path, cfg.tx_log_path)
                try:
                    tx.command('0x41', args=["0x00000003", "0x00002005"])
                except ValueError:
                    send_error_email(const.SENDER, const.RECEIVER, "The command with id {} is not valid. Please try again.".format('0x41'))
                rx = RX_Command(cfg.command_path, cfg.rx_log_path)
                ack = rx.receive()
                if ack:
                    pay_opt_asleep = True
                    ack = False
                tx = TX_Command(cfg.command_path, cfg.tx_log_path)
                try:
                    tx.command('0x41', args=[False, "0x00000705"])
                except ValueError:
                    send_error_email(const.SENDER, const.RECEIVER, "The command with id {} is not valid. Please try again.".format('0x41'))
                rx = RX_Command(cfg.command_path, cfg.rx_log_path)
                ack = rx.receive()
                if ack:
                    disable_6v = True
                    ack = False
                if (therms_invalid) and (pay_opt_asleep) and (disable_6v):
                    c_state = schedule.DataCollection
                    ack = False
                    data_start_time = datetime.now()
        elif (c_state == schedule.DataCollection):
            if (datetime.now() - data_start_time).days >= 60:
                c_state = schedule.MissionComplete
            else:
                satellite_request = Propagator(str(cfg.satellite_id))
                valid_pass = satellite_request.get_pass_times()
                for pass_num, time in enumerate(valid_pass):
                    valid_pass[pass_num] = schedule.epoch_time(time)
                current_time = schedule.curr_time()
                if current_time in valid_pass or True:
                    tx = TX_Command(cfg.command_path, cfg.tx_log_path)
                    try:
                        tx.command('0x20', args = ['0x00', '0x00'])
                    except ValueError:
                        send_error_email(const.SENDER, const.RECEIVER, "The command with id {} is not valid. Please try again.".format('0x20'))
                    rx = RX_Command(cfg.command_path, cfg.rx_log_path)
                    ack = rx.receive()

            print("Collecting Data")
        elif (c_state == schedule.MissionComplete):
            print("Mission Complete")
        else:
            # Reached an error state, report to operations email
            print("Reached an unknown, error state...")
            send_error_email(const.SENDER, const.RECEIVER, "The main state machine has reached an unknown error state")


if __name__ == "__main__":
    main()