# ProteoRE
## User-oriented web-based platform for MS-based proteomics data exploration

The complex, rapidly-evolving field of mass spectrometry-based proteomics analysis calls for collaborative infrastructures where the large volume of algorithms for proteomics data and annotation can be readily integrated whatever the language, evaluated on reference datasets, and chained to build ad hoc workflows for users. Currently the exploitation of data delivered by proteomics platforms are still restricted owing to limited dedicated in-house bioinformatics capabilities. The aim of this project is to provide the life science community with a collaborative research online platform that would enable end-users to further explore their proteomics data by sharing workflows and experiments. This proteomics research environment (ProteoRE) is built upon the [Galaxy](https://github.com/galaxyproject) framework, a software platform that gives experimentalists simple interfaces to powerful tools, while automatically managing the computational details. It enables ergonomic integration, exchange, and running of individual modules and workflows. Three modules for proteomics data downstream analysis are foreseen: i. proteomics data control quality, ii. differential expression analysis and iii. proteomics data annotation. In addition ProteoRE  allow users to select one or more tools or resources to annotate data, and by automatically tracking the provenance of data and tool usage and enabling users to selectively run (and rerun) particular analyses. The development of this research environment may involve corrective or evolutionary maintenance or testing and a helpdesk will be set up. Tutorial are online on the [Galaxy Training Network](https://training.galaxyproject.org) and thematic school are organized regularly. 


With the increased simplicity associated with producing MS-based proteomics data, the bottleneck has now shifted to the functional analysis and exploration of large lists of expressed proteins to extract meaningful biological knowledge. Bioinformatics resources are often spread and disseminated under different forms (program/libraries/software/web tools and databases) and their access is rather limited for researchers without programming experience or no in-house bioinformatics support. As a consequence, interpretation of their data by experts remains a tedious and time-consuming process, and potentially error-prone (e.g., due to manual handling or input error).

 The ProteoRE (Proteomics Research Environment) aims at fulfilling this need by centrally providing an online research service to assist biologists/clinicians in the interpretation of their proteomics data in a unified framework. Built upon the [Galaxy environment](https://github.com/galaxyproject), this web-based platform for computational biomedical research, allows researchers to apply a large range of dedicated bioinformatics tools and data analysis workflows on their data, share their analyses with others, and enable tiers to repeat the same analysis while keeping tracks of the overall process. 
 
 Currently, ProteoRE implements 18 tools organized into four subsections for: i) data manipulation; ii) human and mouse species annotation; iii) functional analysis; and iv) pathway analysis along with graphical representations. Furthermore, we also developed a specialized tool that allow for the management of annotation from external resources upon which some ProteoRE’s tools rely on (e.g. Uniprot, Human Protein Atlas, Biogrid, etc.). The ProteoRE platform has been designed in close collaboration with biomedical researchers; it has recently been implemented for the functional analysis of a human MS/MS proteomics sample [1] and the selection of candidate proteomics biomarkers of human disease [2]. 

How to contribute
-----------------

### Get our tools
All ProteoRE's tools are publicly developped on [GitHub](https://github.com/ifb-git/ProteoRE).
These tools can be either tested via the [ProteoRE](http://www.proteore.org) main instance or installed on any Galaxy instance through the [Galaxy ToolShed](https://toolshed.g2.bx.psu.edu/repository/browse_repositories_by_user?user_id=dca2dd1ff3407665)

### Contribute
Please, do not hesitate to provide us with feedbacks on tools (by opening an issue or contacting us: contact@proteore.org ). We will be glad to consider any suggestion / feedback you may have.
For contributors, please note that any pull request / contribution will be examined for compliancy with the IUC standards.



Fundings 
---------
ProteoRE project is a joint national effort between the [French bioinformatics Institute (IFB)](https://www.france-bioinformatique.fr/en) and the [proteomics infrastructure (ProFI)](http://www.profiproteomics.fr) funded by the French Research Agency (ANR-11-INBS-0013).

    

Project team
------------
Lien Nguyen (software engineer), David Christiany (software engineer), Florence Combes (bioinformatician), Virginie Brun, Maud Lacombe, Marianne Tardif & Benoit Gilquin (use-case & beta-testing), Valentin Loux (Bioinformatician , IT Manager), Yves Vandenbrouck (Project manager – yves.vandenbrouck@cea.fr) The Galaxy Project is supported in part by NHGRI, NSF, The Huck Institutes of the Life Sciences, The Institute for CyberScience at Penn State, and Johns Hopkins University.


Citations
---------
[1]	Lacombe M et al. Proteomic characterization of human exhaled breath condensate. J Breath Res. 12(2):021001, 2018. [10.1088/1752-7163/aa9e71](https://doi.org/10.1088/1752-7163/aa9e71)

[2]	Nguyen L. et al., Designing an In Silico Strategy to Select Tissue-Leakage Biomarkers Using the Galaxy Framework. Methods Mol Biol. 1959:275-289, 2019. [10.1007/978-1-4939-9164-8_18](https://doi.org/10.1007/978-1-4939-9164-8_18)
