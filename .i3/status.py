# -*- coding: utf-8 -*-

import platform

from i3pystatus import Status
from i3pystatus.core.command import run_through_shell
from i3pystatus.weather import weathercom
# import netifaces

colors = {
    "blue": "#81a2be",
    "bright": "#d8d8d8",
    "brown": "#a3685a",
    "dark": "#b8b8b8",
    "green": "#b5bd68",
    "orange": "#de935f",
    "red": "#cc6666",
    "teal": "#8abeb7",
    "violet": "#b294bb",
    "yellow": "#f0c674",
}
default_hints = {
    "align": "center",
    "border": colors["dark"],
    "border_bottom": 1,
    "border_left": 0,
    "border_right": 0,
    "border_top": 0,
    "markup": "pango",
    "separator_block_width": 16,
}
thermal_zones = {
    'loki': '/sys/class/thermal/thermal_zone2/temp',
    'tyr': '/sys/class/thermal/thermal_zone8/temp',
}
cpu_cores = {
    'loki': 4,
    'tyr': 8,
}
network_interface = {
    'tyr': 'wlp2s0',
}
audio_sources = [
    # ("Revo", "alsa_input.usb-0b0e_Jabra_REVO_v4.0.0_1C48F9008D3F040000-00.analog-mono"),
]

def create_hints(**kwargs):
    return {**default_hints, **kwargs}

node_name = platform.node()

status = Status(
    logfile='/home/laeroth/i3pystatus.log',
    standalone=True,
)

status.register("clock",
    color=colors["bright"],
    format=" %Y-%m-%d %H:%M:%S",
    hints=create_hints(),
)

# for (source_label, source_name) in audio_sources:
#     status.register("shell",
#         color=colors["bright"],
#         command="""pacmd dump | grep -c "set-source-mute {source_name} no" """.format(source_name=source_name),
#         error_color=colors["red"],
#         format="{source_label}".format(source_label=source_label),
#         hints=create_hints(),
#         interval=10,
#         on_leftclick="pacmd set-source-mute {source_name} true".format(source_name=source_name),
#         on_rightclick="pacmd set-source-mute {source_name} false".format(source_name=source_name),
#     )


status.register("weather",
    backend=weathercom.Weathercom(
        location_code="GMXX0007",
    ),
    color=colors["blue"],
    colorize=True,
    format="[{icon} ]{current_temp}{temp_unit} ({low_temp}{temp_unit}[, {high_temp}{temp_unit}])",
    hints=create_hints(),
)

status.register("battery",
    format="{status}  {percentage:.0f}%[ {consumption:0.1f}W][ {remaining}h]",
    alert=True,
    color=colors["bright"],
    full_color=colors["bright"],
    charging_color=colors["bright"],
    critical_color=colors["bright"],
    status={
        "FULL": "<span color='{colors[green]}'></span>".format(colors=colors),
        "CHR": "<span color='{colors[blue]}'></span>".format(colors=colors),
        "DIS": "<span color='{colors[yellow]}'></span>".format(colors=colors),
        "DPL": "<span color='{colors[red]}'></span>".format(colors=colors),
    },
    hints=create_hints(),
)

status.register("uptime",
    color=colors["bright"],
    format=" {hours}:{mins:02d}",
    hints=create_hints(),
)

status.register("dpms",
    color=colors["bright"],
    color_disabled=colors["orange"],
    format="",
    format_disabled="",
    hints=create_hints(),
)

# status.register("redshift",
#     colors=colors["bright"],
#     error_color=colors["red"],
#     # format="{inhibit}",
#     format_inhibit=["", ""],
#     hints=create_hints(),
# )

status.register("backlight",
    backlight="intel_backlight",
    color=colors["bright"],
    format=" {percentage}%",
    hints=create_hints(),
)

status.register("pulseaudio",
    color_muted=colors["red"],
    color_unmuted=colors["green"],
    format=" {volume}",
    hints=create_hints(),
    on_leftclick="switch_mute",
    on_rightclick="change_sink",
    on_doubleleftclick="pavucontrol",
)

status.register("shell",
    color=colors["bright"],
    command="""echo " $(gpg-connect-agent 'keyinfo --list' '/bye' | grep -e '^S KEYINFO .* 1 P ' -c)" """,
    hints=create_hints(),
    interval=10,
    on_leftclick=lambda mod: run_through_shell(["killall", "-s", "HUP", "gpg-agent"]),
)

# default_family = netifaces.AF_INET
# default_gateways = netifaces.gateways().get("default", {})
# if default_family in default_gateways:
#     default_interface = default_gateways[default_family][1]
# else:
#     default_interface = "lo"

status.register("network",
    color_down=colors["red"],
    color_up=colors["green"],
    divisor=1024**2,
    end_color=colors["red"],
    format_down=" {interface}",
    format_up=" {interface} {bytes_recv:05.3f}MB/s {bytes_sent:05.3f}MB/s",
    graph_style="braille-snake",
    hints=create_hints(),
    interface=network_interface.get(node_name, 'lo'),
    recv_limit=50*1024,
    round_size=3,
    sent_limit=10*1024,
    start_color=colors["green"],
)

status.register("temp",
    alert_color=colors["red"],
    alert_temp=85,
    color=colors["green"],
    file=thermal_zones.get(node_name, '/sys/class/thermal/thermal_zone0/temp'),
    format=" {temp}°C",
    hints=create_hints(),
)

status.register("cpu_usage_bar",
    bar_type="vertical",
    end_color=colors["red"],
    format=" <tt>" + ("".join([ ("{usage_bar_cpu%d}" % cpu_index) for cpu_index in range(cpu_cores.get(node_name, 1)) ])) + "</tt>",
    hints=create_hints(),
    start_color=colors["green"],
)

status.register("mem",
    alert_color=colors["red"],
    color=colors["green"],
    format=" {avail_mem:5.0f}MB ({percent_used_mem:03.1f}%)",
    hints=create_hints(),
    warn_color=colors["yellow"],
)

# status.register("shell",
#     color=colors["bright"],
#     command="""echo " $(timew get dom.active.tag.1 dom.active.duration || true)" """,
#     hints=create_hints(),
#     interval=10,
#     # on_leftclick=lambda mod: run_through_shell(["killall", "-s", "HUP", "gpg-agent"]),
# )

# status.register("timewarrior",
#     color_running=colors["orange"],
#     color_stopped=colors["dark"],
#     hints=create_hints(),
# )

# status.register("window_title",
#     always_show=True,
#     hints=create_hints(
#         align="left",
#         min_width="m"*79,
#     ),
# )


status.run()
