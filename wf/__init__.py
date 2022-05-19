"""
align sequences using MAFFT
"""

from enum import Enum
from pathlib import Path
import subprocess
from typing import Optional

from latch import small_task, workflow
from latch.types import LatchFile, LatchDir #import LatchDir to use a directory as output

import os

@small_task
def infer_phylogeny_task(
    input_alignment: LatchFile,
    output_dir: LatchDir,
    output_prefix: Optional[str] = None,
    ufboot_reps: Optional[int] = 1000
    ) -> LatchDir:

    local_dir = "/root/iqtree_output/" #local directory to put output files in
    local_prefix = os.path.join(local_dir, output_prefix) # iqtree prefix including local path

    ## logic for how to align seqs
    _iqtree_cmd = [
        "iqtree2",
        "-s",
        input_alignment.local_path,
        "-pre",
        str(local_prefix), #this should probably be handled differently, since using empty prefix with -pre option causes a crash
        "-nt",
        "AUTO",
        "-m",
        "K80",
        "-bb",
        str(ufboot_reps) # the number needs to be formatted as string for the command to run properly
    ]

    subprocess.run(_iqtree_cmd)
    return LatchDir(local_dir, output_dir.remote_path) #this returns the directory in which all output files are stored

@workflow
def infer_phylogeny(
    input_alignment: LatchFile,
    output_dir: LatchDir,
    output_prefix: Optional[str] = None,
    ufboot_reps: Optional[int] = 1000
    ) -> LatchDir:
    """
    IQTREE2
    ----
    # IQTREE, efficient phylogenomic/phylogenetic inference
    ## About
    IQTREE infers phylogenies from multiple sequence alignments.

    <br /><br />

    If you found IQTREE useful, please cite *IQ-TREE 2: New models and efficient
    methods for phylogenetic inference in the genomic era*. Minh et al. 2020,
    Molecular Biology and Evolution. doi:
    [10.1093/molbev/msaa015](https://doi.org/10.1093/molbev/msaa015).

    <br /><br />

    To run IQTREE, user's must provide a minimum a multiple sequence
    alignment. This workflow conducts automated substitution matrix
    model testing. Specify output prefixes and the number of ultrafast
    bootstrap approximations (or UFBoot) to run.

    __metadata__:
        display_name: Infer phylogenetic/phylogenomic trees with IQTREE
        author: Jacob L. Steenwyk
            name: Jacob L. Steenwyk
            email: jlsteenwyk@gmail.com
            github: https://github.com/JLSteenwyk
        repository: http://www.iqtree.org/
        license:
            id: GNU-GPL

    Args:

        input_alignment:
            Input multiple sequence alignment of nucleotide or amino acid sequences
            __metadata__:
                display_name: "Input multi-FASTA file"
                appearance:
					comment: "Input multi-FASTA file"

        ufboot_reps:
            UFBoot (Ultrafast bootstrap approximation replicates)
            __metadata__:
                display_name: "Integer for number of UFBoot replicates to run"
                appearance:
					comment: "UFBoot replicates"

        output_prefix:
            Prefix of all outputted files.
			__metadata__:
				display_name: "Prefix of outputted files."
				appearance:
					comment: "Prefix of outputted files."

        output_dir:
            Output directory
			__metadata__:
				display_name: "Output directory"
				appearance:
					comment: "Output directory"

    """

    return infer_phylogeny_task(
        input_alignment=input_alignment,
        output_dir=output_dir,
        output_prefix=output_prefix,
        ufboot_reps=ufboot_reps
    )
