---
layout: tutorial_hands_on

title: Strategy for candidate biomarkers identification
zenodo_link: ''
questions:
- How to mine public databases to retrieve info?
- How to build a selection strategy by applying
  successive biochemical/cellular criteria to a list of gene/protein?
- How to select biomarkers candidates using experimental information (transcriptomics & proteomics)
  and annotation from public databases?

objectives:
- Build a workflow implementing a **strategy for the selection of tissue-leakage biomarkers** using ProteoRE

time_estimation:  minutes
key_points: biomarker, pipeline,

contributors:
- Florence Combes
- David Christiany
- Valentin Loux
- Yves VandenBrouck

---
# Introduction
{:.no_toc}

A biomarker is a measurable biological component that can be routinely detected in clinical practice and reflects a disease state, 
response to therapeutic treatment, or other relevant biological state. 

[ProteoRE Galaxy instance](http://www.proteore.org) provides necessary tools to execute a complete biomarkers selection pipeline. 
In this tutorial we introduce successively the tools of this pipeline, and guide you to execute them in order to complete the entire 
pipeline on a concrete example.

This strategy is described in  the following paper : 
[Designing an In Silico Strategy to Select Tissue-Leakage Biomarkers Using the Galaxy Framework](https://www.ncbi.nlm.nih.gov/pubmed/30852829)
by Nguyen *et al.* Proteomics for Biomarker Discovery: Methods and Protocols, Methods in Molecular Biology, vol. 1959, ISBN 978-1-4939-9164-8. 



# Global view of the strategy
{:.no_toc}

For this tutorial, no input data are required as the first steps will be to select data from 
public databases with ProteoRE tools. 

The strategy consists in selecting, one step after another, the most interesting candidates biomarkers. 
Our use-case here is to identify candidate biomarkers for myocardial infarction tissue-leakage. 

Criteria candidate biomarkers have to fulfill through this pipeline are: 
- heart-specificity
- cytoplasmic localization 
- detection in LC-MS/MS experiments already done

# Methods
{:.no_toc}

**Create a new history** and give it a name.
{% include snippets/create_new_history.md %}


Strategy is in 3 main steps:

> ### Table of contents
> 1. TOC
> {:toc}
{: .agenda}

# Selection of tissue-specific proteins based on experimental data available in HPA 

We will retrieve from [Human Protein Atlas](https://www.proteinatlas.org/) (HPA) database
proteins expressed in heart tissue according to immunohistochemistry (IHC) data 
and to RNA-seq data. 

> ### {% icon hands_on %} Build tissue-specific expression dataset
> 1. From **Tool Panel** choose **ProteoRE** > **Human Annotation** > **Build tissue-specific expression dataset** tool.
> 2. In **Experimental data source (antibody- or RNAseq-based)** file parameter, select **Expression profiles based on immunohistochemistry**. 
> 3. Click in the **Select tissue** box to select the tissue considered. In our example, tissue to select is 'Heart muscle'.
> 4. You can select the proteins based on their **Expression level** in the tissue. Choose 'High' and 'Medium" for this parameter. 
> 5. You can than choose the **Reliability score**  of this detection/expression level. Select 'Enhanced' and 'Supported' (the most reliable
> score according to HPA. 
> 6. Then click on the **'Execute'** button
> 
> > ### Output
> > - **Tissue-specific expression from IHC** (1596 lines): List of the selected proteins. 
> > 6 columns: 'Gene', 'Gene name' and the retrieved info from HPA. 
>{: .comment}
{:.hands_on}


> ### {% icon tip %} Tip: Change the name of a result dataset in Galaxy
>
> Result datasets in Galaxy are listed on the right panel of the window (your History). 
> They have a default name that you can change for a better comprehension of the files in your "history". 
> 
> To do so:
> * On the right panel of your Galaxy instance, 
> * At the right of the name you want to change,
> * Click on the "pen" icon (Edit attributes)
> * This opens the **Edit dataset attributes** on the central panel 
> * There you can write a new name for your dataset
> * Click on **Save**
{: .tip}


We will now rerun the same tool but to select transcripts according to their expression profile. 

> ### {% icon hands_on %} Build tissue-specific expression dataset
> 1. From **Tool Panel** choose **ProteoRE** > **Human Annotation** > **Build tissue-specific expression dataset** tool.
> 2. In **Experimental data source (antibody- or RNAseq-based)** file parameter, select **RNA levels based on RNA-seq experiments**. 
> 3. Click in the **Select tissue** box to select the tissue considered. In our example, tissue to select is 'Heart muscle'.
> 4. Then click on the **'Execute'** button
> 
> > ### Output
> > - **Tissue-specific expression from RNAseq** (19613 lines): List of the selected transcripts. 
> > 4 columns: 'Gene', 'Gene name' and the retrieved info from HPA. 
>{: .comment}
{:.hands_on}

This second list must be reduced by removing transcripts that are not highly enriched in heart muscle. 
To do so, a filter is applied on the expression value provided by HPA and measured in TPM (last column of the output file). 
In ProteoRE we'll use the "Filter by keywords and/or numerical value" tool. 

> ### {% icon hands_on %} Filter by keywords and/or numerical value
> 1. From **Tool Panel** choose **ProteoRE** > **Data Manipulation** > **Filter by keywords or numerical value** tool.
> 2. In **Input** file parameter, select **Tissue-specific expression from RNAseq**. 
> Keep default option **Yes** for header parameter.
> 3. Set **Operation** to 'Discard'
> 4. Click **Insert Filter by numerical value** box to set the parameters of the filter.
> 5. Fill in the parameters in **Filter by numerical value** section:
>     - The column of the input dataset on which the filter will be applied. In this case it is the column that contains "Value (in TPM unit)": it is c4. 
>     - You need to **Select operator** : choose '<='.
>     - Set the **Value** parameter to '10'.  
> 6. Then click on the **'Execute'** button.
> 
> > ### Outputs
> > - **Filtered Tissue-specific expression from RNAseq**: output list of the heart transcripts with a TPM Value >10 (5257 lines).  
> > - **Filtered Tissue-specific expression from RNAseq - discarded lines**: output list of the heart transcripts with a TPM Value less or equal to 10 (14356 lines, not what we want)
>{: .comment}
{:.hands_on}


We have now 2 datasets of heart-muscle proteins/transcripts, based on IHC data or TPM value. 

We want now to select candidate biomarkers that are expressed in the heart muscle according to **both** IHC and RNA-seq data, using the Jvenn tool. 

> ### {% icon hands_on %} Venn diagram
> 1. From Tool Panel choose **ProteoRE** > **Data Manipulation** > **Venn diagram** tool.
> 2. Set first input (**1: List to compare**) parameters:
>     - **Input file**: Tissue-specific expression from IHC
>     - **Header**: Yes
>     - **Column number**: c1
>     - **Name of the list**: heart IHC
> 3. Set second input (**2: List to compare**) parameters:
>     - **Input file**: Filtered Tissue-specific expression from RNAseq
>     - **Header**: Yes
>     - **Column number**: c1
>     - **Name of the list**: heart RNAseq
> 
> 4. Then click on the **'Execute'** button.
>
> > ### Output.
> > A text output and a graphical output are created. From the Venn diagram, we can see the number of proteins 
> > common/unique for each list combinations.
> > - **Venn diagram text output**
> > - **Venn diagram**
> > ![Venn Diagram output](../../images/jVenn_chart-tuto2.png "Venn diagram output")
>{: .comment}
{:.hands_on}

We see that we end up with 931 ID common to both IHC and RNA-seq lists. 

For greater clarity we'll keep only the column with those 931 ID to continue our pipeline. 
The **Cut columns from a table** tool will allow us to keep one column from our last dataset.  


> ### {% icon hands_on %} Cut columns from a table
> 1. From **Tool Panel** choose **Text Manipulation** > **Cut columns from a table (cut)** tool.
> 2. For **File to cut** parameter, select **Venn diagram text output** 
> 3. For **Operation** choose "Keep"
> 4. For **Delimited by** choose "Tab"
> 5. For **Cut by** choose "fields"
> 6. For **List of fields** parameter, click on the box and choose "Column: 3" to keep the last column of the dataset
> 5. Then click on the **'Execute'** button.
> 
> > ### Outputs
> > - **Cut on data 6**: The third column of the Venn diagram output. It has 4326 lines: the 931 ID in common between our 2 lists, and 'NA' for other lines. 
>{: .comment}
{:.hands_on}


Now we'll filter this dataset not to keep the 'NA' lines. 

> ### {% icon hands_on %} Filter by keywords and/or numerical value
> 1. From **Tool Panel** choose **ProteoRE** > **Data Manipulation** > **Filter by keywords or numerical value** tool.
> 2. In **Input** file parameter, select **Cut on data 6** 
> Keep default option **Yes** for header parameter.
> 3. Set **Operation** to 'Discard'
> 4. Click **Insert Filter by keywords** box to set the parameters of the filter.
> 5. Fill in the parameters in **Filter by keywords** section:
>     - The **column** of the input dataset is c1 
>     - **Search for exact match**: Yes
>     - Select **copy/paste** to **Enter keywords**
>	  - Write in the box the following **keywords to be filtered out**: "NA"
> 6. Then click on the **'Execute'** button.
> 
> > ### Outputs
> > - **Filtered Cut on data 6**: output list of ID different from NA (931 lines)  
> > - **Filtered Cut on data 6 - discarded lines**: output list NA lines (3394 lines, not what we want)
>{: .comment}
{:.hands_on}


Let's rename the 931 IDs dataset in "heart931" for simplification. 

Pipeline will then continue based on those 931, from which we have to select biomarkers that are
highly specific to the heart using additional expression data (still from HPA). 


> ### {% icon hands_on %} Add expression data
>
> 1. From Tool Panel choose **ProteoRE** > **Human annotation** > **Add expression data** tool.
> 2. In section **Enter your IDs**, option 'Input file containing your IDs' is chosen by default. Don't change it and set parameters as following:
>     - **Input file**: heart931 
>     - The **column number**: c1
>     - Does your input contain **header**: Yes
> 3. Numerous information can be extracted from the HPA source files (you can read user documentation at the end of the submission form of the tool for more detailed description). In this tutorial, we select 
>     - **Gene name**
>     - **Gene description**
>     - **RNA tissue category**
>     - **RNA tissue specificity abundance in 'Transcript Per Million'**.
> 4. Then click on the **'Execute'** button.
>
> > ### Outputs
> > - **Add expression data on data 8**: Four columns were added (number 2, 3, 4 and 5), corresponding to the HPA information previously selected.
>{: .comment}
{:.hands_on}


We wish to focus on transcripts that have been classed as (according to the HPA definition): 
* "tissue enriched" (expression in one tissue at least fivefold higher than all other tissues), 
* "group enriched" (fivefold higher average TPM in a group of two to to seven tissues compared to all other tissues) and 
* "tissue enhanced" (fivefold higher average TPM in one or more tissues/cell lines compared to the mean TPM for all tissues)

This information is listed in the column 4 : "RNA tissue category" of the result dataset. 

Let's use the "Filter by keywords and/or numerical value" tool to select the candidate biomarkers based on this 
"RNA tissue category" criterium. 

> ### {% icon hands_on %} Filter by keywords and/or numerical value
> 1. From **Tool Panel** choose **ProteoRE** > **Data Manipulation** > **Filter by keywords or numerical value** tool.
> 2. In **Input** file parameter, select **Add expression data on data 8** 
> 3. Keep default option **Yes** for header parameter.
> 4. Set **Operation** to 'Keep' 
> 5. Click **Insert Filter by keywords** box to set the parameters of the filter.
> 6. Fill in the parameters in **Filter by keywords** section:
>     - The **column** of the input dataset is c4 (see above for explanations) 
>     - **Search for exact match**: No
>     - Select **copy/paste** to **Enter keywords**
>	  - Write in the box the following **keywords to be filtered out**: "enriched enhanced"
> 6. Then click on the **'Execute'** button
> 
> > ### Outputs
> > - **Filtered Add_expression _data_on_data_8**: output list of the heart biomarkers with RNA tissue category containing "enriched" or "enhanced" (115 lines = what we are interested in).  
> > - **Filtered Add_expression _data_on_data_8  - discarded_lines**: output list of the heart biomarkers with RNA tissue category NOT containing "enriched" or "enhanced" (not what we are interested in).
>{: .comment}
{:.hands_on}


We now have identified 115 candidates considered to have significantly higher expression in heart muscle according to HPA criteria. 
Let's call the dataset where are those 115 candidates '**heart115**'. 


# Annotation of this protein list with biochemical and cellular features 

Candidate biomarkers we want to identify have to be cytoplasmic and without transmembrane domains (TMD). 
Thus we will retrieve protein features from neXtProt to retrieve those informations. 

Since HPA only considers ENSG identifiers (related to the gene), although neXtProt uses UniProt
identifiers (related to proteins), first thing to do is to map the Ensembl identifiers contained our list of (115) 
candidates to their corresponding UniProt accession number. The tool **ID Converter** is what we need to do so. 


> ### {% icon hands_on %} 1. ID Convert
> 1. From Tool Panel choose **ProteoRE** > **Data Manipulation** > **ID Converter** tool.
> 2. In section **Enter IDs**, option **Input file** containing your identifiers is chosen by default. Select input file and set its parameters as following:
>     - **Input file**: heart115
>     - **Does file contain header**: Yes
>     - **Column number of IDs to map**: c1
> 3. Set the Source type and Target type(s) of ID to map.
>     - **Species**: Human (Homo sapiens)
>     - **Type/source of IDs**: Ensembl gene ID (please scroll down)
>     - **Target type** of IDs: UniProt accession number and UniProt ID (multiple choices are possible)
> 4. Then click on the **'Execute'** button.
>
> >### Outputs 
> > - **ID Converter on data 11**: In this dataset, 2 columns (columns 6 and 7, at the end)
> > which contain UniProt accession number and ID are added.
>{: .comment}
{:.hands_on}


We have now UniProt IDs for the 115 candidate biomarkers: we are able to collect protein features from neXtProt. For this purpose, 
we use the **Add protein features** ProteoRE tool. 

> ### {% icon hands_on %} Add protein features
> 1. From Tool Panel choose **ProteoRE** > **Human Annotation** > **Add protein features** tool.
> 2. In section **Enter IDs**, option **Input file** to enter your IDs is chosen by default. Select input file and set its parameters as following:
>     - **Input file**: ID converter on data 12
>	  - **Column number of IDs to map**: c6
>     - **Does file contain header**: Yes
>     - **Type of IDs**: Uniprot accession number
> 3. In section **Select features** 
>     - **Physico-Chemical Features**: Number of transmembrane domains
>     - **Localization**: Subcellular Location
>     - **Disease information**: Yes
> 4. Then click on the **'Execute'** button.
>
> >### Outputs 
> > - **Add information from NextProt**: In this file (431 lines), 3 columns (8, 9 and 10) were added (at the end). 
> > These columns present TMDomains, Subcell Location and Diseases info.
>{: .comment}
{:.hands_on}
 

With this dataset, we can select proteins reported as localized in the cytoplasm and having
no transmembrane domains by running the Filter by keywords and/or numerical value tool. 


> ### {% icon hands_on %} Filter by keywords and/or numerical value
> 1. From **Tool Panel** choose **ProteoRE** > **Data Manipulation** > **Filter by keywords or numerical value** tool.
> 2. In **Input** file parameter, select **Add information from neXtProt**  
> Keep default option **Yes** for header parameter.
> 3. Set **Operation** to 'Keep' 
> 4. In **Select an operator to combine your filers** select 'AND' ('OR' by default)
> 5. Click **Insert Filter by keywords** box to set the parameters of the first filter.
> 6. Fill in the parameters in **Filter by keywords** section:
>     - The **column** of the input dataset is c9 (Subcellular Localization) 
>     - **Search for exact match**: No
>     - Select **copy/paste** to **Enter keywords**
>	  - Write in the box the following **keywords to be filtered out**: "cytoplasm cytosol"
> 7. Click **Insert Filter by numerical value** box to set the parameters of the second filter.
> 8. Fill in the parameters in **Filter by numerical value** section:
>     - The **column** of the input dataset is c8 (TMDomains) 
>     - **Select operator**: =
>     - **Value**: 0
> 9. Fill in the parameter **Sort by column** with: c5
> 10. Then click on the **'Execute'** button
> 
> > ### Outputs
> > - **Filtered Add_information_from_neXtProt**: output list of the proteins having a cytoplasmic location and no TMD (48 proteins).  
> > - **Filtered Add_information_from_neXtProt - discarded_lines**: output list of the proteins NOT cytoplasmic and having at least 1 TMD.  
>{: .comment}
{:.hands_on}


We have now 48 proteins. 

Next step : to identify proteins already seen in LS MS/MS experiments. 

# Check whether these proteins have already been detected by LC-MS/MS experiments


> ### {% icon hands_on %} Get MS/MS observations in tissue/fluid
> 1. From Tool Panel choose **ProteoRE** > **Human Annotation** > **Get MS/MS observations in tissue/fluid** tool.
> 2. In section **Enter your IDs**, option **Input file** to enter your IDs is chosen by default. Select input file and set its parameters as following:
>     - **Input file**: Filtered Add_information_from_neXtProt
>     - **Does file contain header**: Yes
>	  - **Column of IDs**: c6 (UniProt accession number) 
> 3. In section **Proteomics dataset (biological sample)** 
>     - check boxes for both 'Human Heart' and 'Human Plasma non glyco'
> 4. Then click on the **'Execute'** button.
>
> >### Outputs 
> > - **Get MS/MS observations in tissue/fluid on data 15**: 
> > In this file, 2 columns (columns 11 and 12, at the end) were added with the info of nb of times
> > peptides were seen by MS/MS. 
>{: .comment}
{:.hands_on}


Let's now keep only proteins that have already been seen by MS/MS in the plasma (last column of the file). 


> ### {% icon hands_on %} Filter by keywords and/or numerical value
> 1. From **Tool Panel** choose **ProteoRE** > **Data Manipulation** > **Filter by keywords or numerical value** tool.
> 2. In **Input** file parameter, select **Get MS/MS observations in tissue/fluid on data 16**  
> Keep default option **Yes** for header parameter.
> 3. Set **Operation** to 'Discard' 
> 4. Click **Insert Filter by keywords** box to set the parameters
> 5. Fill in the parameters in **Filter by keywords** section:
>     - The **column** of the input dataset is c12 (Nb of times peptides observed in Human Plasma) 
>     - **Search for exact match**: Yes
>     - Select **copy/paste** to **Enter keywords**
>	  - Write in the box the following **keywords to be filtered out**: NA
> 6. Then click on the **'Execute'** button
> 
> > ### Outputs
> > - **Filtered Get MS/MS observations in tissue/fluid on data 15**: output list of the proteins whose some peptides have been seen in plasma (21 proteins)
> > - **Filtered Get MS/MS observations in tissue/fluid on data 15 - discarded_lines**: output list of proteins with no peptides seen in the plasma
>{: .comment}
{:.hands_on}



**How to extract a workflow from your history** 
{% include snippets/extract_workflow.md %}



# Conclusion
{:.no_toc}

At the end of the process we end up with a list of 21 biomarkers that are **highly enriched in heart muscle**, localized 
**in the cytosol** and **detectable by MS in the plasma**. 

Briefly and from a biological point of view, 3 of these proteins exhibit a relative low detection level in the plasma
compared to heart muscle tissue, and are reported with a very high heart-muscle-specific RNA abundance. 
These potential mechanistic biomarkers of myocardial infarction include (i) cardiac Troponin I type 3 (TNNI3 (P19429)) 
that is routinely used as the most specific marker of myocardial injury and (ii) the heart-type fatty acid-binding protein
(FABP3 (P05413)) that has been proposed as a diagnostic and prognostic marker for acute and chronic cardiac injury. 

Extraction of workflow is first valuable for analyses reproductibility and tracability. 

Moreover, a workflow can also be made reusable with modifiable parameters, and as a result this strategy can
be applied to other types of tissue injury (e.g. brain, liver, kidney). 





