 for i in range(-1, width+1):
                for j in range(-1, depth+1):
                    if width<depth:
                        if width%2 != 0:
                            if (i == width//2 ):
                                self.editor.placeBlock((x + i, self.coordinates_max[1]+n, z + j), Block("blackstone_slab",{"type":"bottom"}))
                                self.grid3d[ x_plan3d+i, height+n,  z_plan3d+j] = True
                                if j== -1 :
                                    if not self.grid3d[ x_plan3d+i, height+n,  z_plan3d+j-1]:
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+n, z + j-1), Block("quartz_slab",{"type":"bottom"}))
                                        self.grid3d[ x_plan3d+i, height+n,  z_plan3d+j-1] = True
                                    if not self.grid3d[ x_plan3d+i, height+n-1,  z_plan3d+j-1]:
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+n-1, z + j-1), Block("quartz_slab",{"type":"top"}))
                                        self.grid3d[ x_plan3d+i, height+n-1,  z_plan3d+j-1] = True

                                elif j == depth:
                                    if not self.grid3d[ x_plan3d+i, height+n,  z_plan3d+j+1]:
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+n, z + j+1), Block("quartz_slab",{"type":"bottom"}))
                                        self.grid3d[ x_plan3d+i, height+n,  z_plan3d+j+1] = True
                                    if not self.grid3d[ x_plan3d+i, height+n-1,  z_plan3d+j+1]:
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+n-1, z + j+1), Block("quartz_slab",{"type":"top"}))
                                        self.grid3d[ x_plan3d+i, height+n-1,  z_plan3d+j+1] = True
                                
                    else:
                        if depth%2 != 0:
                            if (j == depth//2 ):
                                self.editor.placeBlock((x + i, self.coordinates_max[1]+n, z + j), Block("blackstone_slab",{"type":"bottom"}))
                                self.grid3d[ x_plan3d+i, height+n,  z_plan3d+j] = True
                                if i== -1 :
                                    if not self.grid3d[ x_plan3d+i-1, height+n,  z_plan3d+j]:
                                        self.editor.placeBlock((x + i-1, self.coordinates_max[1]+n, z + j), Block("quartz_slab",{"type":"bottom"}))
                                        self.grid3d[ x_plan3d+i-1, height+n,  z_plan3d+j] = True
                                    if not self.grid3d[ x_plan3d+i-1, height+n-1,  z_plan3d+j]:
                                        self.editor.placeBlock((x + i-1, self.coordinates_max[1]+n-1, z + j), Block("quartz_slab",{"type":"top"}))
                                        self.grid3d[ x_plan3d+i-1, height+n-1,  z_plan3d+j] = True
                                    
                                elif i == width:
                                    if not self.grid3d[ x_plan3d+i+1, height+n,  z_plan3d+j]:
                                        self.editor.placeBlock((x + i+1, self.coordinates_max[1]+n, z + j), Block("quartz_slab",{"type":"bottom"}))
                                        self.grid3d[ x_plan3d+i+1, height+n,  z_plan3d+j] = True
                                    if not self.grid3d[ x_plan3d+i+1, height+n-1,  z_plan3d+j]:
                                        self.editor.placeBlock((x + i+1, self.coordinates_max[1]+n-1, z + j), Block("quartz_slab",{"type":"top"}))
                                        self.grid3d[ x_plan3d+i+1, height+n-1,  z_plan3d+j] = True
                                
            if width<depth:
                
                    h = 0
                    for i in range(-1, width//2):
                        for j in range(-1, depth+1):
                            if i != -1:
                                if h % 1 == 0:
                                    self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j), Block("blackstone_slab",{"type":"top"}))
                                    self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j), Block("blackstone_slab",{"type":"top"}))
                                    self.grid3d[ x_plan3d+ i, round(height+h),  z_plan3d+ j] = True 
                                    self.grid3d[ x_plan3d+ width-1-i, round(height+h),  z_plan3d+ j] = True
                                   
                                    if j == -1 :
                                        
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j -1), Block("quartz_block"))
                                        self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j -1), Block("quartz_block"))
                                        self.grid3d[ x_plan3d+ i, round(height+h),  z_plan3d+ j-1] = True
                                        self.grid3d[ x_plan3d+ width-1-i, round(height+h),  z_plan3d+ j-1] = True
                                    elif j == depth:
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j +1), Block("quartz_block"))
                                        self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j +1), Block("quartz_block"))
                                        self.grid3d[ x_plan3d+ i, round(height+h),  z_plan3d+ j+1] = True
                                        self.grid3d[ x_plan3d+ width-1-i, round(height+h),  z_plan3d+ j+1] = True
                                else:
                                    self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j), Block("blackstone_slab",{"type":"bottom"}))
                                    self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j), Block("blackstone_slab",{"type":"bottom"}))
                                    self.editor.placeBlock((x + i, self.coordinates_max[1]+h-0.5, z + j), Block("C"))
                                    self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h-0.5, z + j), Block("blackstone"))
                                    
                                    self.grid3d[ x_plan3d+ i, round(height+h+0.5),  z_plan3d+ j] = True
                                    self.grid3d[ x_plan3d+ width-1-i, round(height+h+0.5),  z_plan3d+ j] = True
                                    self.grid3d[ x_plan3d+ i, round(height+h-0.5),  z_plan3d+ j] = True
                                    self.grid3d[ x_plan3d+ width-1-i, round(height+h-0.5),  z_plan3d+ j] = True
                                    
                                    if j == -1 :
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j -1), Block("quartz_slab", {"type": "bottom"}))
                                        self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j -1), Block("quartz_slab", {"type": "bottom"}))
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+h-1, z + j -1), Block("quartz_slab", {"type": "top"}))
                                        self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h-1, z + j -1), Block("quartz_slab", {"type": "top"}))
                                        
                                        self.grid3d[ x_plan3d+ i, round(height+h-1),  z_plan3d+ j-1] = True
                                        self.grid3d[ x_plan3d+ width-1-i, round(height+h-1),  z_plan3d+ j-1] = True
                                        self.grid3d[ x_plan3d+ i, round(height+h),  z_plan3d+ j-1] = True
                                        self.grid3d[ x_plan3d+ width-1-i, round(height+h),  z_plan3d+ j-1] = True
                                    elif j == depth:
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j +1), Block("quartz_slab", {"type": "bottom"}))
                                        self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j +1), Block("quartz_slab", {"type": "bottom"}))
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+h-1, z + j +1), Block("quartz_slab", {"type": "top"}))
                                        self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h-1, z + j +1), Block("quartz_slab", {"type": "top"}))
                                        
                                        self.grid3d[ x_plan3d+ i, round(height+h-1),  z_plan3d+ j+1] = True
                                        self.grid3d[ x_plan3d+ width-1-i, round(height+h-1),  z_plan3d+ j+1] = True
                                        self.grid3d[ x_plan3d+ i, round(height+h),  z_plan3d+ j+1] = True
                                        self.grid3d[ x_plan3d+ width-1-i, round(height+h),  z_plan3d+ j+1] = True
                            else:  
                                self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j), Block("blackstone_slab",{"type":"bottom"}))
                                self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j), Block("blackstone_slab",{"type":"bottom"})) 
                                
                                self.grid3d[ x_plan3d+ i, round(height+h),  z_plan3d+ j] = True
                                self.grid3d[ x_plan3d+ width-1-i, round(height+h),  z_plan3d+ j] = True

                                if j == -1 :
                                    self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j -1), Block("quartz_slab", {"type": "bottom"}))
                                    self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j -1), Block("quartz_slab", {"type": "bottom"}))
                                    if not self.grid3d[ x_plan3d+i, height+h-1,  z_plan3d+j-1]:
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+h-1, z + j -1), Block("quartz_slab", {"type": "top"}))
                                        self.grid3d[ x_plan3d+i, height+h-1,  z_plan3d+j-1] = True
                                    if not self.grid3d[ x_plan3d+width-1-i, height+h-1,  z_plan3d+j-1]:
                                        self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h-1, z + j -1), Block("quartz_slab", {"type": "top"}))
                                        self.grid3d[ x_plan3d+width-1-i, height+h-1,  z_plan3d+j-1] = True
                                    
                                    self.grid3d[ x_plan3d+ i, round(height+h-1),  z_plan3d+ j-1] = True
                                    self.grid3d[ x_plan3d+ width-1-i, round(height+h-1),  z_plan3d+ j-1] = True
                                elif j == depth:
                                    self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j +1), Block("quartz_slab", {"type": "bottom"}))
                                    self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j +1), Block("quartz_slab", {"type": "bottom"}))
                                    if not self.grid3d[ x_plan3d+i, height+h-1,  z_plan3d+j+1]:
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+h-1, z + j +1), Block("quartz_slab", {"type": "top"}))
                                        self.grid3d[ x_plan3d+i, height+h-1,  z_plan3d+j+1] = True
                                    if not self.grid3d[ x_plan3d+width-1-i, height+h-1,  z_plan3d+j+1]:
                                        self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h-1, z + j +1), Block("quartz_slab", {"type": "top"}))
                                        self.grid3d[ x_plan3d+width-1-i, height+h-1,  z_plan3d+j+1] = True
                                    
                                    self.grid3d[ x_plan3d+ i, round(height+h-1),  z_plan3d+ j+1] = True 
                                    self.grid3d[ x_plan3d+ width-1-i, round(height+h-1),  z_plan3d+ j+1] = True
                        if i != -1:
                            h += 0.5
            else:
            
                    h = 0
                    for i in range(-1, depth//2):
                        for j in range(-1, width+1):
                            if i != -1:
                                if h % 1 == 0:  
                                    self.editor.placeBlock((x + j, self.coordinates_max[1]+h, z + i), Block("blackstone_slab",{"type":"top"}))
                                    self.editor.placeBlock((x + j, self.coordinates_max[1]+h, z + depth-1-i), Block("blackstone_slab",{"type":"top"}))
                                    
                                    self.grid3d[ x_plan3d+j, round(height+h), z_plan3d+ i] = True
                                    self.grid3d[ x_plan3d+j, round(height+h), z_plan3d+ depth-1-i] = True
                                    
                                    if j == -1 :
                                        self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h, z + i ), Block("quartz_block"))
                                        self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h, z + depth-1-i ), Block("quartz_block"))
                                        
                                        self.grid3d[ x_plan3d+j-1, round(height+h), z_plan3d+ i] = True
                                        self.grid3d[ x_plan3d+j-1, round(height+h), z_plan3d+ depth-1-i] = True
                                    elif j == width:
                                        self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h, z + i ), Block("quartz_block"))
                                        self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h, z + depth-1-i ), Block("quartz_block"))
                                        
                                        self.grid3d[ x_plan3d+j+1, round(height+h), z_plan3d+ i] = True
                                        self.grid3d[ x_plan3d+j+1, round(height+h), z_plan3d+ depth-1-i] = True
                                    
                                else:  
                                    self.editor.placeBlock((x + j, self.coordinates_max[1]+h, z + i), Block("blackstone_slab",{"type":"bottom"}))
                                    self.editor.placeBlock((x + j, self.coordinates_max[1]+h, z + depth-1-i), Block("blackstone_slab",{"type":"bottom"}))
                                    self.editor.placeBlock((x + j, self.coordinates_max[1]+h-0.5, z + i), Block("blackstone"))
                                    self.editor.placeBlock((x + j, self.coordinates_max[1]+h-0.5, z + depth-1-i), Block("blackstone"))
                                    
                                    self.grid3d[ j, round(height+h+0.5),  i] = True
                                    self.grid3d[ j, round(height+h+0.5),  depth-1-i] = True
                                    self.grid3d[ j, round(height+h-0.5),  i] = True
                                    self.grid3d[ j, round(height+h-0.5),  depth-1-i] = True
                                
                                    if j == -1 :
                                        self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h, z + i ), Block("quartz_slab", {"type": "bottom"}))
                                        self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h, z + depth-1-i ), Block("quartz_slab", {"type": "bottom"}))
                                        self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h-1, z + i ), Block("quartz_slab", {"type": "top"}))
                                        self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h-1, z + depth-1-i ), Block("quartz_slab", {"type": "top"}))
                                        
                                        self.grid3d[ j, round(height+h),  i] = True
                                        self.grid3d[ j, round(height+h),  depth-1-i] = True
                                        self.grid3d[ j, round(height+h-1),  i] = True
                                        self.grid3d[ j, round(height+h-1),  depth-1-i] = True
                                    elif j == width:
                                        self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h, z + i ), Block("quartz_slab", {"type": "bottom"}))
                                        self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h, z + depth-1-i ), Block("quartz_slab", {"type": "bottom"}))
                                        self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h-1, z + i ), Block("quartz_slab", {"type": "top"}))
                                        self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h-1, z + depth-1-i ), Block("quartz_slab", {"type": "top"}))
                                        
                                        self.grid3d[ j, round(height+h),  i] = True
                                        self.grid3d[ j, round(height+h),  depth-1-i] = True
                                        self.grid3d[ j, round(height+h-1),  i] = True
                                        self.grid3d[ j, round(height+h-1),  depth-1-i] = True
                            else:   
                                self.editor.placeBlock((x + j, self.coordinates_max[1]+h, z + i), Block("blackstone_slab",{"type":"bottom"}))
                                self.editor.placeBlock((x + j, self.coordinates_max[1]+h, z + depth-1-i), Block("blackstone_slab",{"type":"bottom"}))
                                
                                self.grid3d[ j, round(height+h),  i] = True
                                self.grid3d[ j, round(height+h),  depth-1-i] = True
                                
                                if j == -1 :
                                    self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h, z + i ), Block("quartz_slab", {"type": "bottom"}))
                                    self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h, z + depth-1-i ), Block("quartz_slab", {"type": "bottom"}))
                                    if not self.grid3d[ j, height+h-1,  i]:
                                        self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h-1, z + i ), Block("quartz_slab", {"type": "top"}))
                                        self.grid3d[ j, height+h-1,  i] = True
                                    if not self.grid3d[ j, height+h-1,  depth-1-i]:
                                        self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h-1, z + depth-1-i ), Block("quartz_slab", {"type": "top"}))
                                        self.grid3d[ j, height+h-1,  depth-1-i] = True
                                    
                                    self.grid3d[ j, round(height+h),  i] = True
                                    self.grid3d[ j, round(height+h),  depth-1-i] = True
                                elif j == width:
                                    self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h, z + i ), Block("quartz_slab", {"type": "bottom"}))
                                    self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h, z + depth-1-i ), Block("quartz_slab", {"type": "bottom"}))
                                    if not self.grid3d[ j, height+h-1,  i]:
                                        self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h-1, z + i ), Block("quartz_slab", {"type": "top"}))
                                        self.grid3d[ j, height+h-1,  i] = True
                                    if not self.grid3d[ j, height+h-1,  depth-1-i]:
                                        self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h-1, z + depth-1-i ), Block("quartz_slab", {"type": "top"}))
                                        self.grid3d[ j, height+h-1,  depth-1-i] = True
                                    
                                    self.grid3d[ j, round(height+h),  i] = True
                                    self.grid3d[ j, round(height+h),  depth-1-i] = True
                                    
                                    
                                self.grid3d[ j, round(height+h),  i] = True
                                self.grid3d[ j, round(height+h),  depth-1-i] = True
                            
                       
                        if i != -1:
                            h += 0.5