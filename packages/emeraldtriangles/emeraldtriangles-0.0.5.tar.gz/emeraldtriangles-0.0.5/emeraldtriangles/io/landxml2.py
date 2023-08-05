import xml.sax
import pandas as pd

class LandXMLHandler(xml.sax.ContentHandler):
    chunk_size = 1024
    
    def __init__(self):
        self.path = []
        self.meta = {}
        self.surfaces = {}
        self.content = ""
        
    def add_meta(self, path, meta, attributes):
        if len(path) == 0:
            meta.update(attributes)
        else:
            if path[0] not in meta:
                meta[path[0]] = {}
            self.add_meta(path[1:], meta[path[0]], attributes)
                
    def startElement(self, tag, attributes):
        self.path.append(tag)
        if self.path[:2] == ["LandXML", "Surfaces"]:
            if self.path == ["LandXML", "Surfaces", "Surface"]:
                self.surfaces[attributes["name"]] = self.surface = {
                    "vertices": [],
                    "triangles": []
                }
                self.vertices = None
                self.triangles = None
                self.vertice_idx = 0
                self.triangle_idx = 0
            if tag in ("P", "F"):
                self.content = ""
        else:
            self.add_meta(self.path[1:], self.meta, attributes)

    def endElement(self, tag):
        if tag == "P":
            self.append_point([float(val) for val in self.content.strip().split(" ")])
            self.content = ""
        elif tag == "F":
            self.append_triangle([int(val) for val in self.content.strip().split(" ")])
            self.content = ""
        elif tag == "Surface":
            self.surface["vertices"] = pd.concat(self.surface["vertices"]).loc[:self.vertice_idx - 1]
            self.surface["triangles"] = pd.concat(self.surface["triangles"]).loc[:self.triangle_idx - 1]
        self.path.pop()
        
    def characters(self, content):
        self.content += content

    def append_point(self, point):
        end = self.vertices.index.max() if self.vertices is not None else -1
        if self.vertice_idx > end:
            self.vertices = pd.DataFrame(index=pd.RangeIndex(end + 1, end + 1 + self.chunk_size), columns=("Y", "X", "Z", "M"))
            self.surface["vertices"].append(self.vertices)
        self.vertices.loc[self.vertice_idx, ("Y", "X", "Z", "M")[:len(point)]] = point
        self.vertice_idx += 1

    def append_triangle(self, triangle):
        end = self.triangles.index.max() if self.triangles is not None else -1
        if self.triangle_idx > end:
            self.triangles = pd.DataFrame(index=pd.RangeIndex(end + 1, end + 1 + self.chunk_size), columns=(0, 1, 2))
            self.surface["triangles"].append(self.triangles)
        self.triangles.loc[self.triangle_idx, (0, 1, 2)] = triangle
        self.triangles.loc[self.triangle_idx] -= 1 # LandXML points are numbered from 1, not 0
        self.triangle_idx += 1

def parse(xmlfile):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = LandXMLHandler()
    parser.setContentHandler(handler)
    parser.parse(xmlfile)
    return {"meta": handler.meta, "surfaces": handler.surfaces}
