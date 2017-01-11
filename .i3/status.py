# -*- coding: utf-8 -*-

import platform

from i3pystatus import Status
from i3pystatus.core.command import run_through_shell
from i3pystatus.weather import weathercom
import netifaces

colors = {
    "blue": "#81a2be",
    "bright": "#ffffff",
    "brown": "#a3685a",
    "dark": "#282a2e",
    "green": "#b5bd68",
    "orange": "#de935f",
    "red": "#cc6666",
    "teal": "#8abeb7",
    "violet": "#b294bb",
    "yellow": "#f0c674",
}
thermal_zones = {
    'loki': '/sys/class/thermal/thermal_zone2/temp',
}
audio_sources = [
    ("Revo", "alsa_input.usb-0b0e_Jabra_REVO_v4.0.0_1C48F9008D3F040000-00.analog-mono"),
]

node_name = platform.node()

status = Status(
    logfile='/home/laeroth/i3pystatus.log',
    standalone=True,
)

status.register("clock",
    format=" %Y-%m-%d %H:%M:%S",
    color=colors["bright"],
    )

for (source_label, source_name) in audio_sources:
    status.register("shell",
        command="""pacmd dump | grep -c "set-source-mute {source_name} no" """.format(source_name=source_name),
        on_leftclick="pacmd set-source-mute {source_name} true".format(source_name=source_name),
        on_rightclick="pacmd set-source-mute {source_name} false".format(source_name=source_name),
        interval=10,
        color=colors["bright"],
        error_color=colors["red"],
        format="{source_label}".format(source_label=source_label),
        )


status.register("weather",
    format="{icon} {current_temp}{temp_unit} ({low_temp}{temp_unit}, {high_temp}{temp_unit})",
    colorize=True,
    backend=weathercom.Weathercom(
        location_code="GMXX0007",
        ),
    )

status.register("battery",
    format=" {percentage:.0f}% {status} {remaining}",
    alert=True,
    color=colors["blue"],
    full_color=colors["green"],
    charging_color=colors["blue"],
    critical_color=colors["red"],
    )

status.register("uptime",
    format=" {uptime}",
    color=colors["teal"],
    )

status.register("dpms",
    format=" {status}",
    color=colors["bright"],
    color_disabled=colors["orange"],
    )

status.register("backlight",
    format=" {percentage}%",
    color=colors["bright"],
    backlight="intel_backlight",
    )

status.register("shell",
    command="""echo " $(gpg-connect-agent 'keyinfo --list' '/bye' | grep -e '^S KEYINFO .* 1 P ' -c)" """,
    on_leftclick=lambda mod: run_through_shell(["killall", "-s", "HUP", "gpg-agent"]),
    interval=10,
    color=colors["bright"],
    )

default_family = netifaces.AF_INET
default_gateways = netifaces.gateways().get("default", {})
if default_family in default_gateways:
    default_interface = default_gateways[default_family][1]
else:
    default_interface = "lo"

status.register("network",
    format_up=" {interface} {essid} {kbs}KB/s",
    format_down=" {interface}",
    start_color=colors["green"],
    end_color=colors["red"],
    color_up=colors["green"],
    color_down=colors["red"],
    interface=default_interface,
    )

status.register("temp",
    format=" {temp}°C ",
    file=thermal_zones.get(node_name, '/sys/class/thermal/thermal_zone0/temp'),
    color=colors["green"],
    alert_color=colors["red"],
    alert_temp=85,
    )

status.register("cpu_usage_graph",
    graph_width=10,
    start_color=colors["green"],
    end_color=colors["red"],
    )

status.register("cpu_usage",
    format=" {usage_all}",
    format_all="{usage:02}%",
    exclude_average=True,
    )

status.register("mem",
    format=" {percent_used_mem:0}% ({used_mem:0} MiB)",
    color=colors["green"],
    warn_color=colors["yellow"],
    alert_color=colors["red"],
    )


status.run()
