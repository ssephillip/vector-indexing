# Vector indexing

This repository contains the code for the vector indexing service used by the new, extended version of new/s/leak that resulted from my BA thesis.\
To use the new version of new/s/leak please refer to https://github.com/ssephillip/newsleak-docker . 
<br/>
<br/>
This service provides the possibility to store vectors in a vector index and to retrieve the k-Nearest-Neighbours, given the ID of a vector in the Index. \
This functionality can be accessed via Http Requests. \
<br/>
<h2>The following endpoints are provided by this service <h2/>

### Indexing vectors
#### Endpoint: 
[baseurl]/index_vectors \
<br/>
#### Example: 
http://localhost:5000/index_vectors \
<br/>
#### Type: 
POST-Request \
<br/>
Provides the possibility to store vectors in the vector index. The existing vectors in the index will be removed. \
As parameters two files have to be provided. \
A file containing the ids of the vectors and a file containing the vectors. Both files are passed as key-value pairs. \
The key for the file containing the IDs  is "ids" and they key for the file containing the vectors is "vectors". \
The values are the files theselves. It is recommended to send the request as a Http Multipart Request. \
When using this service with newsleak, the newsleak document IDs should be used as IDs. Thereby, vectors can easily be associated with the corresponding document. \
<br/>
The files need to look as follows: \
In each file, each line must only contain one ID/vector. Also the ID and the corresponding vector must have the same line number. \
Example: \
The ID in line 5 in the files with the IDs must be the ID of the vector in line 5 in the file containing the vectors. \
<br/>
<br/>
<br/>
### Retrieve the k-Nearest Neighbours
#### Endpoint: 
[baseurl]/vectors/<ID>?num=[num of k-NN] \
<br/>
#### Example: 
http://localhost:5000/vector/7?num=10 \
<br/>
#### Type: 
GET-Request \
<br/>
Retrieves the k-Nearest-Neighbours of the vector for which an ID was provided. \
Note: The vector belonging to the specified ID is also returned as result (as the most similar vector). \
The result is returned in JSON format. It is returned as a list, where each list element is a pair of the following form: \
[vector-id,cosine_distance] \
<br/>
#### Example response: 
{"result":[[3,0.0],[15,0.013967633247375488],[16,0.017206192016601562],[13,0.018164396286010742]]}

