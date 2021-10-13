# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------


def cf_connectedmachine_cl(cli_ctx, *_):
    from azure.cli.core.commands.client_factory import get_mgmt_service_client
    from azext_ssh.vendored_sdks.connectedmachine import ConnectedMachine
    return get_mgmt_service_client(cli_ctx,
                                   ConnectedMachine)


def cf_machine(cli_ctx, *_):
    return cf_connectedmachine_cl(cli_ctx).machines


def cf_machine_extension(cli_ctx, *_):
    return cf_connectedmachine_cl(cli_ctx).machine_extensions


def cf_private_link_scope(cli_ctx, *_):
    return cf_connectedmachine_cl(cli_ctx).private_link_scopes


def cf_private_link_resource(cli_ctx, *_):
    return cf_connectedmachine_cl(cli_ctx).private_link_resources


def cf_private_endpoint_connection(cli_ctx, *_):
    return cf_connectedmachine_cl(cli_ctx).private_endpoint_connections