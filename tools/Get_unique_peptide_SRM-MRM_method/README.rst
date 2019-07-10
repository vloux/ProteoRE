        **Description**

This tool allows you to get SRM/MRM informations from Uniprot-AC IDs.

-----

**Input**

A list of IDs (entered in a copy/paste mode) or a single-column file, the tool will then return a file containing the wanted protein features. 
If your input is a multiple-column file, the mapped IDs column(s) will be added at the end of the input file.

.. class:: warningmark

Accession numbers with an hyphen ("-") that normally correspond to isoform are not considered as similar to its canonical form.

.. class:: warningmark

In copy/paste mode, the number of IDs considered in input is limited to 5000.

-----

**Parameters**

- **Enter IDS:** enter your Uniprot-AC from a file or a copy paste
- **Release:** choose the release you want to use for retrieving protein sequences / features 
- **Protein sequence/Features:** choose proteins features you want to retrieve

-----

**Output**

A text file containing the selected protein features (in addition to the original column(s) provided).
Please, note that a "NA" is returned when there is no match between a source ID and SRM/MRM source file.

-----

**Data sources (release date)**

This tool is using the following source file:

- `HumanSRMAtlasPeptidesFinalAnnotated (2016-04) <http://www.srmatlas.org/downloads/HumanSRMAtlasPeptidesFinalAnnotated.xlsx>`_.

-----

.. class:: infomark

**Authors**

David Christiany, Florence Combes, Yves Vandenbrouck CEA, INSERM, CNRS, Grenoble-Alpes University, BIG Institute, FR

Sandra Dérozier, Olivier Rué, Christophe Caron, Valentin Loux INRA, Paris-Saclay University, MAIAGE Unit, Migale Bioinformatics platform, FR

This work has been partially funded through the French National Agency for Research (ANR) IFB project.

Help: contact@proteore.org for any questions or concerns about this tool.