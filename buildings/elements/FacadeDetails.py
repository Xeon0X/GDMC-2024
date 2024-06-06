from buildings.geometry.Vertice import Vertice

class FacadeDetails:
    def __init__(self,rdata , zones : list[Vertice]):
        self.zones = zones
        self.sizes = self.get_sizes()
        
    def get_sizes(self) -> list[tuple[int]]:
        # foreach different zone sizes in self.zones, we will gen different details
        sizes = []
        center_for_symetry = len(self.zones) // 2
        for zone in self.zones:
            size = zone.point2.position - zone.point1.position
            if size not in sizes :
                sizes.append(size)
                
        return sizes
    
    