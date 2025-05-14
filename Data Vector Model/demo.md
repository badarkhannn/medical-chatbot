## Getting Started

To run this project locally and set up your own vector-based search using Pinecone, follow these steps:

### Run the Notebook

Open and run the `demo.ipynb` file. This notebook handles:

- Downloading the required model to your local machine.
- Processing the source document.
- Creating and querying the vector database.

> ⚠️ Make sure all required dependencies are installed. You can use a virtual environment and run:
> ```bash
> pip install -r requirements.txt
> ```

---

### Set Up Pinecone

To store and manage the vector embeddings, you'll need a Pinecone account.

#### Steps:

1. Go to [Pinecone.io](https://www.pinecone.io/) and **create a free account**.
2. After logging in, navigate to your Pinecone **API key dashboard**.
3. Copy your **API Key** and **Environment**.
4. Add them in the notebook or set as environment variables:
   ```python
   import os
   os.environ["PINECONE_API_KEY"] = "your-api-key-here"
   os.environ["PINECONE_ENVIRONMENT"] = "your-environment-here"
