# Import necessary libraries
import torch
from transformers import AutoTokenizer,  AutoModelForQuestionAnswering, AutoModel
import numpy as np
from scipy.spatial.distance import cosine
import torch

class Summarizer:
    def __init__(self, model_name) -> None:
        
        # Specify the pretrained model you want to use
        self.model_name = model_name

        self.model = AutoModelForQuestionAnswering.from_pretrained(self.model_name) #used for answering
        self.model_vec = AutoModel.from_pretrained(self.model_name) #used for vectorization
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name) #used for tokenization

    def split_context(self, context, overlap=50, max_length=512):
        """
        Function for splitting context into overlapping chunks.
        
        param context: This is the text that you want to split into chunks. 
        The function will split this text based on the max_length and overlap parameters.

        param overlap (default=50): This is the number of characters that will overlap between each chunk. 
        This is used to ensure that the context is not cut off in the middle of a sentence, which could make the text difficult to understand.

        param max_length (default=512): This is the maximum length of each chunk. 
        The function will split the context into chunks of this length, with the exception of the last chunk, which may be shorter.

        The function returns a list of chunks, where each chunk is a string of text from the context. 
        The chunks are created by starting at the beginning of the context and moving forward max_length
        characters at a time, with an overlap of overlap characters between each chunk.
        """
        
        chunks = []
        start = 0
        while start < len(context):
            end = min(start + max_length, len(context))
            chunks.append(context[start:end])
            if end == len(context):
                break
            start = end - overlap
        return chunks


    def answer_question(self, context, question):
        """
        The function answers questions given context and question.
        
        model: This is the model that you're using to generate answers to the questions. 
        It could be any model that's capable of question answering, such as a transformer model.

        param  tokenizer: This is the tokenizer that corresponds to your model. 
        It's used to convert your text data into a format that the model can understand.

        param context: This is the text that the model will look at to find an answer to the question.

        param question: This is the question that you're asking the model. 
        The model will generate an answer to this question based on the context.

        The function returns an answer to the question based on the context. 
        The answer is generated by finding the tokens with the highest start and end scores, 
        and joining them together. If the end score is higher than the start score, 
        they are swapped to ensure the answer makes sense.
        """

        # print("conetext", context)

        # print("Q", question)

        # Encode the context and question
        encoded = self.tokenizer.encode_plus(question, context, truncation=True, padding='max_length', max_length=512, return_tensors='pt')

        # Get the start and end scores for all tokens
        result = self.model(**encoded)
        start_scores = result["start_logits"]
        end_scores = result["end_logits"]

        # Find the tokens with the highest start and end scores
        answer_start = torch.argmax(start_scores)
        answer_end = torch.argmax(end_scores)

        # If the end score is higher than the start score, swap them
        if answer_end < answer_start:
            answer_start, answer_end = answer_end, answer_start

        # Get the tokens for the answer
        all_tokens = self.tokenizer.convert_ids_to_tokens(encoded['input_ids'][0])
        answer = ' '.join(all_tokens[answer_start : answer_end+1])

        return answer


    def vectorize_text(self, input_string):
        """
        Vectorize a given input string.
        
        param model: This is the model used to encode the input string and get the output. 
        It could be any model that's capable of encoding text, such as a transformer model.

        param tokenizer: This is the tokenizer that corresponds to your model. 
        It's used to convert your text data into a format that the model can understand.

        param input_string: This is the text that you want to vectorize. 
        The function will convert this text into a numerical representation that 
        can be processed by the machine learning model.

        The function returns a vector representation of the input string. 
        This vector is obtained by averaging the embeddings from the last hidden 
        state of the model's output.
        """
        # Encode the input string
        inputs = self.tokenizer.encode_plus(
            input_string,
            add_special_tokens=True,
            return_tensors="pt"
        )

        # Get the output from the model
        outputs = self.model(**inputs)

        # Get the embeddings from the last hidden state
        embeddings = outputs.last_hidden_state

        # Average the embeddings
        vector = torch.mean(embeddings, dim=1)

        # Convert tensor to numpy array
        vector = vector.detach().numpy()

        return vector


    def calculate_similarity(question_vector, answer_vector):
        """Calculate the cosine similarity between the question and answer vectors.
        
        param question_vector: This is the vector representation of the question. 
        It's obtained by transforming the question text into numerical data that 
        can be processed by the machine learning model.

        param answer_vector: This is the vector representation of the answer. 
        It's obtained by transforming the answer text into numerical data that 
        can be processed by the machine learning model.

        The function calculates and returns the cosine similarity between the 
        question and answer vectors. Cosine similarity is a measure of similarity 
        between two non-zero vectors of an inner product space that measures the 
        cosine of the angle between them. The closer the cosine similarity to 1, 
        the more similar the question and answer are.
        """

        similarity = 1 - cosine(question_vector[0], answer_vector[0])

        return similarity


    def find_best_answer(self, context, question, model_vec, num_answers=3, overlap=50, max_length=512):
        """Find the best answers to the question given a long context
        param model: This is the model that you're using to generate answers to the questions. 
        It could be any model that's capable of question answering, such as a transformer model.

        param tokenizer: This is the tokenizer that corresponds to your model.
        It's used to convert your text data into a format that the model can understand.

        param context: This is the text that the model will look at to find an answer to the question. 
        In this case, it's a long text that's split into chunks.

        param question: This is the question that you're asking the model. 
        The model will generate an answer to this question based on the context.

        param model_vec: This is a model used to vectorize the text, 
        i.e., convert the text into numerical data that can be processed by the machine learning model.

        param num_answers (default=3): This is the number of best answers the function will return.

        param overlap (default=50): This is the number of overlapping words between 
        two consecutive chunks when the context is split into chunks.

        param max_length (default=512): This is the maximum length of each chunk. 
        The context is split into chunks of this length.

        The function returns a list of tuples, where each tuple contains an answer 
        and its similarity score. The list is sorted in ascending order of similarity, 
        so the first element of the list is the answer with the lowest similarity, 
        and the last element is the answer with the highest similarity.
            
        """
        # Vectorize the question
        question_vector = self.vectorize_text(model_vec, self.tokenizer, question)
        
        # Initialize the best answers and their similarities to the question
        best_answers = [(None, -1) for _ in range(num_answers)]
        
        # Split the context into chunks
        chunks = self.split_context(context, overlap, max_length)
        
        # Generate an answer for each chunk and update the best answers if necessary
        for chunk in chunks:
            answer = self.answer_question(self.model, self.tokenizer, chunk, question)
            if answer is not None:
                answer_vector = self.vectorize_text(model_vec, self.tokenizer, answer)
                if answer_vector is not None:
                    similarity = self.calculate_similarity(question_vector, answer_vector)
                    # Check if the similarity is higher than the current lowest in best_answers
                    if similarity > best_answers[0][1]:
                        # Replace the lowest
                        best_answers[0] = (answer, similarity)
                        # Sort the list so the lowest similarity is first
                        best_answers = sorted(best_answers, key=lambda x: x[1])
        # Return the answers along with their similarities
        return best_answers


    def parse_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        return content


    def run(self, input_file):
        # Ask the user for input
        user_input = input("Enter your question: ")
        log_file = self.parse_file(input_file)
        # log_file = """
        #         INFO - 2022-01-01 00:00:01,234 - Connection established.
        #         INFO - 2022-01-01 00:00:02,345 - Sending request to server.
        #         ERROR - 2022-01-01 00:00:03,456 - Failed to establish a new connection: [Errno 11001] getaddrinfo failed.
        #         INFO - 2022-01-01 00:00:04,567 - Connection closed.
        #         INFO - 2022-01-01 00:00:05,678 - Attempting to reconnect.
        #         INFO - 2022-01-01 00:00:06,789 - Connection established.
        #         INFO - 2022-01-01 00:00:07,890 - Sending request to server.
        #         INFO - 2022-01-01 00:00:08,901 - Server response received.
        #         INFO - 2022-01-01 00:00:09,012 - Processing server response.
        #         ERROR - 2022-01-01 00:00:10,123 - Error while processing server response: Unexpected token.
        #         INFO - 2022-01-01 00:00:11,234 - Connection closed.
        #         """
        best_answer = self.answer_question(log_file, user_input)
        print(f"The best answer is: {best_answer}")

if __name__ == "__main__":
    summarizer = Summarizer("bert-large-uncased-whole-word-masking-finetuned-squad")
    summarizer.run('/home/hackathon26/omar/hackatum23-coinflip/data/test_log1.out')