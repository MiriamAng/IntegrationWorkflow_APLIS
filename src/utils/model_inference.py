# -*- coding: utf-8 -*-
""" The script runs deep-learning deployment with one of the three freely available toolboxes:
1) WSInfer (Kaczmarzyk, J. R. et al. Open and reusable deep learning for pathology with WSInfer and QuPath. NPJ Precis. Oncol. 8, 9 (2024))
2) WSInfer-MIL (https://github.com/SBU-BMI/wsinfer-mil; https://zenodo.org/records/12680704)
3) marugoto (https://github.com/KatherLab/marugoto)

Author: Miriam Angeloni
E-Mail: miriam.angeloni@uk-erlangen.de
"""

import os
import subprocess
import time

from colorama import init, Fore
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from utils import create_qupath_proj

# Automatically reset the style to normal after each print statement
init(autoreset=True)

def create_csv_marugoto(slidename : str,
                        target_label : str,
                        cat_labels : list,
                        outputdir : str | Path):
    """
    This function creates the CSV files to use as input for the --clini_table argument and --slide-csv argument during model deployment with marugoto
    :param slidename: slide identifier
    :param target_label: e.g., BRAF or isMSIH
    :param cat_labels: categorical labels predicted by the model (e.g., MUT,WT or MSIH,nonMSIH)
    :param outputdir: full path where to store the two dataframes generated
    :results: 2 dataframes, cli-table.csv and slide-table.csv
    """
    
    # The clinical table contains the columns 'PATIENT' and 'target_variable' (i.e., BRAF/isMSIH)
    clini_table = pd.DataFrame({'PATIENT':[f"{slidename}"], f'{target_label}':[f"{cat_labels[0]}"]})
    clini_table.to_csv(os.path.join(outputdir, "cli-table.csv"), index=False)
    
    # The slide table contains the columns 'PATIENT' and the column 'FILENAME' that refers to the file name of the features without the .h5 extension
    slide_table = pd.DataFrame({'PATIENT':[f"{slidename}"], 'FILENAME':[f"{slidename}_features"]})
    slide_table.to_csv(os.path.join(outputdir, "slide-table.csv"), index=False)
    

# Run marugoto
def marugoto_dep(slidename : str,
                slidedir : str | Path, 
                ckpt_path :str | Path,
                modeldir : str | Path, 
                target_label : str,
                cat_labels : list, 
                outputdir : str | Path):
    """
    This function runs all the steps, from tiles generation, to features vectors calculation, and ultimately deep-learning model
    deployment, to run inference withe the marugoto toolbox.
    :param slidename: slide identifier
    :param slidedir: full path to the slide in the temporary slides folder
    :param ckpt_path: full path to the best_ckpt.pth file for feature extraction
    :param modeldir: full path to the .pkl file storing model weights for inference
    :param target_label: e.g., BRAF or isMSIH
    :param cat_labels: categorical labels predicted by the model (e.g., MUT,WT or MSIH,nonMSIH)
    :param outputdir: full path where to store the output of wsinfer/marugoto

    """
    
    print(f"{Fore.BLUE}*" * 100)
    print(f"{Fore.BLUE}Running model inference with marugoto for slide: {slidename}") 
    
    # Tiles generation (h5 file)
    command_tiles_gen = f"wsinfer --backend=openslide patch --wsi-dir {slidedir} --results-dir {outputdir} --patch-size-px 224 --patch-spacing-um-px 1.14"
    subprocess.call(command_tiles_gen, shell = True)
    print(f"{Fore.BLUE}Tiles generation completed for slide {slidename}")
    
    # Features extraction
    patches_dir = Path(rf"{outputdir}/patches/{slidename}.h5")
    command_feat_extr = f"python -m marugoto.extract.xiyue_wang --checkpoint-path {ckpt_path} --outdir {outputdir} {patches_dir}"
    subprocess.call(command_feat_extr, shell = True)
    print(f"{Fore.BLUE}Features extraction completed for slide {slidename}")
    
    # Model deployment
    cli_table_path = Path(rf"{outputdir}/cli-table.csv")
    slide_table_path = Path(rf"{outputdir}/slide-table.csv")
    command_dep = f"python -m marugoto.mil deploy --clini_table {cli_table_path} --slide-csv {slide_table_path} --feature-dir {outputdir} --model-path {modeldir} --output_path {outputdir} --target_label {target_label} --cat_labels [{cat_labels[0]},{cat_labels[1]}]"
    subprocess.call(command_dep, shell = True)
    
    print(f"{Fore.BLUE}Model deployment completed for slide {slidename}")



def extract_marugoto_res(outputdir : str | Path,
                       target_label : str):
    """
    This function extract results (i.e., predicted label and associated prediction score)
    from deep-learning model deployment using marugoto.

    :param outputdir : path to the CSV file (patient-preds.csv) containing model's predictions
    :param target_label: e.g., BRAF or isMSIH

    """

    preds_file = Path(rf"{outputdir}/patient-preds.csv")
    preds_df = pd.read_csv(preds_file)
    
    prob_columns = [colname for colname in preds_df.columns if f'{target_label}_' in colname]
    pred_colname = preds_df.iloc[0][prob_columns].idxmax()
    pred_score = preds_df.iloc[0][f"{pred_colname}"]
    
    return pred_colname, pred_score



# Extract WSInfer-MIL results
def extract_wsinfermil_res(outputdir : str | Path,
                           model : str,
                           classes : list):
    """
    This function extract results (i.e., predicted label and associated prediction score)
    from deep-learning model deployment using WSInfer-MIL.

    :param outputdir: path to the CSV file (model_preds.csv) containing model's predictions
    :param model: name of the deep-learning model used for deployment
    :param classes: classes predicted by the deep-learning model

    """
    if 'survival' in model:
        # Basing on model's name we can deduct whether it is a model to predict cancer risk-related death or the status
        # of clinical biomarkers
        risk_file = Path(rf"{outputdir}/risk_score.csv")
        risk_score_df = pd.read_csv(risk_file)
        rs = risk_score_df.loc[0,"Risk_score"]
        if 'kirp' in model:
            if rs < -2.84:
                rs_high_low = "Low"
            else:
                rs_high_low = "High"
        elif 'gbmlgg' in model:
            if rs < -3.22:
                rs_high_low = "Low"
            else:
                rs_high_low = "High"
        pred_class = f"{rs_high_low} risk"
        pred_score = rs
                
    else:
        preds_file = Path(rf"{outputdir}/model_preds.csv")
        preds_df = pd.read_csv(preds_file)
        
        idx_max = preds_df["Probability"].idxmax()
        pred_class = classes[idx_max]
        pred_score = preds_df.iloc[idx_max]["Probability"]
    
    return pred_class, pred_score



def run_inference(slide_id : list,
                  spm_4_2 : str,
                  slides_archive : str | Path,
                  wdir : str | Path):

    """
    This function runs deep-learning model deployment with one of the three available open-source toolboxes for inference:
    1) WSInfer
    2) WSInferMIL
    3)marugoto

    :param slide_id: slide identifier
    :param spm_4_2: name of the deepl-learning model as indicated in the SPM field 4.2 of the input OML^O33 HL7 message
    :param slides_archive: path to the slides archive
    :param wdir: path to the working directory
    """
    
    # Initialize empty lists to store the prediction value(s) and the prediction score(s) associated with DL model deployment
    pred_labels = []
    pred_scores = []
    
    for slide in slide_id:
        # Define the temporary slide directory where to store each new analyzed slide
        tmp_slidedir = Path(rf"{wdir}/tmp_slides/{slide}")
        
        # Check if tmp_slidedir exists, and if it does not exist create the folder
        if not os.path.exists(tmp_slidedir):
            print(rf"...Creating {tmp_slidedir}")
            os.makedirs(tmp_slidedir)
            src = Path(rf"{slides_archive}/{slide}")
            dest = Path(rf"{tmp_slidedir}/{slide}")
            move_slide_cmd = f"cp -r {src} {dest}"
            print(f"...Copying slide {slide} to {tmp_slidedir}")
            subprocess.call(move_slide_cmd, shell = True)
            
            # Create an empty mrxs file, if it does not exist, in the temporary slide folder
            mrxs_path = Path(rf"{tmp_slidedir}/{slide}.mrxs")
            if os.path.isfile(mrxs_path):
                pass
                print(rf"File {slide}.mrxs already exists.")
            else:
                open(mrxs_path, "x").close()
                print(rf"File {slide}.mrxs is being created.")
        else:
            # If the folder already exists, it means that the slide has been previously analyzed with other algorithms
            print(f"Slide {slide} already exists...Skipping copy of slide under {tmp_slidedir}")
        
        custom_modelsdir = Path(rf"{wdir}/custom_DL_models")
        
        # Read in intput the configuration CSV file containing all the DL models, with information on:
        # 1) the toolbox to use for each model
        # 2) the visualization style
        # 3) the classes predicted
        df = pd.read_csv(Path(rf"{wdir}/encodings_DL.csv"))
        
        # Extract the row index corresponding to the model to deploy
        idx = df.index[df['SPM_4.2'] == f"{spm_4_2}"].tolist()
        
        # Extract DL model name
        model_name = df.loc[idx, 'Model_Name'].to_string(index=False)
    
        # Create the results directory storing results for a given model deployed on a given slide
        tmp_resdir = Path(rf"{wdir}/tmp_results/{slide}/{model_name}")
        if not os.path.exists(tmp_resdir):
            os.makedirs(tmp_resdir)

        # Extract class labels
        class_names = df.loc[idx, 'Class_Names'].to_string(index=False)
        if "," in class_names:
            # Transform into list and remove white spaces to avoid spaces after comma
            class_names = class_names.replace(" ", "").split(",")
        else:
            class_names = [class_names]

        # Extract the name of the toolbox to use I
        toolbox = df.loc[idx, 'Toolbox'].to_string(index=False)

        if toolbox == 'marugoto':
            
            target_label = spm_4_2.split("_")[0]
            
            cohort = spm_4_2.split("_")[1]

            ckpt_path = Path(rf"{custom_modelsdir}/marugoto/best_ckpt.pth")
            
            pkl_path = Path(rf"{custom_modelsdir}/marugoto/{cohort}/{target_label}/export.pkl")
            
            for _ in tqdm(range(100), desc="Creating marugoto CSV files"):
                create_csv_marugoto(slide, target_label, class_names, tmp_resdir)
                time.sleep(0.001)

            # Run deployment
            marugoto_dep(slide, tmp_slidedir, ckpt_path, pkl_path, target_label, class_names, tmp_resdir)

            # Extract the predicted label and the associated prediction score
            pred_label, pred_score = extract_marugoto_res(tmp_resdir, target_label)
            
            pred_labels.append(pred_label)
            
            pred_scores.append(pred_score)

        elif toolbox == 'wsinfer-mil':
            command_wsinfer_mil = f"wsinfer-mil run -m kaczmarj/{model_name} -i {tmp_slidedir}/{slide}.mrxs"
            
            print(f"{Fore.BLUE}*" * 100)
            print(f"{Fore.BLUE}Running model inference with WSInfer-MIL for slide: {slide}")
            subprocess.call(command_wsinfer_mil, shell = True)

            # Extract the predicted label and the associated prediction score
            pred_label, pred_score = extract_wsinfermil_res(tmp_resdir, model_name, class_names)
            
            # Define the QuPath directory to create the visualization through density maps
            qupathdir = Path(rf"{tmp_resdir}/qupath-proj")
            
            print(f"{Fore.MAGENTA}*" * 100)
            print(f"{Fore.MAGENTA}Creating density map for slide: {slide}")
            create_qupath_proj.create_density_map(slide, tmp_slidedir, tmp_resdir, qupathdir, pred_label, pred_score)
            
            pred_labels.append(pred_label)
            
            pred_scores.append(pred_score)

        else:
            # Run WSInfer for patch-level classification tasks
            qupathdir = Path(rf"{tmp_resdir}/qupath-proj")

            customized_model = df.loc[idx, 'Customized'].to_string(index=False) #Yes/No
                
            if customized_model == "Yes":

                #  We have to specify the model by providing as additional files a .pt file and a JSON file
                model_path = Path(rf"{custom_modelsdir}/{model_name}/model.pt")
                config_path = Path(rf"{custom_modelsdir}/{model_name}/config.json")
                command_wsinfer = f"wsinfer --backend=openslide run --wsi-dir {tmp_slidedir}/ --results-dir {tmp_resdir} --model-path {model_path} --config {config_path}"
            else:
                # We are using a WSInfer built-in model
                command_wsinfer = f"wsinfer --backend=openslide run --wsi-dir {tmp_slidedir}/ --results-dir {tmp_resdir} --model {model_name}"

            print(f"{Fore.BLUE}*" * 100)
            print(f"{Fore.BLUE}Running model inference with WSInfer for slide: {slide}")
            subprocess.call(command_wsinfer, shell = True)

            model_resdir = Path(rf"{tmp_resdir}/model-outputs-csv")

            # Since we are dealing with patch-level classification models, we will not have a slide-level predicted label nor a slide-level prediction score, but rather
            # tiles-level metrics.
            pred_labels.append(None)
            pred_scores.append(None)

            # Select the appropriate colored heatmap
            visualization = df.loc[idx, 'Visualization'].to_string(index=False)
            if visualization == "measurement_map":
                print(f"{Fore.MAGENTA}*" * 100)
                print(f"{Fore.MAGENTA}Creating measurement map for slide: {slide}")
                create_qupath_proj.create_measurement_map(slide, tmp_slidedir, model_resdir, qupathdir, class_names)
            elif visualization == 'color_map':
                print(f"{Fore.MAGENTA}*" * 100)
                print(f"{Fore.MAGENTA}Creating color map for slide: {slide}")
                create_qupath_proj.create_color_map(slide, tmp_slidedir, model_resdir, qupathdir)
                
    return model_name, pred_labels, pred_scores


if __name__ == "model_inference":
    run_inference()




