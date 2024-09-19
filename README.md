# Closing the gap in the clinical adoption of computational pathology: a standardized, open-source framework to integrate deep-learning algorithms into the laboratory information system
A standardized, open-source framework to integrate both <ins>publicly available</ins> and <ins>custom developed</ins> deep-learning (DL) models into the anatomic pathology laboratory information system (AP-LIS).
The developed integration framework relies on a Python-based server-client architecture to: 
1. interconnect the AP-LIS with an AI-based decision support sistem (AI-DSS) via HL7 messaging

<p align="center">
  <img src="https://github.com/MiriamAng/IntegrationFramework_APLIS/blob/main/docs/integration_framework.png" width="600" />
</p>
  
2. run DL model deployment using freely available resources ([WSInfer](https://github.com/SBU-BMI/wsinfer), [WSInfer-MIL](https://github.com/SBU-BMI/wsinfer-mil), [marugoto](https://github.com/KatherLab/marugoto))

3. provide an intuitive visualization of model inference results through colored heatmaps in [QuPath](https://qupath.github.io/)
<p align="center">
  <img src="https://github.com/MiriamAng/IntegrationFramework_APLIS/blob/main/docs/visualization_styles.PNG" width="700" />
</p>

  
> [!CAUTION]
> All DL models employed in this work as well as the freely available software used for DL model deployment and visualization are non-commercial, open-source resources intended for research use only. Hence, use of the integration framework outside of research context is under the responsibility of the user.

> [!TIP]
> 1. Once you download the code, please make sure to replace in the main.py script the variables storing the IP addresses as server (*hs*) and clienti (*hc*) with the corrisponding ports (*ps* and *pc*)
> 2. The developed framework was tested using AMD GPUs, but if you have NVIDIA GPUs please install pytorch accordingly

> [!NOTE]
> 1. The scripts have been developed and tested using WSIs in MRXS format. Hence: (i) a directory exists storing a file named Slidedat.ini; (ii) an mrxs file needs to be created in the same location as the directory, with the same name as the directory plus the .mrxs extension in order to be opened in Qupath.
> 2. [WSInfer-MIL](https://github.com/SBU-BMI/wsinfer-mil) and [marugoto](https://github.com/KatherLab/marugoto) source codes were partially costumized. Please refer to the Supplementary Material of [our preprint](https://www.biorxiv.org/content/10.1101/2024.07.11.603091v1) for detailed information on how the scripts were modified to comply with our framework's requirements. 
> 3. The code was written to take into account multiple segment pairs associated with a given HL7 message, but at the end only one per patient was used.
> The scripts assume that you have a CSV file called encodings_DL.csv containing information on the DL models to deploy integrated in the framework. An example of encodings_DL.csv file can be downloaded found [here](https://github.com/MiriamAng/IntegrationFramework_APLIS/blob/main/docs/encodings_DL.csv).
> The fields 4.1 and 4.2 of the SPM segment of the input OML^O33 HL7 message should be populated with the name of the DL model from column 'SPM_4.2' of the encodings_DL.csv file.

## Software requirements and setup
The integration framework has been developed and tested on a remote server based on Ubuntu's LTS operating system equipped with two AMD Radeon Instinct MI210 GPUs. Hence, PyTorch was installed with ROCm support. 
For NVIDIA GPUs please customize PyTorch installation with CUDA support. 

To get started, clone the GitHub respository through the command:
```bash
git clone https://github.com/MiriamAng/IntegrationFramework_APLIS.git
```
or
```bash
git clone git@github.com:MiriamAng/IntegrationFramework_APLIS.git
```

We suggest to run the integration framework in a dedicated conda environment. This can be built through the yml file provided [here]() as follows:
```bash
# Crete the conda environment env_name
conda env create -f /path/to/IntegrationFramework_APLIS/conda_env.yml

# Activate the conda environment
conda activate env_name
```
### Example of results folder structure after deployment of a DL model
**1. WSInfer built-in models**
Example of results folder structure afer running one of the WSInfer built-in models, e.g., the *colorectal-resnet34.penn* model. 
```bash
\---tmp_results
    \---00002548745622
        \---colorectal-resnet34.penn
            |   run_metadata.json
            |
            +---masks
            |       00002548745622.jpg
            |
            +---model-outputs-csv
            |       00002548745622.csv
            |       00002548745622_withoffset.csv
            |
            +---model-outputs-geojson
            |       00002548745622.geojson
            |
            +---patches
            |       00002548745622.h5
            |
            \---qupath-proj
                \---00002548745622_QuPathProj-colorectal_resnet34_penn
                    |   00002548745622-colorectal_resnet34_penn.qpproj
                    |   00002548745622-colorectal_resnet34_penn.qpproj.backup
                    |   project.qpproj.backup
                    |
                    +---classifiers
                    \---data
```

**2. WSInfer-MIL built-in models**
Example of results folder structure afer running one of the WSInfer-MIL built-in models, e.g., the *pancancer-tp53-mut.tcgan* model. 

**3. marugoto**
Example of results folder structure after running the *braf-attMIL-marugoto* model with marugoto 
```bash
\---tmp_results
    \---00002548745621
        \---braf-attMIL-marugoto
            |   cli-table.csv
            |   patient-preds.csv
            |   slide-table.csv
            |
            \---patches
                    00002548745621.h5
```

> [!NOTE]
> 1. The scripts have been developed and tested using WSIs in MRXS format. Hence: (i) a directory exists storing a file named Slidedat.ini; (ii) an mrxs file needs to be created in the same location as the directory, with the same name as the directory plus the .mrxs extension in order to be opened in Qupath.
> 2. [WSInfer-MIL](https://github.com/SBU-BMI/wsinfer-mil) and [marugoto](https://github.com/KatherLab/marugoto) source codes were partially costumized. Please refer to the Supplementary Material of [our preprint](https://www.biorxiv.org/content/10.1101/2024.07.11.603091v1) for detailed information on how the scripts were modified to comply with our framework's requirements. 
> 3. The code was written to take into account multiple segment pairs associated with a given HL7 message, but at the end only one per patient was used.
> The scripts assume that you have a CSV file called encodings_DL.csv containing information on the DL models to deploy integrated in the framework. An example of encodings_DL.csv file can be downloaded found [here](https://github.com/MiriamAng/IntegrationFramework_APLIS/blob/main/docs/encodings_DL.csv).
> The fields 4.1 and 4.2 of the SPM segment of the input OML^O33 HL7 message should be populated with the name of the DL model from column 'SPM_4.2' of the encodings_DL.csv file.

## Citation
If you find our work useful, please cite [our preprint](https://www.biorxiv.org/content/10.1101/2024.07.11.603091v1)!
```bash
@article{angeloni2024closing,
  title={Closing the gap in the clinical adoption of computational pathology: a standardized, open-source framework to integrate deep-learning algorithms into the laboratory information system},
  author={Angeloni, Miriam and Rizzi, Davide and Schoen, Simon and Caputo, Alessandro and Merolla, Francesco and Hartmann, Arndt and Ferrazzi, Fulvia and Fraggetta, Filippo},
  journal={bioRxiv},
  year={2024},
  doi={https://doi.org/10.1101/2024.07.11.603091}
}
```

## References
1) Kaczmarzyk, J. R. et al. Open and reusable deep learning for pathology with WSInfer and QuPath. NPJ Precis. Oncol. 8, 9 (2024).
2) WSInfer-MIL: https://zenodo.org/records/12680704
3) marugoto: https://github.com/KatherLab/marugoto
4) Bankhead, P. et al. QuPath: Open source software for digital pathology image analysis. Sci. Rep. 7, 1-7 (2017).


