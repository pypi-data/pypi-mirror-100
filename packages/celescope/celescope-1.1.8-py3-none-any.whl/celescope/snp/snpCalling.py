import os
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
import celescope
import pysam
import numpy as np
import pandas as pd
import logging
from celescope.tools.utils import *
from celescope.tools.report import reporter
from mutract.utils import Mutract


@add_log
def snpCalling(args):

    sample = args.sample
    outdir = args.outdir
    thread = int(args.thread)
    match_dir = args.match_dir
    bam = args.bam
    genomeDir = args.genomeDir
    gene_list_file = args.gene_list

    # check dir
    if not os.path.exists(outdir):
        os.system('mkdir -p %s' % (outdir))

    # get args
    _refFlat, _gtf, fasta = glob_genomeDir(genomeDir, fa=True)
    _match_barcode, _cell_total, match_barcode_file = read_barcode_file(match_dir, return_file=True)

    # mutract
    obj = Mutract(
        outdir, sample, bam, fasta, 
        match_barcode_file, thread=thread, gene_file=gene_list_file
    )
    obj.run()


def get_opts_snpCalling(parser, sub_program):
    if sub_program:
        s_common(parser)
        parser.add_argument("--bam", help='featureCounts bam', required=True)
    parser.add_argument("--genomeDir", help='genomeDir', required=True)
    parser.add_argument(
        "--match_dir", help="match scRNA-Seq dir", required=True)
    parser.add_argument("--gene_list", help='gene_list', required=True)
