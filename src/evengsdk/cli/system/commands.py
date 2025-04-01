import click

from evengsdk.cli.common import list_sub_command, list_command
from evengsdk.cli.console import cli_print, cli_print_error, cli_print_output, console
from evengsdk.cli.utils import get_client
from evengsdk.exceptions import EvengApiError, EvengHTTPError

client = None


@list_command
@click.command(name="list-node-templates")
@click.pass_context
def templates(ctx, output):
    """
    list EVE-NG node templates

    \b
    Examples:
        eveng list-node-templates
    """
    _client = get_client(ctx)
    try:
        resp = _client.api.list_node_templates()
        if output == "table":
            table_data = []
            style = {"true": "green", "false": "red"}
            for key, value in resp["data"].items():
                template_image_available = "true" if "missing" not in value else "false"
                this_style = style[template_image_available]
                table_data.append(
                    {
                        "name": key,
                        "description": value,
                        "available": f"[{this_style}]{template_image_available}[/{this_style}]",
                    }
                )

            table_header = [
                ("Name", dict(justify="right", style="cyan", no_wrap=True)),
                ("Description", {}),
                ("Available", dict(justify="center")),
            ]
            cli_print_output(
                output,
                {"data": table_data},
                table_header=table_header,
                table_title="Node Templates",
            )
        else:
            cli_print_output("json", resp)
    except (EvengHTTPError, EvengApiError) as err:
        console.print_error(err)


@click.command(name="show-template")
@click.argument("template_name")
@click.pass_context
def read_template(ctx, template_name):
    """
    get EVE-NG node template details

    \b
    Examples:
        eveng show-template veos
    """
    _client = get_client(ctx)
    try:
        resp = _client.api.node_template_detail(template_name)
        if resp:
            del resp["data"]["options"]["icon"]["list"]
        text_header = f"Node Template: {template_name}"
        cli_print_output("json", resp, header=text_header)
    except (EvengHTTPError, EvengApiError) as err:
        console.print_error(err)


@list_command
@click.command(name="list-network-types")
@click.pass_context
def network_types(ctx, output):
    """
    list EVE-NG network types

    \b
    Examples:
        eveng list-network-types
    """
    _client = get_client(ctx)
    try:
        resp = _client.api.list_networks()
        if output == "table":
            table_data = [
                {"name": key, "description": value}
                for key, value in resp["data"].items()
            ]

            table_header = [
                ("Name", dict(justify="right", style="cyan", no_wrap=True)),
                ("Description", {}),
            ]
            cli_print_output(
                output,
                {"data": table_data},
                table_header=table_header,
                table_title="Network Types",
            )
        cli_print_output(output, resp, header="Network Types")
    except (EvengHTTPError, EvengApiError) as err:
        console.print_error(err)


@list_command
@click.command(name="list-user-roles")
@click.pass_context
def user_roles(ctx, output):
    """
    list EVE-NG user roles

    \b
    Examples:
        eveng list-user-roles
    """
    _client = get_client(ctx)
    try:
        resp = _client.api.list_user_roles()
        if output == "table":
            table_data = [
                {"name": key, "description": value}
                for key, value in resp["data"].items()
            ]

            table_header = [
                ("Name", dict(justify="right", style="cyan", no_wrap=True)),
                ("Description", {}),
            ]
            cli_print_output(
                output,
                {"data": table_data},
                table_header=table_header,
                table_title="User Roles",
            )
        cli_print_output("json", resp, header="User Roles")
    except (EvengHTTPError, EvengApiError) as err:
        console.print_error(err)


@list_command
@click.command(name="show-status")
@click.pass_context
def status(ctx, output):
    """View EVE-NG server status

    \b
    Examples:
        eveng show-status
    """
    _client = get_client(ctx)
    try:
        resp = _client.api.get_server_status()
        if output == "table":
            table_data = [
                {"name": key, "value": value} for key, value in resp["data"].items()
            ]

            table_header = [
                ("Name", dict(justify="right", style="cyan", no_wrap=True)),
                ("Value", {}),
            ]
            cli_print_output(
                output,
                {"data": table_data},
                table_header=table_header,
                table_title="Server Status",
            )
        cli_print_output(output, resp, header="System")
    except (EvengHTTPError, EvengApiError) as err:
        console.print_error(err)


@list_command
@click.option("--ad-server-dn", help="Base DN")
@click.option("--ad-server-group", help="EVE-NG Active Directory Group")
@click.option("--ad-server-ip", help="Active Directory Server")
@click.option("--ad-server-port", help="Port", type=int)
@click.option("--ad-server-tls", help="Active Directory TLS", type=int)
@click.option("--caching", help="Caching mode")
@click.option("color-scheme", help="Color scheme")
@click.option("--cpudedicate", default=1, help="CPU Dedicate Mode", type=int)
@click.option("--docker-net", default="172.17", help="Docker Network")
@click.option("--font-name", default="monospace", help="Font Name")
@click.option("--font-size", default=11, help="Font Size", type=int)
@click.option("--ipv6", default=0, help="Enable IPv6", type=int)
@click.option("--lic-check", default="strict", help="License Check Mode")
@click.option("--mindisk", default=20, help="Minimum Disk Size", type=int)
@click.option("--nat-net", default="172.29.129", help="NAT Network")
@click.option("--numa", default=0, help="NUMA Mode", type=int)
@click.option("--proxy-password", default="", help="Proxy Password")
@click.option("--proxy-port", default=0, help="Proxy Port", type=int)
@click.option("--proxy-server", default="0.0.0.0", help="Proxy Server")
@click.option("--proxy-user", default="", help="Proxy Username")
@click.option("--radius-server-ip", default="0.0.0.0", help="RADIUS Server IP")
@click.option("--radius-server-ip_2", default="0.0.0.0", help="RADIUS Server IP 2")
@click.option("--radius-server-port", default=1812, help="RADIUS Server Port", type=int)
@click.option(
    "--radius-server-port_2", default=1812, help="RADIUS Server Port 2", type=int
)
@click.option("--radius-server-secret", default="secret", help="RADIUS Server Secret")
@click.option(
    "--radius-server-secret_2", default="secret", help="RADIUS Server Secret 2"
)
@click.option("--template-disabled", default=".missing", help="Disabled Template")
@click.option("--vpn-net", default="172.29.130", help="VPN Network")
@click.pass_context
def system_settings(
    ctx,
    ad_server_dn,
    ad_server_group,
    ad_server_ip,
    ad_server_port,
    ad_server_tls,
    caching,
    color_scheme,
    cpudedicate,
    docker_net,
    font_name,
    font_size,
    ipv6,
    lic_check,
    mindisk,
    nat_net,
    numa,
    proxy_password,
    proxy_port,
    proxy_server,
    proxy_user,
    radius_server_ip,
    radius_server_ip_2,
    radius_server_port,
    radius_server_port_2,
    radius_server_secret,
    radius_server_secret_2,
    template_disabled,
    vpn_net,
):
    """Edit System Settings
    \b
    Example:
        eve-ng node create --ad_server_dn "dc=com,dc=example" --ad_server_group "EVE Users" --ad_server_ip "0.0.0.0" --ad_server_port 389 --ad_server_tls 0 --caching 0 --color_scheme "black-white" --cpudedicate 1 --docker_net "172.17" --font_name "monospace" --font_size 11 --ipv6 0 --lic_check "strict" --mindisk 20 --nat_net "172.29.129" --numa 0 --proxy_password "" --proxy_port 0 --proxy_server "0.0.0.0" --proxy_user "" --radius_server_ip "0.0.0.0" --radius_server_ip_2 "0.0.0_

    """
    _client = get_client(ctx)
    node = {
        "ad_server_dn": ad_server_dn,
        "ad_server_group": ad_server_group,
        "ad_server_ip": ad_server_ip,
        "ad_server_port": ad_server_port,
        "ad_server_tls": ad_server_tls,
        "caching": caching,
        "color_scheme": color_scheme,
        "cpudedicate": cpudedicate,
        "docker_net": docker_net,
        "font_name": font_name,
        "font_size": font_size,
        "ipv6": ipv6,
        "lic_check": lic_check,
        "mindisk": mindisk,
        "nat_net": nat_net,
        "numa": numa,
        "proxy_password": proxy_password,
        "proxy_port": proxy_port,
        "proxy_server": proxy_server,
        "proxy_user": proxy_user,
        "radius_server_ip": radius_server_ip,
        "radius_server_ip_2": radius_server_ip_2,
        "radius_server_port": radius_server_port,
        "radius_server_port_2": radius_server_port_2,
        "radius_server_secret": radius_server_secret,
        "radius_server_secret_2": radius_server_secret_2,
        "template_disabled": template_disabled,
        "vpn_net": vpn_net,
    }
    try:
        resp = _client.edit_system_settings(node)
        cli_print_output("json", resp, header="Node created")
    except (EvengHTTPError, EvengApiError) as err:
        console.print_error(err)


@click.group()
@click.pass_context
def system(ctx):
    """System sub commands

    Edit System Settings
    """
    global client
    client = ctx.obj.client


# system.add_command(system_settings)
