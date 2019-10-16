
import nmslib
import numpy
from flask import Flask, request, jsonify
from pathlib import Path

app = Flask(__name__)




class Indexer:
    index_file_name = "index_optim.bin"
    id_file_name = "vector_ids.txt"
    data_file_name = "vectors.txt"
    index = None
    id_to_vector_map = None


    def __init__(self):
        print("juhuu")
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

    #@app.route('/index_vectors', methods=['POST'])
    def index_vectors(self):
        vector_file = request.files['vectors']
        vector_file.save(self.data_file_name)
        id_file = request.files['ids']
        id_file.save(self.id_file_name)


        data_matrix = numpy.loadtxt(self.data_file_name)
        ids = numpy.loadtxt(self.id_file_name, dtype=numpy.int)
        self.id_to_vector_map = dict(zip(ids, data_matrix))
        print("num of vectors arrived:")
        print(len(self.id_to_vector_map))



        self.index = nmslib.init(method='hnsw', space='l2')
        self.index.addDataPointBatch(data_matrix, ids)
        self.index.createIndex({'post': 2}, print_progress=True)
        self.index.saveIndex('index_optim.bin', save_data=True)

        return "OK"


    #@app.route('/vector/<int:id>')
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





