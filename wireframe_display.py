import wireframe as wf
import pygame

class ProjectionViewer:

    key_to_func = {
        pygame.K_LEFT: (lambda x: x.translateAll([-10, 0, 0])),
        pygame.K_RIGHT: (lambda x: x.translateAll([10, 0, 0])),
        pygame.K_DOWN: (lambda x: x.translateAll([0, 10, 0])),
        pygame.K_UP: (lambda x: x.translateAll([0, -10, 0])),
        pygame.K_EQUALS: (lambda x: x.scaleAll(1.25)),
        pygame.K_MINUS: (lambda x: x.scaleAll(0.75)),
        pygame.K_q: (lambda x: x.rotateX(0.1)),
        pygame.K_w: (lambda x: x.rotateX(-0.1)),
        pygame.K_a: (lambda x: x.rotateY(0.1)),
        pygame.K_s: (lambda x: x.rotateY( -0.1)),
        pygame.K_z: (lambda x: x.rotateZ(0.1)),
        pygame.K_x: (lambda x: x.rotateZ(-0.1)),
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Wireframe Display")
        self.background = (10, 10, 50)

        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColor = (255, 255, 255)
        self.edgeColor = (200, 200, 200)
        self.nodeRadius = 4

    def display(self):
        self.screen.fill(self.background)

        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for edge in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColor, (edge.start.x, edge.start.y), (edge.stop.x, edge.stop.y), 1)

            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColor, (int(node.x), int(node.y)), self.nodeRadius, 0)

    def translateAll(self, vec):
        matrix = wf.translationMatrix(*vec)
        for wireframe in self.wireframes.values():
            wireframe.transform(matrix)

    def scaleAll(self, vec):
        matrix = wf.scaleMatrix(*vec)
        for wireframe in self.wireframes.values():
            wireframe.transform(matrix)

    def rotateX(self, axis, theta):
        matrix = wf.rotateXMatrix(theta)

        for wireframe in self.wireframes.values():
            wireframe.transform(matrix)

    def rotateY(self, axis, theta):
        matrix = wf.rotateYMatrix(theta)

        for wireframe in self.wireframes.values():
            wireframe.transform(matrix)

    def rotateZ(self, axis, theta):
        matrix = wf.rotateZMatrix(theta)

        for wireframe in self.wireframes.values():
            wireframe.transform(matrix)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.key_to_func:
                        self.key_to_func[event.key](self)

            self.display()
            pygame.display.flip()

    def addWireframe(self, name, wireframe):
        self.wireframes[name] = wireframe

if __name__=="__main__":
    cube = wf.Wireframe()
    cube.addNodes([(x,y,z) for x in (50,250) for y in (50,250) for z in (50,250)])
    cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])

    pv = ProjectionViewer(400, 300)
    pv.addWireframe("cube", cube)
    pv.run()
