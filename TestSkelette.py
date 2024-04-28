import numpy as np
from skimage.morphology import skeletonize
import matplotlib.pyplot as plt

# Créer un tableau de booléens
image = np.ones((20, 20), dtype=bool)
image[1:-1, 1:-1] = True

# Effectuer la squelettisation
skeleton = skeletonize(image)

# Afficher les résultats
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4), sharex=True, sharey=True)

ax = axes.ravel()

ax[0].imshow(image, cmap=plt.cm.gray)
ax[0].axis('off')
ax[0].set_title('original', fontsize=20)

ax[1].imshow(skeleton, cmap=plt.cm.gray)
ax[1].axis('off')
ax[1].set_title('skeleton', fontsize=20)

fig.tight_layout()
plt.show()