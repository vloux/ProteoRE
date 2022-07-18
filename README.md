# ProteoRE
## A biologist-oriented Galaxy platform for proteomics data exploration

With the increased simplicity associated with producing MS-based proteomics data, the bottleneck has now shifted to the functional analysis and exploration of large lists of expressed proteins to extract meaningful biological knowledge. Bioinformatics resources are often spread and disseminated under different forms (program/libraries/software/web tools and databases) and their access is rather limited for researchers without programming experience or no in-house bioinformatics support. As a consequence, interpretation of their data by experts remains a tedious and time-consuming process, and potentially error-prone (e.g., due to manual handling or input error).

The ProteoRE (Proteomics Research Environment) aims at fulfilling this need by centrally providing an online research service to assist biologists/clinicians in the interpretation of their proteomics data in a unified framework. Built upon the [Galaxy environment](https://github.com/galaxyproject), this web-based platform for computational biomedical research, allows researchers to apply a large range of dedicated bioinformatics tools and data analysis workflows on their data, share their analyses with others, and enable tiers to repeat the same analysis while keeping tracks of the overall process. 
 
Currently, ProteoRE implements 21 tools organized into four subsections for: i) data manipulation and visualization; ii) Get features/annotation; iii) functional analysis; and iv) pathway analysis along with graphical representations. Furthermore, we also developed a specialized tool that allow for the management of annotation from external resources upon which some ProteoRE’s tools are based (e.g. Uniprot, Human Protein Atlas, Biogrid, etc.). The ProteoRE platform has been designed in close collaboration with biomedical researchers on the basis of case studies such as functional analysis of a human MS/MS proteomics sample [1] and the selection of candidate proteomics biomarkers of human disease [2,3]. Our platform also provides online support, shared workflows and training materials (shared via the [Galaxy Training Network]- https://training.galaxyproject.org/training-material/topics/proteomics/) and is in free access: https://www.proteore.org. 

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
ProteoRE project is a joint national effort between the [French bioinformatics Institute (IFB)](https://www.france-bioinformatique.fr/en) and the [proteomics infrastructure (ProFI)](http://www.profiproteomics.fr) funded by the IFB via the French Research Agency (ANR-11-INBS-0013).

 
Project team
------------
David Christiany & Lien Nguyen (software engineers);  Florence Combes (bioinformatician);  Lisa Perus (internship);  Virginie Brun, Maud Lacombe, Marianne Tardif & Benoit Gilquin (use-case & beta-testing); Valentin Loux (Galaxy Manager) ; Yves Vandenbrouck (Project manager – yves.vandenbrouck@cea.fr) The Galaxy Project is supported in part by NHGRI, NSF, The Huck Institutes of the Life Sciences, The Institute for CyberScience at Penn State, and Johns Hopkins University.


Citations
---------
[1]	Combes F, Loux V, Vandenbrouck Y. GO Enrichment Analysis for Differential Proteomics Using ProteoRE. Methods Mol Biol. 2021;2361:179-196. doi: 10.1007/978-1-0716-1641-3_11. PMID: 34236662. 
[2]	Vandenbrouck Y, Christiany D, Combes F, Loux V, Brun V. Bioinformatics Tools and Workflow to Select Blood Biomarkers for Early Cancer Diagnosis: An Application to Pancreatic Cancer. Proteomics. 2019 Nov;19(21-22):e1800489. [doi:10.1002/pmic.201800489] (https://www.ncbi.nlm.nih.gov/pubmed/31538697).
[3] Nguyen L, Brun V, Combes F, Loux V, Vandenbrouck Y. Designing an In Silico Strategy to Select Tissue-Leakage Biomarkers Using the Galaxy Framework. Methods Mol Biol. 2019;1959:275-289. doi: 10.1007/978-1-4939-9164-8_18. PMID: 30852829.
