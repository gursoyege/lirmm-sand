from common.imports import *
from module import sequence_generator

# Clean
#sequence_generator.clean()

# Run
#sequence_generator.run()

x=np.load("loss.npy")
from matplotlib import pyplot as plt
fig = plt.figure()
plt.plot(x)
plt.xlabel("epoch")
plt.ylabel("loss")
plt.show()
fig.savefig("loss.png")