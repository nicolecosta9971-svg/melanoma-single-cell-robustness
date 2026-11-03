# References and source credit

These links credit the biological data, methods and interpretive foundations. Original investigators generated the experimental data; this portfolio presents secondary computation and interpretation. Inclusion is not endorsement by the investigators or permission to redistribute each resource. See [data availability](DATA_AVAILABILITY.md) and [resource-specific terms](THIRD_PARTY_TERMS.md).

## Primary source cohort and deposit

1. Poźniak J et al. **A TCF4-dependent gene regulatory network confers resistance to immunotherapy in melanoma.** Cell, 2024. [DOI 10.1016/j.cell.2023.11.037](https://doi.org/10.1016/j.cell.2023.11.037).
2. Poźniak J et al. **Cytotoxic NK Cells Impede Response to Checkpoint Immunotherapy in Melanoma with an Immune-Excluded Phenotype.** Cancer Discovery, 2025. [DOI 10.1158/2159-8290.CD-24-1208](https://doi.org/10.1158/2159-8290.CD-24-1208).
3. **KU Leuven Research Data Repository, DOI 10.48804/GSAXBN, version 7.** [Version-specific deposit](https://rdr.kuleuven.be/dataset.xhtml?persistentId=doi:10.48804/GSAXBN&version=7.0); [processed immune-cell file 266111](https://rdr.kuleuven.be/file.xhtml?fileId=266111&version=7.0).
4. **MarineLab/Poźniak source-processing repository.** [Repository](https://github.com/MarineLab/Pozniak-et-al_TCF4_paper); [GC_ALL.R at the source-audited commit](https://github.com/MarineLab/Pozniak-et-al_TCF4_paper/blob/cfc178c2c15f318a3b4d9da7448909237a48a3bc/GC_ALL.R). Linked for provenance, not redistributed.

References 1 and 2 concern the same cohort. The original investigators generated the experimental data and source annotations. Neither paper is counted as an independent cohort replication of this reanalysis's locked ratio.

## External evidence sources

5. Sade-Feldman M et al. **Defining T Cell States Associated with Response to Checkpoint Immunotherapy in Melanoma.** Cell, 2018. [DOI 10.1016/j.cell.2018.10.038](https://doi.org/10.1016/j.cell.2018.10.038); [GEO GSE120575](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE120575).
6. Schlenker et al. **Myeloid-T cell interplay and cell state transitions associated with checkpoint inhibitor response in melanoma.** 2024. [PubMed record 38593812](https://pubmed.ncbi.nlm.nih.gov/38593812/).
7. Schwalie P. **MelanomaCITResponse_scRNAseq_TILandPBMC_publication_data**, version 3, 4 June 2025. [Zenodo DOI 10.5281/zenodo.15593993](https://doi.org/10.5281/zenodo.15593993). The record links the processed data to reference 6 and ArrayExpress E-MTAB-13770. Dataset-deposit creator credit and paper authorship are distinguished deliberately.

These datasets are external comparisons with material platform, measurement and/or outcome-definition differences. Their citation is not a claim of confirmatory biomarker validation.

## Computational and statistical methods

8. Lopez R et al. **Deep generative modeling for single-cell transcriptomics.** Nature Methods, 2018. [DOI 10.1038/s41592-018-0229-2](https://doi.org/10.1038/s41592-018-0229-2).
9. Wolf FA, Angerer P, Theis FJ. **SCANPY: large-scale single-cell gene expression data analysis.** Genome Biology, 2018. [DOI 10.1186/s13059-017-1382-0](https://doi.org/10.1186/s13059-017-1382-0).
10. Domínguez Conde C et al. **Cross-tissue immune cell analysis reveals tissue-specific features in humans.** Science, 2022. [DOI 10.1126/science.abl5197](https://doi.org/10.1126/science.abl5197).
11. **Automatic cell-type harmonization and integration across Human Cell Atlas datasets.** Cell, 2023. [DOI 10.1016/j.cell.2023.11.026](https://doi.org/10.1016/j.cell.2023.11.026). Cited alongside reference 10 by the [official CellTypist model catalogue](https://www.celltypist.org/models).
12. Andreatta M et al. **Interpretation of T cell states from single-cell transcriptomics data using reference atlases.** Nature Communications, 2021. [DOI 10.1038/s41467-021-23324-4](https://doi.org/10.1038/s41467-021-23324-4); [ProjecTILs software and reference links](https://github.com/carmonalab/ProjecTILs).
13. Büttner M et al. **scCODA is a Bayesian model for compositional single-cell data analysis.** Nature Communications, 2021. [DOI 10.1038/s41467-021-27150-6](https://doi.org/10.1038/s41467-021-27150-6).
14. Squair JW et al. **Confronting false discoveries in single-cell differential expression.** Nature Communications, 2021. [DOI 10.1038/s41467-021-25960-2](https://doi.org/10.1038/s41467-021-25960-2).

These methods were used in or informed the retained research; the aggregate export is not a new execution. The public synthetic calculation does not implement, rerun or redistribute the full scientific workflow. The fixed CellTypist model name is `Immune_All_Low`; the official catalogue defines "Low" as low-hierarchy/high-resolution, not low-resolution.

## Release and research-reporting guidance

- [GitHub: licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).
- [Creative Commons: CC BY-NC-SA 4.0 summary](https://creativecommons.org/licenses/by-nc-sa/4.0/).

The source dataset's terms must not be substituted with article or software terms. [Data availability](DATA_AVAILABILITY.md) and [source terms](THIRD_PARTY_TERMS.md) record the boundaries; no new ethics determination, funding statement or research-author list is established by these citations.
