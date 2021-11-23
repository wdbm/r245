#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# R2-45                                                                        #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program monitors volatile memory usage and progressively kills          #
# blocklisted programs with the goal of avoiding overuse of available          #
# resources. As it acts it notifies you of its actions. It knows that it is    #
# not perfect, but it is trying.                                               #
#                                                                              #
# copyright (C) 2018 Will Breaden Madden, wbm@protonmail.ch,                   #
#                    Gavin Kirby        , clean_air_turbulence@protonmail.com  #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

usage:
    program [options]

options:
    -h, --help          display help message
    --version           display version and exit
    --limit=INT         critical RAM limit
                        [default: 96]
    --rate=FLOAT        rate at which program checks running processes (seconds)
                        [default: 0.25]
    --blocklist=STRING  comma-separated list of blocklisted programs
                        [default: transmission-gtk,ebook-convert,pdftoppm,convert,chromium,firefox,Popcorn-Time,riot-web,signal-desktop,python,thunderbird,evince,nautilus]
"""

import docopt
import os
import shutil
import subprocess
import time

import psutil

name        = "R2-45"
__version__ = "2021-11-23T1048Z"

def main():
    options = docopt.docopt(__doc__, version = __version__)
    critical_RAM_used = int(options["--limit"])
    check_frequency   = float(options["--rate"])
    blocklist         = options["--blocklist"].split(",")
    RAM_usage_critical_final_message_sent = False
    print("\nwatching memory usage and ready to kill progressively the following blocklist of programs if RAM usage >= {critical_RAM_used} %:\n\n{blocklist}\n".format(critical_RAM_used=critical_RAM_used, blocklist=", ".join(blocklist)))
    while True:
        total_RAM_used = psutil.virtual_memory().percent
        if total_RAM_used >= critical_RAM_used:
            processes                       = [process for process in psutil.process_iter()]
            processes_by_memory             = sorted(processes, key=lambda process: process.memory_percent(), reverse=True)
            blocklisted_processes_by_memory = [process for process in processes_by_memory if process.name() in blocklist]
            if blocklisted_processes_by_memory:
                process_name = blocklisted_processes_by_memory[0].name()
                blocklisted_processes_by_memory[0].kill()
                message = "RAM usage critical => killed blocklisted process \"{process_name}\"".format(process_name=process_name)
                print(message); notify(text=message)
            else:
                if not RAM_usage_critical_final_message_sent:
                    message = "RAM usage critical!"
                    print(message); notify(text=message)
                    RAM_usage_critical_final_message_sent = True
        else:
            RAM_usage_critical_final_message_sent = False
        time.sleep(check_frequency)

def notify(
    text    = None,
    subtext = None,
    icon    = None
    ):
    try:
        if text and shutil.which("notify-send"):
            command = "notify-send \"{text}\""
            if subtext:
                command = command + " \"{subtext}\""
            if icon and os.path.isfile(os.path.expandvars(icon)):
                command = command + " --icon={icon}"
            command = command + " --urgency=critical"
            command = command.format(
                text    = text,
                subtext = subtext,
                icon    = icon
            )
            engage_command(command)
    except:
        pass

def engage_command(
    command    = None,
    background = True,
    timeout    = None
    ):
    if background:
        subprocess.Popen(
            [command],
            shell      = True,
            executable = "/bin/bash"
        )
        return None
    elif not background:
        process = subprocess.Popen(
            [command],
            shell      = True,
            executable = "/bin/bash",
            stdout     = subprocess.PIPE
        )
        try:
            process.wait(timeout=timeout)
            output, errors = process.communicate(timeout=timeout)
            return output
        except:
            process.kill()
            return False
    else:
        return None

if __name__ == "__main__":
    main()
