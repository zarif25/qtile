from datetime import datetime
from libqtile import bar, layout, widget, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

# from libqtile.utils import guess_terminal
import os
import subprocess
from libqtile import hook


PRIMARY_COLOR = "#6790eb"
PRIMARY_FONT = "CaskaydiaCove Nerd Font"
PRIMARY_ARABIC_FONT = "DejaVu Sans Mono Bold"
MATERIAL_COLORS = {
    # "purple": "#ff5370",
    "red": "#f07178",
    # "orange": "#f78c6c",
    "cyan": "#89ddff",
    "green": "#c3e88d",
    "yellow": "#ffcb6b",
    "erie black": "#212121",
}

mod = "mod4"
left_alt = "mod1"
terminal = "alacritty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # custom keys
    Key([mod], "b", lazy.spawn("firefox"), desc="Opens Firefox"),
    Key([mod], "t", lazy.spawn("org.telegram.desktop"), desc="Opens Telegram"),
    Key([mod], "e", lazy.spawn("alacritty --command ranger"), desc="Opens Ranger"),
    Key([mod, "shift"], "x", lazy.spawn("systemctl poweroff"), desc="Shutdown"),
    # Change the volume if your keyboard has special volume keys.
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q sset Master 5%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q sset Master 5%-")),
    Key([], "XF86AudioMute", lazy.spawn("amixer -q sset Master toggle")),
    # screenshot
    Key(
        [mod, "shift"],
        "s",
        lazy.spawn(
            "scrot --line style=dash,width=3 --select=blur --freeze /home/seven89/Pictures/Screenshots/ --exec 'xclip -selection clipboard -t \"image/png\" < $f'"
        ),
    ),
    # dmenu
    Key(
        [mod],
        "Return",
        lazy.run_extension(
            extension.DmenuRun(
                fontsize=13,
                dmenu_prompt="$",
                background="#000000",
                foreground=PRIMARY_COLOR,
                selected_foreground=MATERIAL_COLORS["erie black"],
                selected_background=PRIMARY_COLOR,
            )
        ),
    ),
    # toggle full screen
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, left_alt], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, left_alt], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, left_alt], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, left_alt], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    # Key(
    #     [mod, "shift"],
    #     "Return",
    #     lazy.layout.toggle_split(),
    #     desc="Toggle between split and unsplit sides of stack",
    # ),
    Key([mod, "shift"], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

groups = [Group(i, label=j) for i, j in zip("123456789", "١٢٣٤٥٦٧٨٩")]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(
        border_focus_stack=PRIMARY_COLOR, border_focus=PRIMARY_COLOR, border_width=2
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font=PRIMARY_FONT,
    fontsize=15,
    padding=7,
)
extension_defaults = widget_defaults.copy()


def get_watson_status():
    w_stat = subprocess.check_output(["watson", "status"])
    message = w_stat.decode("utf-8").replace("\n", "")
    if message.startswith("Project "):
        return (
            message[8:-17]
            .replace(" started ", "|")
            .replace(" ago", "")
            .replace(" seconds", "s")
            .replace(" minutes", "min")
            .replace(" [", "|")
            .replace("]", "")
        )
    return ""


screens = [
    Screen(
        top=bar.Bar(
            [
                # widget.CurrentLayoutIcon(scale=0.5),
                # widget.TextBox(
                #     text="",
                #     foreground="#000000",
                #     background=PRIMARY_COLOR,
                #     # padding=0,
                # ),
                widget.GenPollText(
                    func=get_watson_status,
                    update_interval=2,
                    foreground="#000000",
                    background=MATERIAL_COLORS["cyan"],
                ),
                widget.Prompt(
                    font=PRIMARY_FONT,
                    background=MATERIAL_COLORS["cyan"],
                    foreground="#000000",
                    cursor_color="#000000",
                    prompt="$",
                ),
                widget.WindowName(
                    font=PRIMARY_FONT,
                    foreground=PRIMARY_COLOR,
                    empty_group_string="You will have plenty of time to rice qtile after admission",
                ),
                widget.Systray(icon_size=15),
                widget.Spacer(length=10),
                widget.TextBox(text="BRAC:", foreground=PRIMARY_COLOR),
                widget.Countdown(
                    date=datetime(2022, 7, 22),
                    format="{D}d ",
                    update_interval=60,
                    padding=0,
                ),
                widget.TextBox(text="SUST:", foreground=PRIMARY_COLOR),
                widget.Countdown(
                    date=datetime(2022, 7, 30),
                    format="{D}d ",
                    update_interval=60,
                    padding=0,
                ),
                widget.TextBox(text="JU:", foreground=PRIMARY_COLOR),
                widget.Countdown(
                    date=datetime(2022, 8, 1),
                    format="{D}d ",
                    update_interval=60,
                    padding=0,
                ),
                widget.TextBox(text="KUET:", foreground=PRIMARY_COLOR),
                widget.Countdown(
                    date=datetime(2022, 8, 6),
                    format="{D}d ",
                    update_interval=60,
                    padding=0,
                ),
                widget.TextBox(text="NSU:", foreground=PRIMARY_COLOR),
                widget.Countdown(
                    date=datetime(2022, 8, 13),
                    format="{D}d ",
                    update_interval=60,
                    padding=0,
                ),
                widget.GroupBox(
                    highlight_method="block",
                    this_current_screen_border=PRIMARY_COLOR,
                    this_screen_border=PRIMARY_COLOR,
                    rounded=False,
                    margin=0,
                    borderwidth=0,
                    padding=7,
                    disable_drag=True,
                    background=MATERIAL_COLORS["erie black"],
                    foreground=PRIMARY_COLOR,
                    inactive="#ffffff",
                    # fontsize=15,
                ),
                # widget.Chord(
                #     chords_colors={
                #         "launch": ("#ff0000", "#ffffff"),
                #     },
                #     name_transform=lambda name: name.upper(),
                # ),
                # widget.TextBox("default config", name="default"),q
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # widget.TextBox(
                #     text="墳",
                #     font=PRIMARY_FONT,
                #     background=MATERIAL_COLORS["yellow"],
                #     foreground="#000000",
                # ),
                widget.Volume(
                    font=PRIMARY_FONT,
                    background=MATERIAL_COLORS["yellow"],
                    foreground="#000000",
                    fmt="墳 {}",
                ),
                widget.Clock(
                    format="%a %d %b %I:%M %p",
                    font=PRIMARY_FONT,
                    background=MATERIAL_COLORS["green"],
                    foreground="#000000",
                ),
                widget.TextBox(
                    text="",
                    foreground="#000000",
                    background=PRIMARY_COLOR,
                ),
                widget.Battery(
                    battery=0,
                    format="{percent:2.0%}",
                    foreground="#000000",
                    background=PRIMARY_COLOR,
                    padding=0,
                ),
                widget.Battery(
                    battery=1,
                    format="{percent:2.0%}",
                    foreground="#000000",
                    background=PRIMARY_COLOR,
                ),
                widget.QuickExit(
                    default_text="﫼",
                    countdown_format="{}",
                    font=PRIMARY_FONT,
                    background=MATERIAL_COLORS["red"],
                    foreground="#000000",
                    countdown_start=1,
                ),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw bottom and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            background="#0a0a0a",
        ),
        wallpaper="~/.config/qtile/wall.png",
        wallpaper_mode="fill",
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/scripts/autostart.sh"])
