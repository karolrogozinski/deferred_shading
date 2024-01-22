import numpy as np


class Camera:

    def __init__(self, position, eulers):
        self.position = np.array(position,dtype=np.float32)
        self.eulers = np.array(eulers,dtype=np.float32)
        self.global_up = np.array([0, 0, 1], dtype=np.float32)

    def calculate_forward(self):
        target = + np.array(
            [
                np.cos(np.radians(self.eulers[1]),dtype=np.float32) * np.cos(np.radians(self.eulers[0]),dtype=np.float32),
                np.sin(np.radians(self.eulers[1]),dtype=np.float32) * np.cos(np.radians(self.eulers[0]),dtype=np.float32),
                np.sin(np.radians(self.eulers[0]),dtype=np.float32)], 
                dtype = np.float32)

        return target

    
    def calculate_up(self):
        forward = self.calculate_forward()
        up = np.cross(a = np.cross(a = forward,b = self.global_up),b = forward,)
        
        return up
