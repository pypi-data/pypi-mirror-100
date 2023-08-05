import argparse
from .Analysis_tag import Analysis_tag
from celescope.tools.utils import *

def get_opts_analysis_tag(parser, sub_program):
    if sub_program:
        parser = s_common(parser)
        parser.add_argument('--tsne_tag_file', help='tsne tag file', required=True)
        parser.add_argument("--match_dir", help="matched scRNA-Seq CeleScope directory path", required=True)


def analysis_tag(args):

    analysis_tag_object = Analysis_tag(
        args.sample,
        args.outdir,
        args.assay,
        args.match_dir,
        'analysis_tag',
    )
    analysis_tag_object.run(args.tsne_tag_file)