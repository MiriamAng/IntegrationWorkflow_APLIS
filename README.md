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
> The scripts assume that you have a CSV file called encodings_DL.csv containing information on the the integrated DL models to deploy. An example of encodings_DL.csv file can be downloaded found [here
> The fields 4.1 and 4.2 of the SPM segment of the input OML^O33 HL7 message should be populated with the name of the DL model as indicated in column

## Installation

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
