# Closing the gap in the clinical adoption of computational pathology: a standardized, open-source framework to integrate deep-learning algorithms into the laboratory information system
Framework based on HL7 messaging and freely available digital pathology (DP) resources to integrate deep-learning models into the anatomic pathology laboratory information system (AP-LIS)

> [!CAUTION]
> All software (except for the AP-LIS) and DL models employed in this work are non-commercial, open-source resources intended for research use only. Hence, use of the integration workflow outside of research context is under the responsibility of the user.

> [!TIP]
> 1. Once you download the code, please make sure to replace in the main.py script the variables storing the IP addresses as server (*hs*) and clienti (*hc*) with the corrisponding ports (*ps* and *pc*)
> 2. The developed framework was tested using AMD GPUs, but if you have NVIDIA GPUs please install pytorch accordingly

> Note
> The script is customized to run with mrxs files but it can be customized to run with other file formats as well.
> wsinfer-mil and marugoto scripts were costumized according to what written in the manuscript.
> The code was written to take into account multiple segment pairs associated with a given HL7 message, but at the end only one per patient was used.
> The code assumes that you are working with mrxs, where the output of the scanning is a folder containing the dat file and the ini file --> need to create the associated mrxs file to open it in QuPath.
> The script assume that we have a csv file called encodings_DL containing all the DL models information
> The model name assigned to your models should be the same as the name that you put in the fields XX and XX of the SPM segment
> Although the code assumes that you can run multiple slide per time, the main script is thought to run with only one slide per patient

## Installation
### Install 

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
