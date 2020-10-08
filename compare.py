import btk
import numpy as np

#this is a test
class compare:
    """
    les techniques de comparaison
    """
    
    def __init__(self):
        self.number_markers = 149
    
    def array_from_c3d(self, file_c3d):
        """
        Returns the array representation of a C3D file.
        """

        reader = btk.btkAcquisitionFileReader()
        reader.SetFilename(file_c3d)
        reader.Update()
        acq = reader.GetOutput()

        N = acq.GetPointFrameNumber()
        nber_points = acq.GetPointNumber()

        result = []
        points_coords = np.array([acq.GetPoint(j).GetValues()
                                  for j in range(nber_points)])
        for i in range(N):
            result.append(points_coords[:, i])
        return np.array(result)

    def prepare_datasets(self, facelift, performer):
        c1 = self.array_from_c3d(facelift)
        c2 = self.array_from_c3d(performer)
        diff = c1.shape[0] - c2.shape[0]

        if diff > 0:
            print("FaceLift's C3D file has " + str(diff) + " more frames than Performer's C3D file. We ASSUME " +
                  "they correspond to the first frames of the video that were ignored when reading Performer's C3D file, " +
                  "so we remove them from FaceLift's C3D to compute the error between the C3D files.")
            c1 = c1[diff:]
        else:
            print("no valid data")
        print("facelift: ", c1.shape[0], "performer: ", c2.shape[0])
        return c1, c2

    def face_dimension(self, c):
        """calculate the radius of the face (half of the face length)
        we table the markers 9 and 90 as references
        """
        return np.sqrt(np.sum((c[:,8,:]- c[:,89,:])**2, axis=1)) / 2
        """
        def euclidean(p1, p2):
            return np.sqrt(np.sum((p1- p2)**2))
            
        length = []
        for i in range(c.shape[0]):
            max = 0
            if i%100 == 0:
                print(i)
            for j in range(c.shape[1]):
                for k in range(j+1, c.shape[1]):
                    if euclidean(c[i,j], c[i,k]) > max:
                        max = euclidean(c[i,j], c[i,k])
            length.append(max)
        return np.array(length)
        """
        
        
    def euclidean_dist(self, c1, c2):
        """calculate the euclidean distance par marker per frames
        """
        return np.sqrt(np.sum((c1- c2)**2, axis=2))

        
    def avg_euclidean_dist_frame(self, c1, c2):
        """calculate the average euclidean distance per frames
        """
        return np.mean(self.euclidean_dist(c1, c2), axis=1)

        
    def relative_avg_euclidean_dist_frame(self, c1, c2):
        """calculate the average euclidean distance per frames
        """
        return np.clip(self.avg_euclidean_dist_frame(c1, c2) / self.face_dimension(c1) * 100, 0, 100)


    def log_avg_euclidean_dist_frame(self, c1, c2):
        """calculate the average euclidean distance per frames
        """
        return np.clip(-np.log(self.relative_avg_euclidean_dist_frame(c1, c2) / 100), 0, 10)
        
        
    def max_euclidean_dist_frame(self, c1, c2):
        """find the maximum euclidean distance per frames
        """
        return np.ndarray.max(self.euclidean_dist(c1, c2), axis=1)
        
        
    def relative_max_euclidean_dist_frame(self, c1, c2):
        """find the maximum euclidean distance per frames
        """
        return np.clip(np.ndarray.max(self.euclidean_dist(c1, c2), axis=1) / self.face_dimension(c1) * 100, 0, 100)
    
    
    def log_max_euclidean_dist_frame(self, c1, c2):
        """find the maximum euclidean distance per frames
        """
        return np.clip(-np.log(self.relative_max_euclidean_dist_frame(c1, c2) / 100), 0, 10)
        
        
    def min_euclidean_dist_frame(self, c1, c2):
        """find the minimum euclidean distance per frames
        """
        return np.ndarray.min(self.euclidean_dist(c1, c2), axis=1)
  

    def relative_min_euclidean_dist_frame(self, c1, c2):
        """find the minimum euclidean distance per frames
        """
        return np.clip(np.ndarray.min(self.euclidean_dist(c1, c2), axis=1) / self.face_dimension(c1) * 100, 0, 100)
 

    def log_min_euclidean_dist_frame(self, c1, c2):
        """find the maximum euclidean distance per frames
        """
        return np.clip(-np.log(self.relative_min_euclidean_dist_frame(c1, c2) / 100), 0, 10)


    def average_euclidean_dist(self, c1, c2):
        """find the averaged euclidean distance of all frames
        """
        return np.sum(self.avg_euclidean_dist_frame(c1, c2), axis=0) / c1.shape[0]
    
    
    def relative_average_euclidean_dist(self, c1, c2):
        """find the averaged euclidean distance of all frames
        """
        return np.clip(self.average_euclidean_dist(c1, c2) / np.mean(self.face_dimension(c1), axis=0) * 100, 0, 100)
    
    def funct():
        print('this is a test.')
    
    
    def log_average_euclidean_dist(self, c1, c2):
        """find the averaged euclidean distance of all frames
        """
        return np.clip(-np.log(self.relative_average_euclidean_dist(c1, c2) / 100), 0, 10)       
    
    
    def get_frame_seuil(self, c1, c2, seuil):
        """to get the frame whose index is under a get_frame_seuil
        """
        frames = []
        for ind, index in enumerate(self.log_avg_euclidean_dist_frame(c1, c2)):
            if index < seuil:
                frames.append(ind)
        return len(frames), frames
        
        
        
