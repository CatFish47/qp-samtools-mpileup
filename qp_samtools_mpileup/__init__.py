# -----------------------------------------------------------------------------
# Copyright (c) 2020, Qiita development team.
#
# Distributed under the terms of the BSD 3-clause License License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from qiita_client import QiitaPlugin, QiitaCommand
from .qp_samtools_mpileup import get_ref, samtools_mpileup
from .utils import plugin_details
from os.path import splitext


THREADS = 15


# Initialize the plugin
plugin = QiitaPlugin(**plugin_details)

# Define the command
ref = get_ref()
ref_without_extension = splitext(ref)[0]
dbs_defaults = ', '.join([f'"{x}"' for x in dbs_without_extension])
req_params = {'input': ('artifact', ['per_sample_FASTQ'])}
opt_params = {
    'reference': [
        f'choice:["None", {dbs_defaults}]', dbs_without_extension[0]],
    'threads': ['integer', f'{THREADS}']}

outputs = {'Filtered files': 'per_sample_FASTQ'}
default_params = {
    'auto-detect adapters only filtering [not recommended]': {
        'reference': "None", 'threads': THREADS}}
for db in dbs_without_extension:
    name = f'auto-detect adapters and {db} + phix filtering'
    default_params[name] = {'reference': db, 'threads': THREADS}

samtools_pileup_cmd = QiitaCommand(
    'Samtools pileup', "Pileup using samtools",
    samtools_pileup, req_params, opt_params, outputs, default_params)

plugin.register_command(samtools_pileup_cmd)
