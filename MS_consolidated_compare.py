import csv
import yaml
import argparse
from datetime import datetime, timezone
import json
import base64
import requests
import hashlib
import uuid
import hmac
from openpyxl import load_workbook
from cryptography.fernet import Fernet
import sseclient
from tqdm import tqdm
from time import perf_counter_ns
import pandas as pd
import json
import csv
from sklearn.metrics import f1_score
import torch
from conva_ai.response import ConvaAIResponse
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.utils.multiclass import unique_labels
from tqdm import tqdm 
import numpy as np


tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-large-en-v1.5', truncation=True)
model = AutoModel.from_pretrained('BAAI/bge-large-en-v1.5')

def compute_cosine_similarity(true_values, predicted_values):
  true_encoding = tokenizer(true_values, return_tensors='pt', truncation=True)
  predicted_encoding = tokenizer(predicted_values, return_tensors='pt', truncation=True)

  with torch.no_grad():
    true_output = model(**true_encoding).last_hidden_state.mean(dim=1)
    predicted_output = model(**predicted_encoding).last_hidden_state.mean(dim=1)

  similarity = cosine_similarity(true_output, predicted_output)
  return similarity[0][0]

def compare_csv_files(file1, file2, output_file):
   
    # Read data from the first CSV file into a list
    with open(file1, 'r', newline='') as csv_file1:
        csv_reader1 = csv.reader(csv_file1)
        data1 = list(csv_reader1)
    
    # Read data from the second CSV file into a list
    with open(file2, 'r', newline='') as csv_file2:
        csv_reader2 = csv.reader(csv_file2)
        data2 = list(csv_reader2)
    
    columns_to_compare = [0,2,3,4,5,6,7,8,9,10]
    # Assuming both data1 and data2 are lists of lists where each inner list represents a row
    mismatched_columns = []
    for index in range(min(len(data1), len(data2))):
        row3 = []
        row1 = data1[index]
        row2 = data2[index]
        score = [0.0] * 11
        for col_index in columns_to_compare:
                flag=0
                if ',' in row1[col_index]:
                    list1 = [i.strip("[]' ").lower() for i in row1[col_index].split(',')]
                else:
                    list1 = [row1[col_index]]
            
                if ',' in row2[col_index]:
                    list2 = [i.strip("[]' ").lower() for i in row2[col_index].split(',')]
                else:
                    list2 = [row2[col_index]]

                if col_index == 5:
                    for i in list2:
                        for j in list1:
                            if j.lower() in i.lower():
                                flag=1
                                score[col_index] = 1
                                break

                else: #cousine similaritu
                    for i in list2:
                        for j in list1:
                            x = compute_cosine_similarity(i.lower(), j.lower())
                            if x >= 0.5 and x <= 2.0:
                                score[col_index] =1
                                flag=1
                                break
                            else:
                                score[col_index] = x
                    
                if flag == 0:
                    row3 = [row2[0], row2[2], row1[3], row2[3], score[3], row1[4], row2[4], score[4], row1[5], row2[5], score[5], row1[6], row2[6], score[6], row1[7], row2[7], score[7], row1[8], row2[8], score[8], row1[9], row2[9], score[9], row1[10], row2[10], score[10]]
                    mismatched_columns.append(row3)
                    print("Actual row : ", [row2[1]], " ", list2)
                    print("Expected row : ", row1[1], " ", list1)
                    break
     # Write the mismatched rows to the output CSV file
    with open(output_file, 'w', newline='') as output_csv:
        csv_writer = csv.writer(output_csv)
        csv_writer.writerow(
            ["Assistant_name", "input_query", "message", "Expected_message", "message_score", "related_queries", "Expected_related_queries_score", "related_queries_score", "tool_name", "Expected_tool_name", "tool_name_score", "reason", "Expected_reason", "reason_score", "steps", "Expected_steps", "steps_score","api_response", "Expected_api_response", "api_response_score", "citations", "Expected_citations", "citations_score","parameters", "Expected_parameters", "parameters_score"]
        )
        csv_writer.writerows(mismatched_columns)        

    


compare_csv_files("/Users/divyac/Downloads/consolidated_prompts_prod_18.csv", "/Users/divyac/Downloads/FAQ Golden dataset - Consolidated_golden_dataset.csv", "/Users/divyac/Downloads/prompts_compare_result19nov2024.csv")

#  To run
#  /Users/divyac/Documents/Notebooks/my_env/bin/python /Users/divyac/Documents/Notebooks/MS_consolidated_compare.py