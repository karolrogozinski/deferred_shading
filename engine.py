import pygame as pg
import numpy as np
import pyrr
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
from config import WIDTH, HEIGHT
from objects import Material, ObjMesh, TexturedQuad, LightCubeMesh

class Engine:

    def __init__(self, scene):
        glClearColor(0.1, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        self.shaderGPass = self.createShader(
            "shaders/g_vertex.txt", 
            "shaders/g_fragment.txt"
        )
        self.shaderLPass = self.createShader(
            "shaders/l_vertex.txt", 
            "shaders/l_fragment.txt"
        )
        self.shaderColored = self.createShader(
            "shaders/simple_vertex.txt", 
            "shaders/simple_fragment.txt"
        )

        self.set_initial_uniform_values()

        self.get_uniform_locations()

        self.create_assets(scene)

        self.create_framebuffer()

    def createShader(self, vertexFilepath, fragmentFilepath):
        with open(vertexFilepath,'r') as f:
            vertex_src = f.readlines()

        ver = compileShader(vertex_src, GL_VERTEX_SHADER)

        with open(fragmentFilepath,'r') as f:
            fragment_src = f.readlines()

        frag = compileShader(fragment_src, GL_FRAGMENT_SHADER)
        
        shader = compileProgram(ver, frag)
        
        return shader

    def get_uniform_locations(self):
        # shaders locations
        # g_shader
        glUseProgram(self.shaderGPass)
        self.viewLocTextured = glGetUniformLocation(self.shaderGPass, "view")
        # light_shader
        glUseProgram(self.shaderLPass)
        self.lightLocTextured = {
            "pos": [glGetUniformLocation(self.shaderLPass, f"lights[{i}].position") for i in range(24)],
            "color": [glGetUniformLocation(self.shaderLPass, f"lights[{i}].color") for i in range(24)],
            "strength": [glGetUniformLocation(self.shaderLPass, f"lights[{i}].strength") for i in range(24)],
            "count": glGetUniformLocation(self.shaderLPass, f"lightCount")
        }
        self.cameraLocTextured = glGetUniformLocation(self.shaderLPass, "viewPos")
        # simple_shader
        glUseProgram(self.shaderColored)
        self.viewLocUntextured = glGetUniformLocation(self.shaderColored, "view")
        self.modelLocUntextured = glGetUniformLocation(self.shaderColored, "model")
        self.colorLocUntextured = glGetUniformLocation(self.shaderColored, "color")

    def set_initial_uniform_values(self):
        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy = 45, aspect = WIDTH/HEIGHT, 
            near = 0.1, far = 40, dtype=np.float32
        )
        glUseProgram(self.shaderGPass)
        glUniformMatrix4fv(glGetUniformLocation(self.shaderGPass,"projection"),1,GL_FALSE,projection_transform)
        glUniform1i(glGetUniformLocation(self.shaderGPass, "material.albedo"), 0)
        glUniform1i(glGetUniformLocation(self.shaderGPass, "material.ao"), 1)
        glUniform1i(glGetUniformLocation(self.shaderGPass, "material.normal"), 2)
        glUniform1i(glGetUniformLocation(self.shaderGPass, "material.specular"), 3)

        glUseProgram(self.shaderLPass)
        glUniform3fv(glGetUniformLocation(self.shaderLPass,"ambient"), 1, np.array([0.1, 0.1, 0.1],dtype=np.float32))
        glUniform1i(glGetUniformLocation(self.shaderLPass, "fragment.position"), 0)
        glUniform1i(glGetUniformLocation(self.shaderLPass, "fragment.gAlbedoSpecular"), 1)
        glUniform1i(glGetUniformLocation(self.shaderLPass, "fragment.normalAo"), 2)

        glUseProgram(self.shaderColored)
        glUniformMatrix4fv(glGetUniformLocation(self.shaderColored,"projection"),1,GL_FALSE,projection_transform)

    def create_assets(self, scene):
        glUseProgram(self.shaderGPass)
        self.stone_texture = Material("Stone", "png")
        self.grass_texture = Material("Grass", "png")
        # Cubes
        self.cube_mesh = ObjMesh("models/cube.obj")
        self.cubeTransforms = np.array([
            pyrr.matrix44.create_identity(dtype=np.float32)
            for i in range(len(scene.cubes))
        ], dtype=np.float32)
        glBindVertexArray(self.cube_mesh.vao)
        self.cubeTransformVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.cubeTransformVBO)
        glEnableVertexAttribArray(5)
        glVertexAttribPointer(5, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(0))
        glEnableVertexAttribArray(6)
        glVertexAttribPointer(6, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(16))
        glEnableVertexAttribArray(7)
        glVertexAttribPointer(7, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(32))
        glEnableVertexAttribArray(8)
        glVertexAttribPointer(8, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(48))
        glVertexAttribDivisor(5,1)
        glVertexAttribDivisor(6,1)
        glVertexAttribDivisor(7,1)
        glVertexAttribDivisor(8,1)
        # Spheres
        self.sphere_mesh = ObjMesh("models/sphere.obj")
        self.sphereTransforms = np.array([
            pyrr.matrix44.create_identity(dtype=np.float32)
            for i in range(len(scene.spheres))
        ], dtype=np.float32)
        glBindVertexArray(self.sphere_mesh.vao)
        self.sphereTransformVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.sphereTransformVBO)
        glEnableVertexAttribArray(5)
        glVertexAttribPointer(5, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(0))
        glEnableVertexAttribArray(6)
        glVertexAttribPointer(6, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(16))
        glEnableVertexAttribArray(7)
        glVertexAttribPointer(7, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(32))
        glEnableVertexAttribArray(8)
        glVertexAttribPointer(8, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(48))
        glVertexAttribDivisor(5,1)
        glVertexAttribDivisor(6,1)
        glVertexAttribDivisor(7,1)
        glVertexAttribDivisor(8,1)
        # Cones
        self.cone_mesh = ObjMesh("models/CONE.obj")
        self.coneTransforms = np.array([
            pyrr.matrix44.create_identity(dtype = np.float32)
            for i in range(len(scene.cones))
        ], dtype=np.float32)
        self.groundTransform = np.array([pyrr.matrix44.create_identity(dtype = np.float32)], dtype=np.float32)
        glBindVertexArray(self.cone_mesh.vao)
        self.coneTransformVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.coneTransformVBO)
        glEnableVertexAttribArray(5)
        glVertexAttribPointer(5, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(0))
        glEnableVertexAttribArray(6)
        glVertexAttribPointer(6, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(16))
        glEnableVertexAttribArray(7)
        glVertexAttribPointer(7, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(32))
        glEnableVertexAttribArray(8)
        glVertexAttribPointer(8, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(48))
        glVertexAttribDivisor(5,1)
        glVertexAttribDivisor(6,1)
        glVertexAttribDivisor(7,1)
        glVertexAttribDivisor(8,1)
        # Ground
        self.ground_mesh = ObjMesh("models/cube.obj")
        glBindVertexArray(self.ground_mesh.vao)
        self.groundTransformVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.groundTransformVBO)
        glEnableVertexAttribArray(5)
        glVertexAttribPointer(5, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(0))
        glEnableVertexAttribArray(6)
        glVertexAttribPointer(6, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(16))
        glEnableVertexAttribArray(7)
        glVertexAttribPointer(7, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(32))
        glEnableVertexAttribArray(8)
        glVertexAttribPointer(8, 4, GL_FLOAT, GL_FALSE, 64, ctypes.c_void_p(48))
        glVertexAttribDivisor(5,1)
        glVertexAttribDivisor(6,1)
        glVertexAttribDivisor(7,1)
        glVertexAttribDivisor(8,1)
        # Quad
        glUseProgram(self.shaderLPass)
        self.screenQuad = TexturedQuad(0, 0, 2, 2)

        glUseProgram(self.shaderColored)
        self.light_mesh = LightCubeMesh(l = 0.1,w = 0.1,h = 0.1)

    def create_framebuffer(self):
        # gbuffer
        self.gBuffer = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.gBuffer)
        #position
        self.gPosition = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.gPosition)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB16F, WIDTH, HEIGHT, 0, GL_RGBA, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.gPosition, 0)
        #albedo/diffuse (r,g,b) + specular
        self.gAlbedoSpecular = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.gAlbedoSpecular)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, WIDTH, HEIGHT, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT1, GL_TEXTURE_2D, self.gAlbedoSpecular, 0)
        # normal+ ambient
        self.gNormalAo = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.gNormalAo)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, WIDTH, HEIGHT, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT2, GL_TEXTURE_2D, self.gNormalAo, 0)
        # zbuffer
        self.gDepthStencil = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.gDepthStencil)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, WIDTH, HEIGHT)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, self.gDepthStencil)

    def draw(self, scene):
        #refresh screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.prepare_shaders(scene)
        self.geometry_pass(scene)
        self.lighting_pass()
        self.draw_lights(scene)
        pg.display.flip()

    def prepare_shaders(self, scene):
        view_transform = pyrr.matrix44.create_look_at(
            eye=scene.camera.position,
            target=scene.camera.position + scene.camera.calculate_forward(),
            up=scene.camera.calculate_up(),
            dtype=np.float32
        )
        glUseProgram(self.shaderGPass)
        glUniformMatrix4fv(
            self.viewLocTextured, 1, GL_FALSE, view_transform
        )
        # Update cube transformations
        for i, cube in enumerate(scene.cubes):
            model_transform = pyrr.matrix44.create_from_translation(vec=np.array(cube.position), dtype=np.float32)
            self.cubeTransforms[i] = model_transform

        glBindVertexArray(self.cube_mesh.vao)
        glBindBuffer(GL_ARRAY_BUFFER,self.cubeTransformVBO)
        glBufferData(GL_ARRAY_BUFFER, self.cubeTransforms.nbytes, self.cubeTransforms, GL_STATIC_DRAW)

        # Update sphere transformations
        for i, sphere in enumerate(scene.spheres):
            model_transform = pyrr.matrix44.create_from_translation(vec=np.array(sphere.position), dtype=np.float32)
            self.sphereTransforms[i] = model_transform

        glBindVertexArray(self.sphere_mesh.vao)
        glBindBuffer(GL_ARRAY_BUFFER,self.sphereTransformVBO)
        glBufferData(GL_ARRAY_BUFFER, self.sphereTransforms.nbytes, self.sphereTransforms, GL_STATIC_DRAW)

        # Update cone transformations
        for i, cone in enumerate(scene.cones):
            model_transform = pyrr.matrix44.create_from_translation(vec=np.array(cone.position), dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_x_rotation(theta=np.radians(-90), dtype=np.float32)
            )
            self.coneTransforms[i] = model_transform

        glBindVertexArray(self.cone_mesh.vao)
        glBindBuffer(GL_ARRAY_BUFFER,self.coneTransformVBO)
        glBufferData(GL_ARRAY_BUFFER, self.coneTransforms.nbytes, self.coneTransforms, GL_STATIC_DRAW)

        # Update ground transformations
        for i, ground in enumerate(scene.ground):
            model_transform = pyrr.matrix44.create_from_scale(scale = np.array([10.0, 14.0, 0.5]), dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(vec = np.array(ground.position), dtype=np.float32)
            )
            self.groundTransform[i] = model_transform

        glBindVertexArray(self.ground_mesh.vao)
        glBindBuffer(GL_ARRAY_BUFFER,self.groundTransformVBO)
        glBufferData(GL_ARRAY_BUFFER, self.groundTransform.nbytes, self.groundTransform, GL_STATIC_DRAW)

        glUseProgram(self.shaderLPass)
        glUniform3fv(self.cameraLocTextured, 1, scene.camera.position)
        #lights
        glUniform1f(self.lightLocTextured["count"], min(24,max(0,len(scene.lights))))

        for i, light in enumerate(scene.lights):
            if i >= 24:
                break
            glUniform3fv(self.lightLocTextured["pos"][i], 1, light.position)
            glUniform3fv(self.lightLocTextured["color"][i], 1, light.color)
            glUniform1f(self.lightLocTextured["strength"][i], light.strength)
        
        glUseProgram(self.shaderColored)
        glUniformMatrix4fv(self.viewLocUntextured, 1, GL_FALSE, view_transform)

    def geometry_pass(self, scene):
        glEnable(GL_CULL_FACE)
        glUseProgram(self.shaderGPass)
        glBindFramebuffer(GL_FRAMEBUFFER, self.gBuffer)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glDrawBuffers(3, (GL_COLOR_ATTACHMENT0, GL_COLOR_ATTACHMENT1, GL_COLOR_ATTACHMENT2))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.grass_texture.use()

        # Draw cubes
        glBindVertexArray(self.cube_mesh.vao)
        glDrawArraysInstanced(GL_TRIANGLES, 0, self.cube_mesh.vertex_count, len(scene.cubes))

        # Draw ground
        glBindVertexArray(self.ground_mesh.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.ground_mesh.vertex_count)

        self.stone_texture.use()

        # Draw spheres
        glBindVertexArray(self.sphere_mesh.vao)
        glDrawArraysInstanced(GL_TRIANGLES, 0, self.sphere_mesh.vertex_count, len(scene.spheres))

        # Draw cones
        glBindVertexArray(self.cone_mesh.vao)
        glDrawArraysInstanced(GL_TRIANGLES, 0, self.cone_mesh.vertex_count, len(scene.cones))

    def lighting_pass(self):
        glUseProgram(self.shaderLPass)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.gPosition)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.gAlbedoSpecular)
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.gNormalAo)
        glBindVertexArray(self.screenQuad.vao)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindFramebuffer(GL_READ_FRAMEBUFFER, self.gBuffer)
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)
        glBlitFramebuffer(0, 0, WIDTH, HEIGHT, 0, 0, WIDTH, HEIGHT, GL_DEPTH_BUFFER_BIT, GL_NEAREST)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def draw_lights(self, scene):
        glDisable(GL_CULL_FACE)
        glUseProgram(self.shaderColored)
        for light in scene.lights:
            model_transform = pyrr.matrix44.create_from_translation(
                vec=np.array(light.position),dtype=np.float32
            )
            glUniformMatrix4fv(self.modelLocUntextured, 1, GL_FALSE, model_transform)
            glUniform3fv(self.colorLocUntextured, 1, light.color)
            glBindVertexArray(self.light_mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.light_mesh.vertex_count)

    def quit(self):
        self.cube_mesh.destroy()
        self.sphere_mesh.destroy()
        self.ground_mesh.destroy()
        self.cone_mesh.destroy()
        self.light_mesh.destroy()
        self.stone_texture.destroy()
        self.grass_texture.destroy()
        self.screenQuad.destroy()
        glDeleteFramebuffers(1, (self.gBuffer,))
        glDeleteTextures(3, (self.gPosition, self.gAlbedoSpecular, self.gNormalAo))
        glDeleteBuffers(1, (self.cubeTransformVBO,))
        glDeleteBuffers(1, (self.sphereTransformVBO,))
        glDeleteBuffers(1, (self.coneTransformVBO,))
        glDeleteRenderbuffers(1, (self.gDepthStencil,))
        glDeleteProgram(self.shaderGPass)
        glDeleteProgram(self.shaderLPass)
        glDeleteProgram(self.shaderColored)
        pg.quit()
