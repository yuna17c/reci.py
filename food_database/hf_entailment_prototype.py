import boto3
import transformers
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import nltk
import pandas as pd
import numpy as np
#nltk.download('punkt')

transformers.logging.set_verbosity_error()

if __name__ == '__main__':

    # Setting up client and accessing documents in /txt sub-folder in bucket
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')
    result = s3_client.list_objects_v2(Bucket='', Prefix='txt/') #add in bucket later
    all_documents = []

    for item in result['Contents']:
        files = item['Key']
        all_documents.append(files)

    # Model + Tokenizer
    hg_model_hub_name = "ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli"
    # some other models to consider
    # hg_model_hub_name = "ynie/albert-xxlarge-v2-snli_mnli_fever_anli_R1_R2_R3-nli"
    # hg_model_hub_name = "ynie/bart-large-snli_mnli_fever_anli_R1_R2_R3-nli"
    # hg_model_hub_name = "ynie/electra-large-discriminator-snli_mnli_fever_anli_R1_R2_R3-nli"
    # hg_model_hub_name = "ynie/xlnet-large-cased-snli_mnli_fever_anli_R1_R2_R3-nli"

    tokenizer = AutoTokenizer.from_pretrained(hg_model_hub_name)
    model = AutoModelForSequenceClassification.from_pretrained(hg_model_hub_name)

    # List of compliance questions
    questions = [
        "This item is a fruit.",
        "This item is a vegetable.",
        "This item is a meat product.",
        "This item is a dairy product."
    ]

    # Creating CSV
    data = {'Document': [],
            'Question/Premise': [],
            'Sentence': [],
            'Entailment': [],
            'Neutral': [],
            'Contradiction': []
            }

    df = pd.DataFrame(data, columns=['Document', 'Question/Premise', 'Sentence',
                                     'Entailment', 'Neutral', 'Contradiction'])

    # Updating CSV for sample of documents
    for document in all_documents[1:20]:
        content_object = s3.Object(#bucket, document)
        content = content_object.get()['Body'].read().decode('utf-8')
        sentences = nltk.sent_tokenize(content)

        for premise in questions:
            for hypothesis in sentences:
                # TODO: Make this one tokenizer call later on
                tokenized_input_seq_pair = tokenizer.encode_plus(premise, hypothesis, max_length=128,
                                                                 return_token_type_ids=True, truncation=True)

                input_ids = torch.Tensor(tokenized_input_seq_pair['input_ids']).long().unsqueeze(0)
                # remember bart doesn't have 'token_type_ids', remove the line below if you are using bart.
                token_type_ids = torch.Tensor(tokenized_input_seq_pair['token_type_ids']).long().unsqueeze(0)
                attention_mask = torch.Tensor(tokenized_input_seq_pair['attention_mask']).long().unsqueeze(0)

                outputs = model(input_ids,
                                attention_mask=attention_mask,
                                token_type_ids=token_type_ids,
                                labels=None)

                # Note:
                # "id2label": {
                #     "0": "entailment",
                #     "1": "neutral",
                #     "2": "contradiction"
                # },

                predicted_probability = torch.softmax(outputs[0], dim=1)[0].tolist()  # batch_size only one
                # if predicted_probability[1]<0.5:
                #     print("{}--{}".format(premise,hypothesis))


                if not content:
                    break
                df = df.append({'Document': document,
                                'Question/Premise': premise,
                                'Sentence': hypothesis,
                                'Entailment': '{:0.3f}'.format(predicted_probability[0]),
                                'Neutral': '{:0.3f}'.format(predicted_probability[1]),
                                'Contradiction': '{:0.3f}'.format(predicted_probability[2])
                                },
                               ignore_index=True)

    df.to_csv("entailment-output.csv", index=False)


