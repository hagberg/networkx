#!/usr/bin/env python
from nose.tools import *
import networkx
from test_graph import BaseAttrGraphTester,TestGraph
from scipy import sparse


class TestSparseGraph(TestGraph,BaseAttrGraphTester):
    """Tests specific to sparse graph data structure"""
    def setUp(self):
        self.Graph=networkx.SparseGraph
        # build dict-of-dict-of-dict K3
        ed1,ed2,ed3 = ({},{},{})
#        self.k3adj={0: {1: ed1, 2: ed2},
#                    1: {0: ed1, 2: ed3},
#                    2: {0: ed2, 1: ed3}}
        self.k3edges=[(0, 1), (0, 2), (1, 2)]
        self.k3nodes=[0, 1, 2]
        self.K3=self.Graph()
        format = self.K3.matrix.format
        self.K3.matrix = sparse.csr_matrix((20,20)).asformat(format)
        self.K3.matrix[0,1]=1
        self.K3.matrix[0,2]=1
        self.K3.matrix[1,0]=1
        self.K3.matrix[1,2]=1
        self.K3.matrix[2,0]=1
        self.K3.matrix[2,1]=1
        self.K3.node={}
        self.K3.node[0]={}
        self.K3.node[1]={}
        self.K3.node[2]={}

    def test_data_input(self):
        pass # not implemented

    def test_add_edges_from(self):
        G=self.Graph()
        G.add_edges_from([(0,1),(0,2,{'weight':3})])
        assert_equal(G.adj,{0: {1:{}, 2:{'weight':3}}, 1: {0:{}}, \
                2:{0:{'weight':3}}})
        G=self.Graph()
        G.add_edges_from([(0,1),(0,2,{'weight':3}),(1,2,{'data':4})],data=2)
        assert_equal(G.adj,{\
                0: {1:{'data':2}, 2:{'weight':3,'data':2}}, \
                1: {0:{'data':2}, 2:{'data':4}}, \
                2: {0:{'weight':3,'data':2}, 1:{'data':4}} \
                })

        assert_raises(networkx.NetworkXError,
                      G.add_edges_from,[(0,)])  # too few in tuple
        assert_raises(networkx.NetworkXError,
                      G.add_edges_from,[(0,1,2,3)])  # too many in tuple
        assert_raises(TypeError, G.add_edges_from,[0])  # not a tuple



    def test_to_undirected(self):
        G=self.K3
        self.add_attributes(G)
        H=networkx.Graph(G)
        # not implemented
        # self.is_shallow_copy(H,G)
        # H=G.to_undirected()
        # self.is_deepcopy(H,G)

# not implemented
    def test_to_directed(self):
        pass


    def test_edge_attr(self):
        pass

    def test_edge_attr2(self):
        pass

    def test_edge_attr3(self):
        pass

    def test_edge_attr4(self):
        pass

    def test_copy_attr(self):
        pass

    def test_copy(self):
        pass

    def test_add_edges_from(self):
        G=self.Graph()
        G.add_edges_from([(0,1),(0,2,{'weight':3})])
        assert_equal(G.adj,{0: {1:{}, 2:{'weight':3}}, 1: {0:{}}, \
                2:{0:{'weight':3}}})
        G=self.Graph()
        assert_raises(networkx.NetworkXError,
                      G.add_edges_from,[(0,)])  # too few in tuple
        assert_raises(networkx.NetworkXError,
                      G.add_edges_from,[(0,1,2,3)])  # too many in tuple
        assert_raises(TypeError, G.add_edges_from,[0])  # not a tuple

    def test_add_cycle(self):
        G=self.K3.copy()
        nlist=[12,13,14,15]
        oklists=[ [(12,13),(12,15),(13,14),(14,15)], \
                      [(12,13),(13,14),(14,15),(15,12)] ]
        G.add_cycle(nlist)
        assert_true(sorted(G.edges(nlist)) in oklists)
        G=self.K3.copy()
        oklists=[ [(12,13,{'weight':2.}),\
                (12,15,{'weight':2.}),\
                (13,14,{'weight':2.}),\
                (14,15,{'weight':2.})], \
                \
                [(12,13,{'weight':2.}),\
                (13,14,{'weight':2.}),\
                (14,15,{'weight':2.}),\
                (15,12,{'weight':2.})] \
                ]

        G.add_cycle(nlist,weight=2.0)
        assert_true(sorted(G.edges(nlist,data=True)) in oklists)

    def test_weighted_degree(self):
        G=self.Graph()
        G.add_edge(1,2,weight=2,other=3)
        G.add_edge(2,3,weight=3,other=4)
        assert_equal(list(G.degree(weight='weight').values()),[2,5,3])
        assert_equal(G.degree(weight='weight'),{1:2,2:5,3:3})
        assert_equal(G.degree(1,weight='weight'),2)
        assert_equal(G.degree([1],weight='weight'),{1:2})

        # assert_equal(list(G.degree(weight='other').values()),[3,7,4])
        # assert_equal(G.degree(weight='other'),{1:3,2:7,3:4})
        # assert_equal(G.degree(1,weight='other'),3)
        # assert_equal(G.degree([1],weight='other'),{1:3})

    def test_subgraph(self):
        G=self.K3
        H=G.subgraph([0,1,2,5])
        assert_equal(sorted(G.nodes()),sorted(H.nodes()))
        assert_equal([sorted(e) for e in sorted(G.edges())],
                     [sorted(e) for e in sorted(H.edges())])

        H=G.subgraph(0)
        assert_equal(H.adj,{0:{}})
        H=G.subgraph([])
        assert_equal(H.adj,{})
        assert_not_equal(G.adj,{})
