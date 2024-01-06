import os
import time

import pandas as pd
from openai import OpenAI


client = OpenAI(api_key="")

#
def change_api_key(api_key_new):
    global client
    client = OpenAI(api_key=api_key_new)


def get_answer(question):
    error_count = 0
    if error_count > 10:
        return None
    try:
        start_time = time.time()
        message_response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "user", "content": question}
            ],
            temperature=0.7,
        )
        end_time = time.time()
        processing_time = end_time - start_time

        return message_response.choices[0].message.content, processing_time
    except Exception as e:
        print(e)
        time.sleep(20)
        return get_answer(question)


class Data:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def __str__(self):
        return self.question + ' ' + self.answer


def process_data(filename):
    df = pd.read_csv(filename)
    time_process_count = 0
    if 'question' not in df.columns:
        return
    if 'answer' not in df.columns:
        df['answer'] = None
    for index, row in df.iterrows():
        question = row['question']
        answer = row['answer']
        if pd.isnull(answer) or answer == "":
            print("Processing question: " + question)
            answer, processing_time = get_answer(question)
            time_process_count = time_process_count + processing_time
            df['answer'] = df['answer'].astype(str)
            df.at[index, 'answer'] = str(answer)  # Explicitly cast to string
            df.to_csv(filename, index=False)
            print("Answer: " + answer)
            df.to_csv(filename, index=False, encoding='utf-8-sig')

    # Save the updated DataFrame to the same file


def read_all_key_from_csv():
    df = pd.read_csv('key.csv')
    list_key = df['key'].tolist()
    return list_key


def scan_all_file_csv():
    folder_data = 'data'
    for filename in os.listdir(folder_data):
        process_data(os.path.join(folder_data, filename))


if __name__ == '__main__':
    list_key = read_all_key_from_csv()
   


