
import nmslib
import numpy
from flask import Flask, request, jsonify
from pathlib import Path

app = Flask(__name__)

#This service provides the possibility to store vectors in a vector index and to retrieve the k-Nearest-Neighbours, given the ID of a vector in the Index.
#This functionality can be accessed via Http Requests.
#
#The following endpoints are provided by this service:
#
#Indexing vectors:
#Endpoint:
#[baseurl]/index_vectors
#
#Example:
#http://localhost:5000/index_vectors
#
#Type: POST-Request
#
#Provides the possibility to store vectors in the vector index.
#The existing vectors in the index will be removed.
#As parameters two files have to be provided.
#A file containing the ids of the vectors and a file containing the vectors.
#Both files are passed as key-value pairs.
#The key is "ids" for the file containing the IDs and "vectors" for the file containing the vectors.
#The values are the files theselves. It is recommended to send the request as a Http Multipart Request.
#When using this service with newsleak, the newsleak document IDs should be used as IDs. 
#Thereby, vectors can easily be associated with the corresponding document.
#
#The files need to look as follows:
#In each file, each line must only contain one ID/vector.
#Also the ID and the corresponding vector must have the same line number.
#Example: 
#The ID in line 5 in the files with the IDs must be the ID of the vector in line 5 in the file containing the vectors.
#
#
#
#Retrieve the k-Nearest-Neighbours:
#Endpoint:
#[baseurl]/vectors/<ID>?num=[num of k-NN]
#
#Example:
#http://localhost:5000/vector/7?num=10
#
#Type: GET-Request
#
#Retrieves the k-Nearest-Neighbours of the vector for which an ID was provided.
#Note: The vector belonging to the specified ID is also returned as result (as the most similar vector).
#The result is returned in JSON format. It is returned as a list, where each list element is a pair of the following form:
#[vector-id,cosine_distance]
#
#Example list item:
#[5,0.32432] 
#
#Example response:
#{"result":[[3,0.0],[15,0.013967633247375488],[16,0.017206192016601562],[13,0.018164396286010742]]}


class Indexer:
    index_file_name = "index_optim.bin"
    id_file_name = "vector_ids.txt"
    data_file_name = "vectors.txt"
    index = None
    id_to_vector_map = None


    def __init__(self):
        index_file = Path(self.index_file_name)
        id_file = Path(self.id_file_name)
        vector_file = Path(self.data_file_name)
        self.index = nmslib.init(method='hnsw', space='l2')

        if index_file.is_file() and id_file.is_file() and vector_file.is_file() :
            self.index.loadIndex(self.index_file_name, load_data=True)
            ids = numpy.loadtxt(self.id_file_name, dtype = numpy.int)
            vectors = numpy.loadtxt(self.data_file_name)
            self.id_to_vector_map = dict(zip(ids, vectors))


    def example(self):
        return 'Server Works!'

    
    def index_vectors(self):

        vector_file = request.files['vectors']
        id_file = request.files['ids']


        vector_file.save(self.data_file_name)
        id_file.save(self.id_file_name)


        data_matrix = numpy.loadtxt(self.data_file_name)
        ids = numpy.loadtxt(self.id_file_name, dtype=numpy.int)
        self.id_to_vector_map = dict(zip(ids, data_matrix))
        print("num of vectors arrived:")
        print(len(self.id_to_vector_map))



        self.index = nmslib.init(method='hnsw', space='cosinesimil')
        self.index.addDataPointBatch(data_matrix, ids)
        self.index.createIndex({'post': 2}, print_progress=True)
        self.index.saveIndex('index_optim.bin', save_data=True)

        return "OK"


    
    def get_vector(self, id):
        num_of_NN = int(request.args.get('num'))
        print(num_of_NN)
        vector = self.id_to_vector_map[id]
        ids, distances = self.index.knnQuery(vector, k=num_of_NN)
        ids = list(map(int, ids))               #maps int32 to int
        distances = list(map(float, distances)) #maps float32 to float
        print("found vectors: ", len(ids))
        results = list(zip(ids, distances))

        return jsonify(result=results)




indexerObject = Indexer()

@app.route('/')
def example():
    return indexerObject.example()

@app.route('/index_vectors', methods=['POST'])
def index_vectors():
    return indexerObject.index_vectors()


@app.route('/vector/<int:id>')
def get_vector(id):
    response = indexerObject.get_vector(id)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(port='5003', debug=True)





