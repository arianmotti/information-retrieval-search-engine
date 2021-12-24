# IR
information retrieval search engine
phase 1:
The purpose of this project is to create a search engine to retrieve text documents so that the user asks himself 
Enters and represents the relevant documents system.
 Preprocessing documents 
• Token extraction 
• Normalization of texts 
• Remove repeating filled words 
• Rooting 

Creating a location index for responding to user query 
 In this section, by receiving the user's query, you should be able to binary the documents related to it. 
 restore . 
The user's query can be as follows:
Single word: Just retrieve the list of documents from the dictionary.
A few words: In this section, the list of files must be sorted by the amount of communication. Most relevant document, Sandy 
It is to have all the words in the same order as the query. 
phase 2:
In this step, we want to expand the information retrieval model and represent the documents in vector
To be able to rank search results based on their relevance to the user query. So that for
Each document is extracted a numeric vector that represents that document in the vector space and these vectors are stored.
To be. At the time of receiving the query, first construct the vector corresponding to that query in the same vector space and then with
Using an appropriate similarity criterion, the numerical similarity of the query vector with the vector of all documents in the vector space is calculated
Finally, the output results are sorted by similarity.
In the above display, for a word that does not exist in a document, the weight is considered zero and from
This direction will be zero for many elements of the calculated vectors. To save memory consumption instead
Consider a complete numeric vector for each document, many of whose elements are zero
Save the words in different documents in the same mailing lists. When answering a user query that in
It is also explained that while searching for words in the mailing lists, you can find the weight of the words in the documents
Fetch the different ones as well so that only the non-zero elements of the document vectors are stored and processed
![image](https://user-images.githubusercontent.com/51990802/147371860-1910e93f-5357-4766-b9b6-2f1275c558a5.png)
![image](https://user-images.githubusercontent.com/51990802/147371870-68b10ebb-848c-4752-b275-86810f0020fc.png)

