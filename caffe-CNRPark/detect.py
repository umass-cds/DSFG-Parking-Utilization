import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import caffe
import sys

caffe.set_mode_cpu()

#load the model
net = caffe.Net('trained-models/mLeNet-on-CNRParkA/deploy.prototxt',
                'trained-models/mLeNet-on-CNRParkA/snapshot_iter_2910.caffemodel',
                caffe.TEST)

blob = caffe.proto.caffe_pb2.BlobProto()
data = open( 'trained-models/mLeNet-on-CNRParkA/mean.binaryproto', 'rb' ).read()
blob.ParseFromString(data)
arr = np.array( caffe.io.blobproto_to_array(blob) )
outarr = arr[0]

# load input and configure preprocessing
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_mean('data', outarr.mean(1).mean(1))
transformer.set_transpose('data', (2,0,1))
transformer.set_channel_swap('data', (2,1,0))
transformer.set_raw_scale('data', 255.0)

#note we can change the batch size on-the-fly
#since we classify only one image, we change batch size from 10 to 1
net.blobs['data'].reshape(1,3,224,224)

#load the image in the data layer
# standardize colors if issues with color/sizing
# img = Image.open('dataset/cnrpark/A/busy/20150703_0925_13.jpg').convert('RGB')
# img.save('/home/sarim/Desktop/myphoto.jpg', 'JPEG')

im = caffe.io.load_image(sys.argv[1])

net.blobs['data'].data[...] = transformer.preprocess('data', im)

#compute
out = net.forward()

# other possibility : out = net.forward_all(data=np.asarray([transformer.preprocess('data', im)]))

#predicted predicted class
print("Class:" + str(out['prob'].argmax()))

#print predicted labels
labels = np.loadtxt("trained-models/mLeNet-on-CNRParkA/labels-name.txt", str, delimiter='\t')
top_k = net.blobs['prob'].data[0].flatten().argsort()[-1:-6:-1]
print(labels[top_k])
print(net.blobs['prob'].data[0])