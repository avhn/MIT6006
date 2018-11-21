import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):
        raise NotImplemented

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
