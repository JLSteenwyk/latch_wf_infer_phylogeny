"""
align sequences using MAFFT
"""

from enum import Enum
from pathlib import Path
import subprocess
from typing import Optional

from latch import small_task, workflow
from latch.types import LatchFile


@small_task
def infer_phylogeny_task(
    input_alignment: LatchFile,
    output_prefix: Optional[str] = None,
    ufboot_reps: Optional[int] = 1000
    ) -> LatchFile:

    ## logic for how to align seqs
    _iqtree_cmd = [
        "iqtree2",
        "-s",
        input_alignment.local_path,
        "-pre",
        output_prefix,
        "-nt",
        "AUTO",
        "-m",
        "TEST",
        "-bb",
        ufboot_reps
    ]

    # # figuring out how to write out multiple files based on prefix
    # with open(out_file, "w") as f:
    #     subprocess.call(_iqtree_cmd, stdout=f)

    # return LatchFile(str(output_prefix), f"latch:///{output_prefix.name}")


@workflow
def infer_phylogeny(
    input_alignment: LatchFile,
    output_prefix: Optional[str] = None,
    ufboot_reps: Optional[int] = 1000
    ) -> LatchFile:
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

    """

    return infer_phylogeny_task(
        input_alignment=input_alignment,
        output_prefix=output_prefix,
        ufboot_reps=ufboot_reps
    )
