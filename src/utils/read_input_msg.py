# -*- coding: utf-8 -*-
"""
The script reads the input OML^O33 HL7 message and extracts all the necessary information (e.g., model name, WSI identifier)
for further processing.

Author: Miriam Angeloni
E-Mail: miriam.angeloni@uk-erlangen.de
"""

import os

from pathlib import Path
from hl7apy.parser import parse_message
from hl7apy.exceptions import UnsupportedVersion


def extract_slide_id(msg_input_dict: dict,
                     list_dup_segments: list) -> list:
    """
    This function extracts slide identifier(s) from the input OML^O33 input message.

    :param msg_input_dict: stores the segments/fields of the input OML^O33 message
    :param list_dup_segments: list storing the name of possible repeated segments (e.g., OBR, ORC)
    :return: list of slide identifier(s)
    """
    if 'ORC' in list_dup_segments:
        howmany = len([key for key in list(msg_input_dict.keys()) if 'ORC' in key])
        list_str = [msg_input_dict[f"OBR_{i+1}"]["OBR_13"] for i in range(howmany)]

    else:
        list_str = [msg_input_dict["OBR"]["OBR_13"]]
        
    list_path = [Path(rf"{st}") for st in list_str]

    slide_list = [path.name for path in list_path]
    
    return slide_list
        

def extract_msg_info(hl7_input: str):
    """
    This function takes in input the OML^O33 HL7 message sent by the AP-LIS and:
    1) extracts the name of the deep-learning (DL) model to apply from the fields 4.1 or 4.2 of the SPM segment
    2) stores the content of the input message in a dictionary
    3) extracts the name(s) of the WSI(s) to process from field 13 of the OBR segment

    :param hl7_input: input OML^O33 HL7 message
    """
    
    try:
        msg_input = parse_message(hl7_input, find_groups=False)
    except UnsupportedVersion:
        msg_input = parse_message(hl7_input, find_groups=False)
    
    # Extract either from field SPM 4.1 or from field 4.2 the name of the DL model
    dl_model = msg_input.spm.spm_4.spm_4_2.value
    
    # Analyze the input OML^O33 HL7 message:
    # 1) Look for, if any, repeated segments
    str_segments = [str(segment) for segment in msg_input.children]
    str_segments = [segment.split(" ")[1].split(">")[0] for segment in str_segments]
    set_dup_segments = set([seg for seg in str_segments if str_segments.count(seg) > 1])
    list_dup_segments = list(set_dup_segments)

    # 2) Store all the fields/segments of the input HL7 message in two dictionaries:
    msg_input_dict = {}

    msg_input_dict2 = {}

    for segment in msg_input.children:
        segment_name = str(segment)
        segment_name = segment_name.split(" ")[1].split(">")[0]
        print(f"Processing segment:{segment}")
        msg_subset = {}
        for attribute in segment.children:
            field_value = attribute.value
            field_str = str(attribute)
            field = field_str.split(" ")[1]
            msg_subset[f"{field}"] = field_value
        if segment_name in list_dup_segments:
            # If the segment name is already among the keys, it means that it is a repeated segment and you have to increment the number
            # e.g. ORC_1, ORC_2, etc
            count = len([key for key in list(msg_input_dict.keys()) if segment_name in key])
            msg_input_dict[f"{segment_name}_{count+1}"] = msg_subset
            msg_input_dict2[f"{segment_name}_{count+1}"] = segment.value
        else:
            msg_input_dict[f"{segment_name}"] = msg_subset
            msg_input_dict2[f"{segment_name}"] = segment.value
        
    # List containing one slide ID if we process only one order message for patient at a time, otherwise it may contain multiple slide IDs
    slide_list = extract_slide_id(msg_input_dict, list_dup_segments)

    return dl_model, slide_list, msg_input, msg_input_dict, msg_input_dict2, list_dup_segments
